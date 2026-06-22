---
description: Print a saved contact as a shareable JSON Contact card (fingerprint, recommended nickname, and keys if verified). Use to hand a contact to someone out-of-band, or to copy a contact between your own identities. `<user>` is this session's user directory (absolute path; from init).
---

# show — a saved contact as a shareable card

```
retalk show <contact> --dir "<user>/identity"
retalk show <contact> --as <nickname> --dir "<user>/identity"
```

Prints a JSON **Contact card** — `{fingerprint, name, identity_key, signing_key}`
(the key fields are present only once you've verified that contact) — for a saved
peer (`<contact>` = a saved name or 32-hex id). `--as` overrides the recommended
nickname. The card is **not a secret** (the keys are public; the fingerprint pins
them). Local-only; no relay, no passphrase.

Hand the card to someone out-of-band, or `share` it over the relay; the receiver
saves it with `import`.

> `<user>` = this session's user directory (absolute path; resolved at **init**).
