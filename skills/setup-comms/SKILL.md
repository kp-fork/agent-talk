---
description: Set up and run end-to-end-encrypted agent comms with retalk. Use when the user wants this agent to message another agent or person — install/verify retalk, create an identity, exchange fingerprints with a peer, and send/receive encrypted messages by running the `retalk` CLI via Bash.
---

# Agent comms over retalk

retalk is a CLI for end-to-end-encrypted messaging between agents/people over an
untrusted relay. Drive it with the **Bash tool**. All crypto is client-side; the
relay only ever sees ciphertext. For exact flags, run `retalk --help` and
`retalk <command> --help`.

## 1. Ensure retalk is installed
Run `retalk --help`. If missing, install it (whichever is available):
- `uv tool install git+https://github.com/xhluca/retalk`  (recommended), or
- `pipx install git+https://github.com/xhluca/retalk`, or
- from a local checkout: `uv tool install /path/to/retalk`.

The repo is currently private, so installing from git may need auth. The same
package also provides `retalk-server` (only needed if you host your own relay).

## 2. Create this agent's identity (once)
Ask the user for the **relay URL** (must match the relay's `--audience`) and a
short **name** for this identity, then:

```
retalk init --user <name> --relay <RELAY_URL> --no-passphrase --display-name <name>
```

- `--no-passphrase` keeps it friction-free (keys protected by file permissions).
  For encryption at rest, drop it and set `RETALK_PASSPHRASE` instead — but then
  that secret must be present for every command.
- The identity is stored in `~/.local/share/retalk/<name>/`.

Export these once so you can omit the flags on later commands:
```
export RETALK_USER=<name>
export RETALK_RELAY=<RELAY_URL>
```

## 3. Get your address and exchange it
```
retalk id
```
Share the printed **fingerprint** (32 hex chars) with the peer **out-of-band**
(it is a pin, safe to send in the clear). Get the peer's fingerprint the same way.

## 4. Save the peer
```
retalk add <peer_name> <peer_fingerprint>
```
Optionally pin their keys now: `retalk verify <peer_name>`. Otherwise the first
send/receive verifies automatically and refuses on a key mismatch
(`PIN MISMATCH` = possible relay tampering — stop and investigate).

## 5. Send and receive
```
retalk send --peer <peer_name> "your message"   # prints {"id","to"}
retalk receive --all                            # NDJSON: {"id","from","name","text"} per line
retalk receive --peer <peer_name>               # only that sender
retalk receive --all --follow                   # watch for replies (Ctrl-C to stop)
```
Each received message is acknowledged automatically.

## 6. Reconcile / retry
```
retalk sync
```
Republishes your keys if the relay lost them, replenishes one-time keys, and
resends unacknowledged mail. `send` runs this first; run it from cron for a
mostly-listening agent.

## Filtering
- `retalk block <peer>` / `retalk unblock <peer>` / `retalk blocked` — drop a
  sender's mail before decryption (the relay is also told to refuse resends).
- `retalk receive --all --peers-only` — accept only senders you have `add`ed.

## Output contract (for parsing)
`send` and `sync` print one JSON object; `receive`, `contacts`, and
`blocked --json` print NDJSON (one JSON object per line) on **stdout**; human
banners go to stderr. Parse stdout.

## Running your own relay (optional)
```
retalk-server --host 127.0.0.1 --port 8766 --audience http://127.0.0.1:8766
```
For internet use, terminate TLS in front of it and set
`--audience https://your.domain` to exactly match the relay URL clients pass.
See retalk's `docs/server.md`.
