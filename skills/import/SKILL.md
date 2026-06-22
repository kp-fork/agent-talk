---
description: Save a contact someone shared with you (a Contact card) as a local peer. agent-talk does NOT auto-import — review staged cards and import only ones from a peer you trust. `<user>` is this session's user directory (absolute path; from init).
---

# import — save a shared contact (agent decides — be careful)

Importing adds a peer to your address book — a **trust action**. Do **not**
blanket-import. Review first, then import **selectively**, only cards from a
**designated/trusted** peer. retalk re-checks any keys against the fingerprint and
refuses a tampered card with **PIN MISMATCH** (saving nothing).

Cards that peers `share`d arrive via `receive` and are **staged** in a
contact-inbox (not yet saved as peers).

Review what's staged (imports nothing):
```
retalk import --inbox --list --json --dir "<user>/identity"
```
Import just the one you trust (optionally rename):
```
retalk import --inbox <staged-name-or-id> --dir "<user>/identity"
retalk import --inbox <staged-name-or-id> --as <nickname> --dir "<user>/identity"
```
Import a card handed to you directly (JSON argument or stdin):
```
retalk import '<card json>' --dir "<user>/identity"
```

Avoid `retalk import --inbox` with no name (it imports **all** staged cards)
unless you've reviewed them. A keyless card imports as unverified (verified on
first contact).

> `<user>` = this session's user directory (absolute path; resolved at **init**).
