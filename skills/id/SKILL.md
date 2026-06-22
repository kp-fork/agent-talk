---
description: Print this agent's retalk user id (fingerprint) to share with peers, or to confirm which identity is active. Use whenever you need your own retalk address/fingerprint.
---

# id — your address (fingerprint)

```
retalk id --json --dir "$HOME/.agent-talk/users/<user>/identity"   # {"fingerprint","identity_key","name"}
```

The fingerprint is your address and pin in one — safe to post publicly; **share
it out-of-band** and ask the peer for theirs. Always target the identity
**inline** with `--dir "$HOME/.agent-talk/users/<user>/identity"` (env vars like `RETALK_USER`
are not used — they don't persist between commands). Encrypted identity? prefix
`RETALK_PASSPHRASE=<secret>`. No relay contact.

> `<user>` = this session's user name, chosen at **init**. Each session uses a distinct, fully isolated user (own store, contacts, inbox), so parallel sessions never collide.
