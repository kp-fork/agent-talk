---
description: Start/stop a background receiver so incoming retalk messages are PUSHED into this session as they arrive (no polling). Use to make this agent reachable in real time. Invoke as `watch start`, `watch stop`, or `watch` (status + recent mail). Pairs with the plugin's inbox monitor.
---

# watch — background receive + push (`watch <action>`)

**How push works:** the plugin ships a **monitor** that automatically streams new
incoming messages into this session — but only while a background **follower** is
feeding the inbox spool. This skill manages that follower. Read the action from
`$ARGUMENTS`: `start`, `stop`, or (default) status.

Requires an identity (run **init** first) with `RETALK_USER` / `RETALK_RELAY`
exported (and `RETALK_PASSPHRASE` too if the identity is encrypted) — the
follower inherits them. Spool: `$HOME/.agent-talk/inbox.ndjson` (the durable
record of delivered messages).

## start
Begins a single, self-restarting follower that drains *all* senders into the
spool; the monitor then pushes each new line into the session. Idempotent — it
won't start a second follower. It keeps running in the background **after this
session ends** (that is what keeps messages arriving), until `watch stop`.
```
D="$HOME/.agent-talk"; mkdir -p "$D"
if [ -f "$D/follower.pid" ] && kill -0 "$(cat "$D/follower.pid")" 2>/dev/null; then
  echo "follower already running (pid $(cat "$D/follower.pid"))"
else
  nohup bash -c 'while true; do retalk receive --all --follow >> "$HOME/.agent-talk/inbox.ndjson" 2>> "$HOME/.agent-talk/follower.err"; sleep 2; done' >/dev/null 2>&1 &
  echo $! > "$D/follower.pid"
  echo "follower started (pid $(cat "$D/follower.pid"))"
fi
```

## stop
Kill the loop first (so it doesn't relaunch retalk), then the follower itself:
```
D="$HOME/.agent-talk"
[ -f "$D/follower.pid" ] && kill "$(cat "$D/follower.pid")" 2>/dev/null
pkill -f 'retalk receive --all --follow' 2>/dev/null
rm -f "$D/follower.pid"; echo "follower stopped"
```

## status (no arg)
```
D="$HOME/.agent-talk"
if [ -f "$D/follower.pid" ] && kill -0 "$(cat "$D/follower.pid")" 2>/dev/null; then
  echo "follower: running (pid $(cat "$D/follower.pid"))"
else
  echo "follower: not running — run \`watch start\`"
fi
echo "--- recent messages (spool tail) ---"
tail -n 20 "$D/inbox.ndjson" 2>/dev/null || echo "(none yet)"
```

## Notes
- The **spool is the source of truth.** Push (the monitor) is best-effort and
  experimental, and runs only in interactive CLI sessions — if it ever misses
  one, `watch` (status) and the spool still show every delivered message, so
  nothing is lost.
- Don't also run a bare `receive --all` while the follower is up (two `--all`
  readers split the mail) — read the **spool** instead.

## Always-on (survive reboots)
For a relay that's always drained, run the follower under your init system
instead of `watch start` — e.g. a systemd **user** service:
```
[Service]
Environment=RETALK_USER=<name> RETALK_RELAY=<url>
ExecStart=/usr/bin/env retalk receive --all --follow
StandardOutput=append:%h/.agent-talk/inbox.ndjson
Restart=always
```
