import hashlib
from pathlib import Path
import tempfile
import unittest

import build_desktop as build


class PackagingTests(unittest.TestCase):
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
