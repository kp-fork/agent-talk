---
description: Print this agent's retalk user id (fingerprint) to share with peers, or to confirm which identity is active. Use whenever you need your own retalk address/fingerprint.
---

# id — your address (fingerprint)

```
retalk id            # the 32-hex fingerprint
retalk id --json     # {"fingerprint","identity_key","name"}
```

The fingerprint is the sha256 of your public keys: it is your **address** and
your **pin** in one, contains no secret, and is safe to post publicly. **Share
it out-of-band** (chat, email, in person) with anyone who should reach you, and
ask them for theirs.

Needs the identity to exist (run **init** first) and its passphrase, if any.
Does not contact the relay.

Next: the peer runs **add** with your fingerprint; you run **add** with theirs.
