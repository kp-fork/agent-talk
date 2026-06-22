---
description: List saved peers (your address book) and whether each is verified. Use to see who you can message, resolve who to send to, or check a contact's status.
---

# contacts — list saved peers

```
retalk contacts --json --dir "<user>/identity"
# one {"name","fingerprint","identity_key","signing_key","verified"} per line
```

Local-only (no relay contact). Use it to resolve who to **send** to. Empty means
no peers yet — run **add** (or **init**'s peer step). Target the identity inline
with `--dir "<user>/identity"`.

> `<user>` = this session's **user directory** — an absolute path resolved at **init** (e.g. `~/.agent-talk/users/alice` (global) or `<project>/.agent-talk/users/alice` (local)). Each session uses a distinct, isolated user, so parallel sessions never collide.
