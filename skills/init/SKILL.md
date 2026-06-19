---
description: Create this agent's retalk identity, explain how retalk works, AND front-load who it talks to and receives from. Use for first-time setup, or when a command fails with "no identity". All human input belongs here — ask with AskUserQuestion for the relay, name, passphrase, the peer(s) to message, and which sender(s) to receive from — so send/receive run autonomously and safely afterward.
---

# init — set up this agent's comms (front-loaded)

Front-loads every human decision so that afterward **send and receive run
unattended**.

## How retalk works (read once)
End-to-end-encrypted messages through a relay that is **never trusted** (stores
only public keys + ciphertext; every request is signed). Your **user id** is a
32-hex **fingerprint** of your public keys — both your address and the pin peers
verify you by; share it over a channel the relay does not control. Order:
`init` (this) → share your `id` → `add` peers → `send`/`receive`.

## 1. Ensure retalk is installed
`retalk --help`; if missing: `uv tool install git+https://github.com/xhluca/retalk`
(or `pipx install git+https://github.com/xhluca/retalk`).

## 2. Gather identity settings — ask with AskUserQuestion if not given
- **Relay URL** — must equal the relay's audience. None yet? Paste an existing
  URL, or stand one up with the `relay` skill (`relay setup`).
- **Name** — short handle (also the default display name).
- **Passphrase** — *no passphrase* (recommended for agents) or *a passphrase*
  (`RETALK_PASSPHRASE`, required on every later command).

## 3. Create the identity
```
retalk init --user <name> --relay <RELAY_URL> --no-passphrase --display-name <name>
# or, with a passphrase (keep it off the command line):
RETALK_PASSPHRASE=<secret> retalk init --user <name> --relay <RELAY_URL> --display-name <name>
```

## 4. Set the defaults for later commands
```
export RETALK_USER=<name>
export RETALK_RELAY=<RELAY_URL>   # plus RETALK_PASSPHRASE=<secret> if you set one
```

## 5. Front-load the peer(s)
Establish **who this agent talks to**, now, while a human is available. Use
**AskUserQuestion** to collect each peer's local name + 32-hex fingerprint
(exchange out-of-band: yours from `retalk id`, theirs from them), then:
```
retalk add <peer_name> <peer_fingerprint>
```

## 6. Choose who this agent RECEIVES from (safety — required)
agent-talk **never** drains the whole mailbox (`receive --all`); it only reads
from the sender(s) you designate here, so it never processes mail from anyone it
was not set up to talk to. Use **AskUserQuestion**:
- **A specific peer** (recommended — the usual case): one of the peers above.
- **All saved contacts**: read from every peer in your contact list.
Record the choice:
```
mkdir -p "$HOME/.agent-talk"
echo "<peer-name-or-fingerprint>" > "$HOME/.agent-talk/receive-from"   # individual
# or, for contact-list mode:
# echo "*contacts*" > "$HOME/.agent-talk/receive-from"
```

After steps 5–6, **send** and **receive** need no further human input — and
`receive` only ever pulls from your designated sender(s).

Next: share your `id`; then use `send` / `receive` autonomously.
