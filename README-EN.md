# My TrendRadar

[简体中文](README.md) · [Home](https://steve-luo55.github.io/my-trendradar/) · [Latest report](https://steve-luo55.github.io/my-trendradar/report/) · [Visual editor](https://steve-luo55.github.io/my-trendradar/editor/) · [Sources](https://steve-luo55.github.io/my-trendradar/sources.html) · [Run history](https://github.com/Steve-Luo55/my-trendradar/actions)

A personal trending-news reader with email notifications. The hourly job collects configured charts and RSS feeds, filters titles by keywords, publishes the latest HTML report. Email editions are scheduled for 08:30 and 20:30 Asia/Shanghai; ordinary website refreshes do not send mail.

## Sources

Twelve trending charts via the NewsNow aggregation API: Toutiao, Baidu, WallstreetCN, The Paper, bilibili, CLS, iFeng, Tieba, Weibo, Douyin, Zhihu, and GitHub Trending. These supply ranked titles and original links, rather than full article text.

Three enabled RSS feeds: U.S. Google Trends through its official RSS, Hacker News through hnrss.org, and Ars Technica through its publisher feed. The Ruanyifeng feed is disabled; the default Yahoo Finance feed is disabled because its URL returned HTTP 404.

## Reading and notifications

The report supports keyword search, topic tabs, and light/dark themes. QQ SMTP credentials live in GitHub Actions Secrets. The schedule is set to minute **37 of each hour**; report timestamps use Asia/Shanghai. Ordinary hourly refreshes are silent; the two daily email editions use separate schedule events. GitHub may delay or drop scheduled runs, so check the actual report time and workflow history.

A home page links to the report, visual editor, and source inventory. The editor starts with visual controls; raw YAML/TXT is available through an optional source panel. It is published with a credential-free snapshot of this deployment's settings. Drafts stay in the current browser. Export and commit the edited files to the repository to change background tasks; changing the UI language does not select a different source configuration.

This copy removes the upstream seven-day check-in cutoff. Weekly check-ins and run-log deletion are unnecessary. GitHub's own scheduling rules still apply, including possible suspension after prolonged repository inactivity.

## Limits and configuration

AI filtering, analysis, and translation are disabled. Keyword matches are not fact checks. Google Trends coverage is limited to U.S. recent searches, without global coverage or historical Explore data. Other major platforms such as Reddit, X, YouTube, and Product Hunt are not included. Each run uses a temporary database; the site shows the current snapshot, without durable history or reliable cross-run deduplication.

- [Deployment and email settings](docs/MY_DEPLOYMENT.md)
- [Source configuration](config/config.yaml)
- [Keyword configuration](config/frequency_words.txt)
- [Upstream technical documentation](https://trendradar.sandev.cc/en/docs/)

## Attribution and license

Based on [sansan0/TrendRadar](https://github.com/sansan0/TrendRadar) v6.11.0, with upstream copyright notices and the [GPL-3.0 license](LICENSE) retained. Aggregated chart data comes from [NewsNow](https://github.com/ourongxing/newsnow). Sponsor banners, referral links, and promotional QR codes have been removed from this copy.
