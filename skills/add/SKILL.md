---
description: Save a peer's retalk user id under a local name so you can message them by name. Use when you have a peer's fingerprint to record. If the name or fingerprint is missing, ask with AskUserQuestion.
---

# add — save a peer

```
retalk add <name> <fingerprint>
```

- `<name>`: a short local label (e.g. `bob`) — yours alone; it never leaves your
  machine and the peer never learns it.
- `<fingerprint>`: the peer's 32-hex user id, obtained out-of-band (they run the
  **id** skill).

If the user has not supplied both, use **AskUserQuestion** to get the local name
and the fingerprint (which must be 32 hex characters). Re-adding a name
overwrites it. Local-only: no passphrase, no relay contact.

This stores an *incomplete* contact (name + fingerprint). The peer's keys are
fetched and verified automatically on your first `send`/`receive`, or run the
**verify** skill now to record and pin them.

Next: **send** a message, or **verify** the peer first.
