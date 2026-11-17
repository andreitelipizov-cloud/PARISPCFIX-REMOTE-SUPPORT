# PARISPCFIX Remote Support — desktop releases

The CLIENT edition receives assistance. The ADMIN edition connects to remote devices.
Both editions use the same integrated RustDesk engine, AGPL-3.0 source and five-language interface.

## Packages

- Windows: the existing PARISPCFIX Windows installers workflow.
- macOS Intel: DMG containing PARISPCFIX-CLIENT.app or PARISPCFIX-ADMIN.app.
- macOS Apple Silicon: a separate ARM64 DMG; the ScreenCaptureKit build requires macOS 12.3 or later.
- Linux x86_64: a portable tar.gz bundle and an amd64 DEB for Debian/Ubuntu-compatible systems. The current CI baseline is Ubuntu 22.04, so older distributions are not supported by these binaries.

On Mac, open the DMG and drag the application to Applications. These test releases have only ad-hoc integrity signatures. They do not have an Apple Developer ID signature or notarization; Gatekeeper may block them. Do not disable system-wide protections. For customer distribution, sign and notarize with your own Apple Developer account first.

On Linux, unpack the tar.gz and run the included `rustdesk` executable, or install the DEB using the system package manager. The internal engine filename is retained for compatibility; the visible product is PARISPCFIX. The DEB provides a menu entry for the selected edition. It does not enable a system service, unattended access or startup automatically. Current desktop session support must be tested on real devices; login-screen access and Wayland permission behavior are not certified by a successful build.

The macOS package also retains upstream native executable/framework names so helper loading continues to work. Application names, icons and bundle IDs are branded and distinct between editions. macOS screen-recording and Accessibility permissions must be granted by the user when required; signing cannot grant those permissions.

## Build and verification

The `PARISPCFIX macOS and Linux` workflow builds both editions for all three targets. Flutter 3.24.5 is used on Intel/Linux; Apple Silicon follows upstream's Flutter 3.44.9 patch and matching generated bridge. Rust is pinned to 1.81 on macOS and 1.75 on Linux. Native dependencies follow the existing vcpkg baseline. No DRM/direct-capture feature is enabled by this workflow.

Artifacts contain the package, source commit, license and SHA256SUMS. Successful CI is evidence of compilation, packaging and the checks named in the job; it does not certify that remote control, audio, clipboard, file transfer, printing, installation or unattended access work on physical hardware.

## Signing

These builds are not signed by a publicly trusted publisher. Windows requires a trusted Code Signing provider; macOS requires Apple Developer ID and notarization; Android uses a release keystore and optional Play App Signing; iOS uses Apple distribution certificates/profiles and an allowed distribution channel. These are different trust systems. Keep private keys and passwords out of source control and reports.

## Change scope

`flutter/lib/parispcfix/brand.dart` owns the new branding, localized captions and background. `desktop_home_page.dart` changes panel presentation and branded dimensions; existing ID, password, consent, settings and connection logic is preserved. `build.py` adds the edition label to Windows Dart build flags. The new build/package script and workflow handle Mac/Linux without rewriting the existing Windows packaging path. No network protocol, authentication or permission guards are changed.

Source and upstream attribution: https://github.com/andreitelipizov-cloud/PARISPCFIX-REMOTE-SUPPORT and https://github.com/rustdesk/rustdesk.
