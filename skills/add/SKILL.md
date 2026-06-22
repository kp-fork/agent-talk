---
description: Save a peer's retalk user id under a local name so you can message them by name. Use when you have a peer's fingerprint to record. If the name or fingerprint is missing, ask with AskUserQuestion.
---

# add — save a peer

```
retalk add <name> <fingerprint> --dir "<user>/identity"
```

`<name>` is a local label (yours alone; the peer never learns it); `<fingerprint>`
is the peer's 32-hex id, obtained out-of-band. If both aren't given, use
**AskUserQuestion**. Re-adding a name overwrites it. Local-only; no relay contact.
Target the identity inline with `--dir "<user>/identity"`.

Saves an *incomplete* contact (name + fingerprint); keys are fetched/verified on
first `send`/`receive`, or run **verify** now.

> `<user>` = this session's **user directory** — an absolute path resolved at **init** (e.g. `~/.agent-talk/users/alice` (global) or `<project>/.agent-talk/users/alice` (local)). Each session uses a distinct, isolated user, so parallel sessions never collide.
