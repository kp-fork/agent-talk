---
description: List the senders currently blocked for this identity. Use to review or audit your block list.
---

# blocked — list blocked senders

```
retalk blocked --json --dir "<user>/identity"   # {"fingerprint","name"} per line
```

Local-only; no relay contact. Manage entries with **block** / **unblock**.
Target the identity inline with `--dir "<user>/identity"`.

> `<user>` = this session's **user directory** — an absolute path resolved at **init** (e.g. `~/.agent-talk/users/alice` (global) or `<project>/.agent-talk/users/alice` (local)). Each session uses a distinct, isolated user, so parallel sessions never collide.
