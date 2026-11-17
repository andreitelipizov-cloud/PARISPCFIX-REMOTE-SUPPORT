#!/usr/bin/env python3
"""Build the branded native editions on the matching OS, then package them."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import plistlib
import re
import shutil
import subprocess
import sys
import tarfile

ROOT = Path(__file__).resolve().parents[1]


def run(*args, cwd=ROOT, env=None):
    subprocess.run([str(a) for a in args], cwd=cwd, env=env, check=True)


def product(edition):
    if edition not in ("client", "admin"):
        raise ValueError("Edition must be client or admin")
    return "PARISPCFIX-" + edition.upper()


def features(edition, system, arch):
    product(edition)
    result = ["flutter", "hwcodec", "unix-file-copy-paste", "parispcfix-" + edition]
    if system == "Darwin" and arch == "arm64":
        result.append("screencapturekit")
    return ",".join(result)


def version():
    match = re.search(r'^version\s*=\s*"([^"]+)"',
                      (ROOT / "Cargo.toml").read_text(encoding="utf-8"), re.M)
    if not match:
        raise RuntimeError("Cargo package version missing")
    return match.group(1)


def write_provenance(destination, edition, system, arch):
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT,
                                     text=True).strip()
    (destination / "build-info.json").write_text(json.dumps({
        "product": product(edition), "version": version(), "platform": system,
        "architecture": arch, "source_commit": commit,
        "publisher_signature": "not configured",
        "apple_notarization": "not configured" if system == "Darwin" else "not applicable",
    }, indent=2) + "\n", encoding="utf-8")
    shutil.copy2(ROOT / "LICENCE", destination / "LICENCE-AGPL-3.0.txt")
    shutil.copy2(ROOT / "parispcfix" / "DESKTOP-RELEASE.md", destination / "README.md")


def sha256_manifest(destination):
    rows = []
    for path in sorted(destination.iterdir()):
        if path.is_file() and path.name != "SHA256SUMS":
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            rows.append(f"{digest}  {path.name}\n")
    (destination / "SHA256SUMS").write_text("".join(rows), encoding="utf-8")


def configure_macos(edition, arch):
    # Keep native executable/framework names: upstream helper loading relies on them.
    minimum = "12.3" if arch == "arm64" else "10.14"
    path = ROOT / "flutter/macos/Runner/Configs/AppInfo.xcconfig"
    text = path.read_text(encoding="utf-8")
    text = re.sub(r'^PRODUCT_BUNDLE_IDENTIFIER\s*=.*$',
                  "PRODUCT_BUNDLE_IDENTIFIER = fr.parispcfix.remote." + edition, text, flags=re.M)
    path.write_text(text, encoding="utf-8")
    path = ROOT / "flutter/macos/Runner.xcodeproj/project.pbxproj"
    text = path.read_text(encoding="utf-8")
    text = re.sub(r'MACOSX_DEPLOYMENT_TARGET = [\d.]+;',
                  f"MACOSX_DEPLOYMENT_TARGET = {minimum};", text)
    path.write_text(text, encoding="utf-8")
    path = ROOT / "flutter/macos/Podfile"
    text = re.sub(r"platform :osx, '[^']+'", f"platform :osx, '{minimum}'",
                  path.read_text(encoding="utf-8"))
    path.write_text(text, encoding="utf-8")
    return minimum


def package_macos(output, edition, arch):
    name = product(edition)
    source = ROOT / "flutter/build/macos/Build/Products/Release/RustDesk.app"
    app = output / (name + ".app")
    shutil.copytree(source, app, symlinks=True)
    shutil.copy2(ROOT / "target/release/service", app / "Contents/MacOS/service")
    plist_path = app / "Contents/Info.plist"
    with plist_path.open("rb") as stream:
        metadata = plistlib.load(stream)
    metadata["CFBundleName"] = name
    metadata["CFBundleDisplayName"] = name
    metadata["CFBundleIdentifier"] = "fr.parispcfix.remote." + edition
    metadata["NSHumanReadableCopyright"] = "PARISPCFIX. Based on RustDesk (AGPL-3.0)."
    with plist_path.open("wb") as stream:
        plistlib.dump(metadata, stream)
    iconset = output / "AppIcon.iconset"
    iconset.mkdir()
    for size in (16, 32, 128, 256, 512):
        for scale in (1, 2):
            suffix = "@2x" if scale == 2 else ""
            run("sips", "-z", size * scale, size * scale,
                ROOT / "flutter/assets/parispcfix-icon.png", "--out",
                iconset / f"icon_{size}x{size}{suffix}.png")
    run("iconutil", "-c", "icns", iconset, "-o", app / "Contents/Resources/AppIcon.icns")
    # Ad-hoc integrity signatures permit local testing, but assert NO publisher trust.
    run("codesign", "--force", "--deep", "--sign", "-", "--entitlements",
        ROOT / "flutter/macos/Runner/Release.entitlements", app)
    run("codesign", "--verify", "--deep", "--strict", app)
    image_root = output / "disk-image"
    image_root.mkdir()
    shutil.move(str(app), image_root / app.name)
    (image_root / "Applications").symlink_to("/Applications")
    shutil.copy2(output / "README.md", image_root / "README.md")
    run("hdiutil", "create", "-volname", name, "-srcfolder", image_root,
        "-format", "UDZO", output / f"{name}-{version()}-macOS-{arch}.dmg")
    shutil.rmtree(image_root)
    shutil.rmtree(iconset)


def linux_desktop(edition):
    name = "parispcfix-" + edition
    return ("[Desktop Entry]\nType=Application\n"
            f"Name={product(edition)}\nComment=Remote support\n"
            f"Exec=/opt/{name}/rustdesk %u\nIcon={name}\n"
            "Terminal=false\nCategories=Network;RemoteAccess;\n")


def package_linux(output, edition, arch):
    name = product(edition)
    source = ROOT / "flutter/build/linux/x64/release/bundle"
    if not (source / "rustdesk").is_file() or not (source / "lib/librustdesk.so").is_file():
        raise RuntimeError("Native Linux application or engine missing")
    bundle = output / name
    shutil.copytree(source, bundle, symlinks=True)
    shutil.copy2(output / "README.md", bundle / "README.md")
    with tarfile.open(output / f"{name}-{version()}-Linux-{arch}.tar.gz", "w:gz") as archive:
        archive.add(bundle, arcname=name)
    deb_root = output / "deb-root"
    package = "parispcfix-" + edition
    application = deb_root / "opt" / package
    application.parent.mkdir(parents=True)
    shutil.move(str(bundle), application)
    control = deb_root / "DEBIAN"
    control.mkdir()
    (control / "control").write_text(
        f"Package: {package}\nVersion: {version()}\nArchitecture: amd64\n"
        "Maintainer: PARISPCFIX\nSection: net\nPriority: optional\n"
        "Depends: libgtk-3-0, libayatana-appindicator3-1, libasound2, libpulse0, libxdo3, libva2\n"
        f"Description: {name} remote support for the current desktop session\n",
        encoding="utf-8")
    applications = deb_root / "usr/share/applications"
    applications.mkdir(parents=True)
    (applications / (package + ".desktop")).write_text(linux_desktop(edition), encoding="utf-8")
    icons = deb_root / "usr/share/icons/hicolor/256x256/apps"
    icons.mkdir(parents=True)
    shutil.copy2(ROOT / "flutter/assets/parispcfix-icon.png", icons / (package + ".png"))
    run("dpkg-deb", "--root-owner-group", "--build", deb_root,
        output / f"{name}-{version()}-Linux-amd64.deb")
    shutil.rmtree(deb_root)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--edition", required=True, choices=("client", "admin"))
    args = parser.parse_args()
    system = platform.system()
    arch = "arm64" if platform.machine().lower() in ("aarch64", "arm64") else "x86_64"
    if system not in ("Darwin", "Linux") or (system == "Linux" and arch != "x86_64"):
        parser.error("Build on macOS Intel/Apple Silicon or Linux x86_64")
    os.environ["PARISPCFIX_EDITION"] = args.edition
    if system == "Darwin":
        os.environ["MACOSX_DEPLOYMENT_TARGET"] = configure_macos(args.edition, arch)
    else:
        runner = ROOT / "flutter/linux/my_application.cc"
        text = runner.read_text(encoding="utf-8")
        for call in ("gtk_header_bar_set_title(header_bar,", "gtk_window_set_title(window,"):
            text = text.replace(call + ' "rustdesk")', call + f' "{product(args.edition)}")')
        runner.write_text(text, encoding="utf-8")
    build_features = features(args.edition, system, arch)
    command = ["cargo", "build", "--locked", "--release", "--features", build_features]
    if system == "Linux":
        command.append("--lib")
    run(*command)
    if system == "Darwin":
        shutil.copy2(ROOT / "target/release/liblibrustdesk.dylib", ROOT / "target/release/librustdesk.dylib")
        os.environ["FLUTTER_XCODE_ARCHS"] = arch
        os.environ["FLUTTER_XCODE_ONLY_ACTIVE_ARCH"] = "YES"
    else:
        bridge = ROOT / "flutter/lib/generated_bridge.dart"
        text = bridge.read_text(encoding="utf-8").replace(
            "ffi.NativeFunction<ffi.Bool Function(DartPort", "ffi.NativeFunction<ffi.Uint8 Function(DartPort")
        bridge.write_text(text, encoding="utf-8")
    run("flutter", "build", "macos" if system == "Darwin" else "linux", "--release",
        "--dart-define=PARISPCFIX=true", "--dart-define=PARISPCFIX_EDITION=" + args.edition,
        cwd=ROOT / "flutter")
    output = ROOT / "parispcfix/dist" / (system + "-" + arch + "-" + args.edition)
    output.mkdir(parents=True, exist_ok=False)
    write_provenance(output, args.edition, system, arch)
    if system == "Darwin":
        package_macos(output, args.edition, arch)
    else:
        package_linux(output, args.edition, arch)
    sha256_manifest(output)
    print("Artifacts:", output)


if __name__ == "__main__":
    main()
