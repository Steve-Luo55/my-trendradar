"""Google's shared RSS link must not collapse distinct search trends."""

import tempfile
import unittest
from urllib.parse import parse_qs, urlsplit

from trendradar.crawler.rss.parser import RSSParser
from trendradar.storage.base import RSSData, RSSItem
from trendradar.storage.local import LocalStorageBackend


FEED = """<rss version="2.0"><channel><title>Daily Search Trends</title>
<item><title>stock futures</title><link>https://trends.google.com/trending/rss?geo=US</link></item>
<item><title>space &amp; science</title><link>https://trends.google.com/trending/rss?geo=US</link></item>
</channel></rss>"""


class GoogleTrendsTests(unittest.TestCase):
    def test_distinct_topics_survive_storage_and_link_to_their_queries(self):
        parsed = RSSParser().parse(FEED, "https://trends.google.com/trending/rss?geo=US")
        items = []
        for item in parsed:
            query = parse_qs(urlsplit(item.url).query)
            self.assertEqual(query["q"], [item.title])
            self.assertEqual(query["geo"], ["US"])
            items.append(RSSItem(title=item.title, feed_id="google-trends-us", url=item.url, guid=item.guid))
        with tempfile.TemporaryDirectory() as folder:
            backend = LocalStorageBackend(folder, enable_txt=False, enable_html=False)
            data = RSSData(date="2026-10-30", crawl_time="23:50", items={"google-trends-us": items})
            try:
                self.assertTrue(backend.save_rss_data(data))
                saved = backend.get_latest_rss_data("2026-10-30")
                self.assertEqual({item.title for item in saved.items["google-trends-us"]}, {"stock futures", "space & science"})
            finally:
                backend.cleanup()

    def test_other_feed_links_are_unchanged(self):
        item = RSSParser().parse(FEED, "https://example.com/rss")[0]
        self.assertEqual(item.url, "https://trends.google.com/trending/rss?geo=US")


if __name__ == "__main__":
    unittest.main()
