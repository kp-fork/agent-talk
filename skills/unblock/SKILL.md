---
description: Stop blocking a previously blocked sender so their messages are delivered again. Use to re-allow someone you had blocked.
---

# unblock — re-allow a sender

```
retalk unblock <name-or-fingerprint> --dir "$HOME/.agent-talk/users/<user>/identity"
```

A no-op if they aren't blocked. Use **blocked** to see who is. Target the
identity inline with `--dir "$HOME/.agent-talk/users/<user>/identity"`.

> `<user>` = this session's user name, chosen at **init**. Each session uses a distinct, fully isolated user (own store, contacts, inbox), so parallel sessions never collide.
