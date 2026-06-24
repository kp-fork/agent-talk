---
description: Save a peer's retalk user id under a local name so you can message them by name. Use when you have a peer's fingerprint to record. If the name or fingerprint is missing, ask with AskUserQuestion.
---

# add — save a peer

```
retalk add <name> <fingerprint> --dir "<user>/identity"
```

`<name>` is a local label (yours alone; the peer never learns it); `<fingerprint>`
is the peer's 32-hex id, obtained out-of-band. If both aren't given, use
**AskUserQuestion**. Re-adding a name overwrites it. Local-only; no relay contact.
Target the identity inline with `--dir "<user>/identity"`.

Saves an *incomplete* contact (name + fingerprint); keys are fetched/verified on
first `send`/`receive`, or run **verify** now.

## After adding: share your address back (off-band)
A peer you `add` still needs YOUR address to reach you. Hand them a paste-ready
invite — retalk builds it from your own card (relay + fingerprint + suggested name):
```
retalk id --invite-message --as <your-name> --dir "<user>/identity"
```
Or share your identity as JSON for them to **import**:
`retalk id --card --dir "<user>/identity"`. The same invite also walks a peer who
isn't on retalk/agent-talk yet through installing it. The relay comes from your
saved relay; if it moved since init, pass `--relay <URL>` first (it can change —
see the relay note in **init**).

> `<user>` = this session's **user directory** — an absolute path resolved at **init** (e.g. `~/.agent-talk/users/alice` (global) or `<project>/.agent-talk/users/alice` (local)). Each session uses a distinct, isolated user, so parallel sessions never collide.
