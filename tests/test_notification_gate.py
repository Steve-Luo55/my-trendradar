"""Ordinary page refreshes must not send an email edition."""

import os
import unittest
from unittest.mock import patch

from trendradar.core.loader import _load_notification_config


class NotificationGateTests(unittest.TestCase):
    def load(self, gate, enabled=True):
        with patch.dict(os.environ, {}, clear=True):
            if gate is not None:
                os.environ["NOTIFICATION_ENABLED"] = gate
            return _load_notification_config({"notification": {"enabled": enabled}})["ENABLE_NOTIFICATION"]

    def test_regular_refresh_does_not_send(self):
        self.assertFalse(self.load("false"))

    def test_email_edition_and_existing_cli_behavior_remain_available(self):
        self.assertTrue(self.load("true"))
        self.assertTrue(self.load(None))

    def test_explicit_global_disable_still_wins(self):
        self.assertFalse(self.load("true", enabled=False))


if __name__ == "__main__":
    unittest.main()
