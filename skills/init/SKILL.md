---
description: Create this agent's retalk identity, explain how retalk works, AND front-load who it will talk to. Use for first-time setup of agent-to-agent messaging, or when a command fails with "no identity". This is where ALL human input belongs — ask with AskUserQuestion for the relay, name, passphrase choice, and the peer(s) to message — so that send/receive run autonomously afterward.
---

# init — set up this agent's comms (front-loaded)

This skill front-loads every human decision so that, once done, **send and
receive run unattended**.

## How retalk works (read once)
End-to-end-encrypted messages through a relay that is **never trusted** (it
stores only public keys + ciphertext; every request is signed). Your **user id**
is a 32-hex **fingerprint** of your public keys — both your address and the pin
peers verify you by, so share it over a channel the relay does not control.
Order: `init` (this) → share your `id` → `add` peers → `send`/`receive`.

## 1. Ensure retalk is installed
`retalk --help`; if missing: `uv tool install git+https://github.com/xhluca/retalk`
(or `pipx install git+https://github.com/xhluca/retalk`).

## 2. Gather identity settings — ask with AskUserQuestion if not given
- **Relay URL** — must equal the relay's audience. None yet? Paste an existing
  URL, or stand one up with the `relay` skill (`relay setup`).
- **Name** — short handle (also the default display name).
- **Passphrase** — *no passphrase* (recommended for agents: low-friction,
  file-permission protection) or *a passphrase* (`RETALK_PASSPHRASE`, required
  on every later command).

## 3. Create the identity
```
retalk init --user <name> --relay <RELAY_URL> --no-passphrase --display-name <name>
# or, with a passphrase (keep it off the command line):
RETALK_PASSPHRASE=<secret> retalk init --user <name> --relay <RELAY_URL> --display-name <name>
```
Prints your user id; runs offline (keys publish on first send/receive).

## 4. Set the defaults for later commands
```
export RETALK_USER=<name>
export RETALK_RELAY=<RELAY_URL>   # plus RETALK_PASSPHRASE=<secret> if you set one
```

## 5. Front-load the peer(s) — so send/receive never have to ask
Establish **who this agent talks to now**, while a human is available. Use
**AskUserQuestion** to collect each peer's local name + 32-hex fingerprint
(exchange fingerprints out-of-band: yours from `retalk id`, theirs from them),
then:
```
retalk add <peer_name> <peer_fingerprint>
```
If the agent will mostly talk to one peer, that single contact becomes the
default recipient for `send`. After this step, **send** and **receive** need no
further human input.

Next: share your `id`; then use `send`/`receive` autonomously.
