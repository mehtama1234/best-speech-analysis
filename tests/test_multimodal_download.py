import tempfile
import unittest
from pathlib import Path

from scripts.download_multimodal_pilot import existing_media, run_download
from scripts.recover_full_corpus_media import resolve_yt_dlp


class MultimodalDownloadTests(unittest.TestCase):
    def test_pilot_uses_resolved_downloader(self):
        self.assertTrue(resolve_yt_dlp("/bin/sh").endswith("/bin/sh"))

    def test_ledger_cannot_create_a_cache_hit_without_files(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.assertEqual(existing_media(root, "video"), [])
            self.assertEqual(
                run_download(["command-that-is-not-installed"], root, "video"),
                "failed:missing_command",
            )
            (root / "video.mp4").write_bytes(b"test")
            self.assertEqual([root / "video.mp4"], existing_media(root, "video"))


if __name__ == "__main__":
    unittest.main()
