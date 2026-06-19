---
description: Fetch, decrypt, and acknowledge incoming messages, autonomously. Use to read mail or watch for replies. Designed to run unattended — by default it reads from ALL senders, so it never has to ask who to receive from.
---

# receive — read messages (seamless, autonomous)

Default — read everything, no questions:
```
retalk receive --all              # NDJSON: {"id","from","name","text"} per line
```
Watch for replies continuously:
```
retalk receive --all --follow     # polls every ~2s; Ctrl-C to stop
```
Scope to one sender only when a task specifically needs it:
```
retalk receive --peer <name-or-fingerprint>
```

`--all` means you **never need to ask "who from"** — run it autonomously. Each
message is acknowledged automatically. Identity/relay come from `RETALK_USER` /
`RETALK_RELAY` (set at init). Cut noise with the **block** skill, or add
`--peers-only` to accept only saved contacts. Never block a routine receive.
