---
description: Block a sender so their messages are dropped before decryption (and the relay is told to refuse their resends). Use to stop unwanted or abusive mail from a specific sender. If the sender is not specified, ask with AskUserQuestion.
---

# block — drop a sender

```
retalk block <name-or-fingerprint>
```

Their incoming mail is dropped during `receive` **before any decryption**, so a
blocked sender can never even consume one of your one-time keys; the relay is
also told to refuse their resends (a signed negative-ack). Local to this
identity — never sent to the peer. If the user did not name a sender, use
**AskUserQuestion** (offer the current **contacts** / recent senders).

See also **unblock** and **blocked**. (agent-talk receives only from designated
peers, so a blocked sender is already excluded from reads; block additionally
tells the relay to refuse that sender's resends.)
