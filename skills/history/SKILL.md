---
description: Replay this session's locally-saved message log — the at-rest copies kept by `receive --save-messages` — oldest first, without re-contacting the relay. Use to review past conversation with a peer or audit what was received. `<user>` is this session's user directory (absolute path; from init).
---

# history — replay saved messages

```
retalk history --json --dir "<user>/identity"                # all saved messages, oldest first
retalk history --peer <peer> --json --dir "<user>/identity"  # just one sender
```

Prints the messages this identity saved with **`receive --save-messages`**, as
NDJSON (`{"id","from","name","text"}` — the same shape `receive` emits), oldest
first. Bodies are decrypted from their at-rest seal on the way out, so this needs
the passphrase if the identity is encrypted (prefix `RETALK_PASSPHRASE=<secret>`)
— but it **never contacts the relay**.

retalk keeps no log unless you opt in: pass `--save-messages` when you
**receive** (one-shot or `follow`) to build it. agent-talk's `--follow` reader
already writes a plain `<user>/inbox.ndjson` spool; `history` is the sealed,
decrypt-on-demand alternative — a durable, passphrase-protected record.

> `<user>` = this session's **user directory** — an absolute path resolved at **init** (e.g. `~/.agent-talk/users/alice` (global) or `<project>/.agent-talk/users/alice` (local)). Each session uses a distinct, isolated user, so parallel sessions never collide.
