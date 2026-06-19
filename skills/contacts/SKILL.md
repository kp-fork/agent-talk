---
description: List saved peers (your address book) and whether each is verified. Use to see who you can message, resolve who to send to, or check a contact's status.
---

# contacts — list saved peers

```
retalk contacts          # NAME<tab>FINGERPRINT<tab>STATUS (verified/unverified)
retalk contacts --json   # one {"name","fingerprint","identity_key","signing_key","verified"} per line
```

Local-only (names never leave your machine; no relay contact). Use this to
resolve **who to send to** without asking a human. Empty output means no peers
yet — run **add** (or **init**'s peer step).
