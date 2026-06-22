---
description: Stop blocking a previously blocked sender so their messages are delivered again. Use to re-allow someone you had blocked.
---

# unblock — re-allow a sender

```
retalk unblock <name-or-fingerprint> --dir "<user>/identity"
```

A no-op if they aren't blocked. Use **blocked** to see who is. Target the
identity inline with `--dir "<user>/identity"`.

> `<user>` = this session's **user directory** — an absolute path resolved at **init** (e.g. `~/.agent-talk/users/alice` (global) or `<project>/.agent-talk/users/alice` (local)). Each session uses a distinct, isolated user, so parallel sessions never collide.
