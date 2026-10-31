import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import scraper


class ScraperTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.data_path = Path(self.temp_dir.name) / "data.json"
        self.metadata_path = Path(self.temp_dir.name) / "sync_metadata.json"
        self.data_path.write_text(
            json.dumps([{"institute": "Test Institute", "source_url": "https://example.invalid"}]),
            encoding="utf-8",
        )
        self.paths = (
            patch.object(scraper, "DATA_PATH", self.data_path),
            patch.object(scraper, "METADATA_PATH", self.metadata_path),
        )
        for path_patch in self.paths:
            path_patch.start()
            self.addCleanup(path_patch.stop)

    def test_successful_refresh_updates_data_and_timestamp(self):
        with patch.dict(scraper.SCRAPERS, {"Test Institute": lambda url: {"status": "Open"}}):
            with contextlib.redirect_stdout(io.StringIO()):
                result = scraper.update_recruitments()

        self.assertEqual(result, (1, 0))
        self.assertEqual(json.loads(self.data_path.read_text(encoding="utf-8"))[0]["status"], "Open")
        self.assertIn("last_updated", json.loads(self.metadata_path.read_text(encoding="utf-8")))

    def test_failed_refresh_preserves_data_and_timestamp(self):
        original_data = self.data_path.read_text(encoding="utf-8")
        original_metadata = '{"last_updated": "previous sync"}'
        self.metadata_path.write_text(original_metadata, encoding="utf-8")

        with patch.dict(scraper.SCRAPERS, {"Test Institute": lambda url: None}):
            with contextlib.redirect_stdout(io.StringIO()):
                result = scraper.update_recruitments()

        self.assertEqual(result, (0, 1))
        self.assertEqual(self.data_path.read_text(encoding="utf-8"), original_data)
        self.assertEqual(self.metadata_path.read_text(encoding="utf-8"), original_metadata)


if __name__ == "__main__":
    unittest.main()
