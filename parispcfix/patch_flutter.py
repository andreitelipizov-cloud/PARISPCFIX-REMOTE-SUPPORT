"""Apply the pinned SDK patch once, including when a patched SDK is cached."""
import os
from pathlib import Path
import subprocess


def apply_once(sdk, patch):
    command = ["git", "-C", str(sdk), "apply"]
    if subprocess.run(command + ["--check", str(patch)], capture_output=True).returncode == 0:
        subprocess.run(command + [str(patch)], check=True)
        return
    if subprocess.run(command + ["--reverse", "--check", str(patch)], capture_output=True).returncode == 0:
        print("Flutter SDK already contains the required patch")
        return
    raise RuntimeError("Flutter SDK does not match the pinned patch; refusing to continue")


if __name__ == "__main__":
    sdk = Path(os.environ["FLUTTER_ROOT"]).resolve()
    patch = Path(__file__).resolve().parents[1] / ".github/patches/flutter_3.24.4_dropdown_menu_enableFilter.diff"
    apply_once(sdk, patch)
