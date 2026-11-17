# PARISPCFIX native connection policy

PARISPCFIX CLIENT and ADMIN require an encrypted session channel. Outgoing
sessions also require a remote identity verified by the existing handshake.
A missing or invalid server public key cannot be overridden to continue a
session. Bare IP/domain-and-port connections without the protected handshake
are rejected; use the peer ID with the correct ID server and public key.

This policy applies to native session startup, including desktop control,
file transfer and tunnels that use Client::start. Incoming sessions are
rejected before the login challenge and authorization processing. Password,
consent, permissions and optional two-factor authentication still apply.
Encryption alone does not authenticate an incoming operator.

Existing RustDesk behavior is preserved when the parispcfix feature is off.
No cryptographic algorithms, submodules or saved user settings are changed.
This does not implement a policy for the separate JavaScript web client.

Regression surface:
- src/client.rs: reject an unprotected or unverified outgoing session before
  returning its stream to login/session handlers.
- src/server/connection.rs: reject an unprotected incoming stream before
  login setup, irrespective of the incoming transport.
- src/parispcfix.rs: expose the feature-specific security policy.
- PARISPCFIX Windows and desktop workflows: run policy regression tests and
  trigger new builds when these security paths change.

Three standalone Rust regression tests cover plaintext rejection, encrypted
but unverified peer rejection, and the incoming encryption requirement.
They do not replace live handshake or end-to-end platform tests.
