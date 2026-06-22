---
description: List the senders currently blocked for this identity. Use to review or audit your block list.
---

# blocked — list blocked senders

```
retalk blocked --json --dir "$HOME/.agent-talk/users/<user>/identity"   # {"fingerprint","name"} per line
```

Local-only; no relay contact. Manage entries with **block** / **unblock**.
Target the identity inline with `--dir "$HOME/.agent-talk/users/<user>/identity"`.

> `<user>` = this session's user name, chosen at **init**. Each session uses a distinct, fully isolated user (own store, contacts, inbox), so parallel sessions never collide.
