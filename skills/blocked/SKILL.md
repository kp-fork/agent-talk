---
description: List the senders currently blocked for this identity. Use to review or audit your block list.
---

# blocked — list blocked senders

```
retalk blocked          # one fingerprint per line (with saved name, if any)
retalk blocked --json   # one {"fingerprint","name"} per line
```

Local-only; no relay contact. Manage entries with **block** / **unblock**.
