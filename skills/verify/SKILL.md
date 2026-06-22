---
description: Record and pin a saved peer's public keys (explicit first-contact verification). Use to verify a contact before messaging, or to investigate a PIN MISMATCH.
---

# verify — pin a peer's keys

```
retalk verify <peer> --dir "$HOME/.agent-talk/users/<user>/identity"
retalk verify <peer> --identity-key K --signing-key S --dir "$HOME/.agent-talk/users/<user>/identity"
```

Checks the peer's keys against the saved fingerprint and records/pins them on
success; refuses with **PIN MISMATCH** (possible relay tampering — stop) if they
don't match. Peer must exist via **add**; fetching needs the passphrase if the
identity is encrypted (prefix `RETALK_PASSPHRASE=<secret>`). Target the identity
inline with `--dir "$HOME/.agent-talk/users/<user>/identity"`.

> `<user>` = this session's user name, chosen at **init**. Each session uses a distinct, fully isolated user (own store, contacts, inbox), so parallel sessions never collide.
