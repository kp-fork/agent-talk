---
description: Record and pin a saved peer's public keys (explicit first-contact verification). Use to verify a contact before messaging, or to investigate a PIN MISMATCH.
---

# verify — pin a peer's keys

```
retalk verify <peer>                                   # fetch keys from the relay, check + record
retalk verify <peer> --identity-key K --signing-key S  # record keys obtained out-of-band
```

Turns an incomplete contact (name + fingerprint, from **add**) into a verified
one: keys are checked against the saved fingerprint and, on success, recorded
and pinned (shown by **contacts**). If they do not hash to the fingerprint it
refuses with **PIN MISMATCH** and records nothing — treat that as possible relay
tampering and stop. Optional: `send`/`receive` verify on the fly. The peer must
exist via **add**; fetching from the relay needs your passphrase.
