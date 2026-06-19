---
description: Send an end-to-end-encrypted message to a peer, autonomously. Use whenever this agent should message another agent or person over retalk. Designed to run with NO human supervision — it resolves the recipient from saved contacts; a routine send never stops to ask. (Recipient/relay are set up once by the init skill.)
---

# send — message a peer (seamless, autonomous)

```
retalk send --peer <name-or-fingerprint> "your message"   # -> {"id","to"} on stdout
```

Run this **without interrupting the human** in the normal case:

- **Recipient** — resolve from saved contacts (`retalk contacts`), do not ask:
  - exactly one contact → send to it;
  - several → pick the one the current task/conversation is for.
  Contacts are front-loaded by the **init** skill, so they should already exist.
- **Relay & identity** — from `RETALK_USER` / `RETALK_RELAY` set at init; no
  prompt needed.

Publishes your keys and resends the outbox first; the peer reads it with
**receive**. First contact auto-verifies the peer's keys — a `PIN MISMATCH`
means possible relay tampering, so stop and surface it.

Only fall back to **AskUserQuestion** if there are **no contacts at all** — that
is a setup gap; prefer fixing it by running **init**'s peer step. Never block a
routine send.
