---
description: Set up THIS session's retalk user (a REQUIRED, distinct name), explain how retalk works, and front-load who it talks to and receives from. Use for first-time setup, or when a command fails with "no identity". agent-talk has no default user — every session picks a user name with AskUserQuestion (distinct per parallel session so they never collide), then all human input (relay, passphrase, peers, receive source) is gathered here so send/receive run autonomously afterward.
---

# init — set up this session's user (front-loaded)

agent-talk has **no default user**: each session runs as a *named* user, fully
isolated under `$HOME/.agent-talk/users/<user>/`, so multiple sessions in
parallel never collide. Front-load every human decision here so that afterward
**send and receive run unattended**.

## How retalk works (read once)
End-to-end-encrypted messages through a relay that is **never trusted** (stores
only public keys + ciphertext; every request is signed). Your **user id** is a
32-hex **fingerprint** of your public keys — both your address and the pin peers
verify you by; share it over a channel the relay does not control.

## 1. Ensure retalk is installed
`retalk --help`; if missing: `uv tool install git+https://github.com/xhluca/retalk`
(or `pipx install git+https://github.com/xhluca/retalk`).

## 2. Choose this session's USER NAME (required) — AskUserQuestion
Pick a short user name for THIS session (e.g. `alice`). It is `<user>` everywhere
below; this session's home is `$HOME/.agent-talk/users/<user>/`.
- **Distinct per parallel session** — two live sessions must not share a name or
  their inboxes/identities collide.
- Reusing a name later = reusing that same identity (stable fingerprint).

Collision guard — if a follower is already live for that name, it's likely in use
by another session, so pick a different one:
```
for f in "$HOME/.agent-talk/users/<user>"/follow.*.pid; do
  [ -e "$f" ] && kill -0 "$(cat "$f")" 2>/dev/null && echo "WARN: user <user> looks active in another session — choose a different name"
done
```

## 3. Gather relay + passphrase — AskUserQuestion if not given
- **Relay URL** — must equal the relay's audience. None yet? use the `relay`
  skill (`relay setup`).
- **Passphrase** — *no passphrase* (recommended) or *a passphrase* (then prefix
  every later command `RETALK_PASSPHRASE=<secret>`).

## 4. Create the identity (under this user's dir)
```
retalk init --dir "$HOME/.agent-talk/users/<user>/identity" --relay <RELAY_URL> --no-passphrase --display-name <user>
# with a passphrase:
RETALK_PASSPHRASE=<secret> retalk init --dir "$HOME/.agent-talk/users/<user>/identity" --relay <RELAY_URL> --display-name <user>
```
The relay is saved in this store; later commands only pass
`--dir "$HOME/.agent-talk/users/<user>/identity"` (no env to set — it would not
persist between commands).

## 5. Register this session's user (enables real-time push)
So the inbox monitor knows which user this session is, record the mapping:
```
mkdir -p "$HOME/.agent-talk/by-session"
echo "<user>" > "$HOME/.agent-talk/by-session/${CLAUDE_SESSION_ID}"
```

## 6. Front-load the peer(s)
**AskUserQuestion** for each peer's local name + 32-hex fingerprint (exchange
out-of-band: yours from `retalk id`, theirs from them), then:
```
retalk add <peer_name> <peer_fingerprint> --dir "$HOME/.agent-talk/users/<user>/identity"
```

## 7. Choose who this user RECEIVES from (safety — required)
agent-talk **never** drains the whole mailbox; it reads only from designated
senders. **AskUserQuestion**: a specific peer (usual) or all saved contacts.
```
echo "<peer-name-or-fingerprint>" > "$HOME/.agent-talk/users/<user>/receive-from"
# or contact-list mode:  echo "*contacts*" > "$HOME/.agent-talk/users/<user>/receive-from"
```

From now on **this session is user `<user>`** — target it with
`--dir "$HOME/.agent-talk/users/<user>/identity"` on every command. Next: share
your `id`; then use `send` / `receive` autonomously.
