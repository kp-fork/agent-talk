---
description: Block a sender so their messages are dropped before decryption (and the relay is told to refuse their resends). Use to stop unwanted or abusive mail from a specific sender. If the sender is not specified, ask with AskUserQuestion.
---

# block — drop a sender

```
retalk block <name-or-fingerprint> --dir "$HOME/.agent-talk/users/<user>/identity"
```

Their incoming mail is dropped during `receive` **before any decryption** (so
they can't consume a one-time key), and the relay is told to refuse their
resends. Local to this identity. If no sender was named, use **AskUserQuestion**.
Target the identity inline with `--dir "$HOME/.agent-talk/users/<user>/identity"`.

See also **unblock** and **blocked**. (agent-talk receives only from designated
peers, so a blocked sender is already excluded from reads; block additionally
tells the relay to refuse that sender's resends.)

> `<user>` = this session's user name, chosen at **init**. Each session uses a distinct, fully isolated user (own store, contacts, inbox), so parallel sessions never collide.
