import tempfile
import unittest
from pathlib import Path

from scripts.recover_full_corpus_media import files_for, resolve_yt_dlp


class MediaRecoveryToolTests(unittest.TestCase):
    def test_files_for_ignores_temporary_and_empty_outputs(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "abc.part").write_bytes(b"x" * 5000)
            (root / "abc.mp4").write_bytes(b"")
            (root / "abc.m4a").write_bytes(b"x" * 2048)
            self.assertEqual([root / "abc.m4a"], files_for(root, "abc"))

    def test_resolves_user_local_downloader_when_path_is_missing(self):
        resolved = resolve_yt_dlp()
        self.assertTrue(resolved.endswith("yt-dlp") or resolved == "yt-dlp")


if __name__ == "__main__":
    unittest.main()
