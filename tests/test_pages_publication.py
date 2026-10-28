"""The public website must not disclose runtime notification credentials."""

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import yaml

from scripts import prepare_pages


class PublicPagesTests(unittest.TestCase):
    def test_runtime_credentials_are_redacted_without_mutating_configuration(self):
        config = {
            "notification": {"channels": {
                "email": {"from": "private@example.com", "to": "recipient@example.com", "password": "smtp-secret"},
                "telegram": {"bot_token": "bot-secret", "chat_id": "private-chat"},
                "feishu": {"webhook_url": "https://private.example/webhook"},
            }},
            "ai": {"api_key": "ai-secret", "model": "example/model"},
            "storage": {"remote": {"secret_access_key": "storage-secret", "retention_days": 7}},
        }
        public = prepare_pages.public_config(config)
        text = yaml.safe_dump(public)
        for secret in ("private@example.com", "recipient@example.com", "smtp-secret", "bot-secret", "private-chat", "private.example", "ai-secret", "storage-secret"):
            self.assertNotIn(secret, text)
        self.assertEqual(config["notification"]["channels"]["email"]["password"], "smtp-secret")
        self.assertEqual(public["ai"]["model"], "example/model")

    def test_site_contains_only_selected_files_and_preserves_the_email_report(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in ("output", "docs/assets", "config"):
                (root / name).mkdir(parents=True)
            report = "<!doctype html><html><head></head><body>Fresh news</body></html>"
            (root / "output/index.html").write_text(report)
            (root / "output/private.db").write_text("database-secret")
            (root / "docs/index.html").write_text("Editor")
            (root / "docs/assets/not-for-publication.txt").write_text("private-file")
            for name in ("style.css", "script.js", "i18n.js"):
                (root / "docs/assets" / name).write_text("")
            (root / "config/config.yaml").write_text("platforms: {sources: []}\nrss: {feeds: []}\n")
            for name in ("frequency_words.txt", "timeline.yaml"):
                (root / "config" / name).write_text("")
            (root / "version_configs").write_text("2.4.0")
            with patch.object(prepare_pages, "ROOT", root):
                destination = prepare_pages.prepare_pages(root / "site")
            self.assertIn("配置编辑器", (destination / "index.html").read_text())
            self.assertTrue((destination / "editor/assets/script.js").is_file())
            self.assertTrue((destination / "sources.html").is_file())
            self.assertFalse(list(destination.rglob("*.db")))
            self.assertFalse((destination / "editor/assets/not-for-publication.txt").exists())
            self.assertEqual((root / "output/index.html").read_text(), report)


if __name__ == "__main__":
    unittest.main()
