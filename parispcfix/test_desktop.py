import hashlib
from pathlib import Path
import tempfile
import unittest

import build_desktop as build
from patch_flutter import apply_once


class PackagingTests(unittest.TestCase):
    def test_cached_flutter_patch_is_repeatable_and_rejects_incompatible_sdk(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "example.txt"
            source.write_bytes(b"before\n")
            patch = root / "sdk.patch"
            patch.write_bytes(b"diff --git a/example.txt b/example.txt\n--- a/example.txt\n+++ b/example.txt\n@@ -1 +1 @@\n-before\n+after\n")
            apply_once(root, patch)
            apply_once(root, patch)
            self.assertEqual(source.read_text(encoding="utf-8"), "after\n")
            source.write_bytes(b"incompatible\n")
            with self.assertRaises(RuntimeError):
                apply_once(root, patch)

    def test_checksum_manifest_verifies_downloaded_packages(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "PARISPCFIX-CLIENT.dmg").write_bytes(b"test disk image")
            (root / "README.md").write_text("instructions", encoding="utf-8")
            build.sha256_manifest(root)
            for row in (root / "SHA256SUMS").read_text(encoding="utf-8").splitlines():
                digest, filename = row.split("  ", 1)
                self.assertEqual(hashlib.sha256((root / filename).read_bytes()).hexdigest(), digest)
            self.assertNotIn("SHA256SUMS", (root / "SHA256SUMS").read_text(encoding="utf-8"))

    def test_client_and_admin_launchers_are_independent(self):
        for edition in ("client", "admin"):
            entry = build.linux_desktop(edition)
            self.assertIn(f"Name=PARISPCFIX-{edition.upper()}\n", entry)
            self.assertIn(f"Exec=/opt/parispcfix-{edition}/rustdesk %u\n", entry)
            self.assertNotIn("sudo", entry)
            self.assertNotIn("--service", entry)
        with self.assertRaises(ValueError):
            build.features("--service", "Linux", "x86_64")


if __name__ == "__main__":
    unittest.main()
