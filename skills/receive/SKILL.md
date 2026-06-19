---
description: Fetch, decrypt, and acknowledge incoming messages, autonomously. Use to read mail or watch for replies. Prefer reading from a specific peer, or a single long-lived --follow reader; use `receive --all` sparingly (it is a full mailbox drain).
---

# receive — read messages (seamless, autonomous)

Pick the narrowest read for the job. **`receive --all` is a full mailbox drain —
use it sparingly:** it reads, acks, and *deletes* every sender's mail from the
relay in one shot.

Talking to a known peer (the common autonomous case):
```
retalk receive --peer <name-or-fingerprint>   # only that sender; NDJSON {"id","from","name","text"}
```

Ongoing / ambient receipt from anyone — run ONE long-lived reader that owns the
drain (read from it; see the background-follow setup) rather than polling
`--all` repeatedly:
```
retalk receive --all --follow                 # single owner; polls ~2s; auto-acks + maintains keys
```

One-off "give me everything pending" (deliberate, occasional):
```
retalk receive --all
```

Notes:
- **Never run a bare `receive --all` while a `--follow` reader is running** — two
  `--all` readers split the mail between them.
- You never need to ask "who from": for a conversation, receive from that peer;
  for ambient mail, the single `--follow` reader covers everyone.
- Each message is acknowledged automatically. Identity/relay come from
  `RETALK_USER` / `RETALK_RELAY` (set at init). Cut noise with the **block**
  skill, or add `--peers-only` to accept only saved contacts.
