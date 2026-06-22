---
description: Read incoming retalk messages from this session's user's DESIGNATED sender(s) — one-shot, or as a background --follow reader that PUSHES new messages into the session in real time. agent-talk only ever receives from specific saved peers, never the whole mailbox (safety). `<user>` is this session's user name (from init). Use to check mail or stay reachable.
---

# receive — read messages (`receive`, or `receive follow …`)

`<user>` = this session's user name (chosen at **init**). Target it on every
command with `--dir "$HOME/.agent-talk/users/<user>/identity"`; add
`RETALK_PASSPHRASE=<secret>` if the identity is encrypted.

**Safety rule (mandatory):** never run `retalk receive --all`. Read only from
**specific saved peers**. The source is chosen at **init** and stored in
`$HOME/.agent-talk/users/<user>/receive-from` (a peer, or `*contacts*`).

## One-shot read
Individual (the usual case):
```
retalk receive --peer <peer> --dir "$HOME/.agent-talk/users/<user>/identity"
# NDJSON: {"id","from","name","text"}; auto-acked
```
Contact-list mode — loop saved peers (per-peer, never `--all`; needs jq):
```
retalk contacts --json --dir "$HOME/.agent-talk/users/<user>/identity" | jq -r .fingerprint | while read -r fp; do
  [ -n "$fp" ] && retalk receive --peer "$fp" --dir "$HOME/.agent-talk/users/<user>/identity"
done
```

## Background follow — push, real-time (per peer)
A background `--follow` reader scoped to one peer, writing this user's spool; the
plugin's inbox monitor streams each new line into the session.

`receive follow <peer>` — start (idempotent; survives sessions until stopped):
```
P=<peer>; D="$HOME/.agent-talk/users/<user>"; mkdir -p "$D"; PID="$D/follow.$P.pid"
if [ -f "$PID" ] && kill -0 "$(cat "$PID")" 2>/dev/null; then
  echo "already following $P (pid $(cat "$PID"))"
else
  nohup env RP="$P" UD="$D" bash -c 'while true; do retalk receive --peer "$RP" --follow --dir "$UD/identity" >> "$UD/inbox.ndjson" 2>> "$UD/follow.err"; sleep 2; done' >/dev/null 2>&1 &
  echo $! > "$PID"; echo "following $P (pid $(cat "$PID"))"
fi
```
`receive follow stop <peer>`:
```
P=<peer>; D="$HOME/.agent-talk/users/<user>"
[ -f "$D/follow.$P.pid" ] && kill "$(cat "$D/follow.$P.pid")" 2>/dev/null
pkill -f "receive --peer $P --follow --dir $D/identity" 2>/dev/null
rm -f "$D/follow.$P.pid"; echo "stopped following $P"
```
`receive follow status`:
```
D="$HOME/.agent-talk/users/<user>"
for f in "$D"/follow.*.pid; do [ -e "$f" ] || continue
  p=$(basename "$f" .pid); p=${p#follow.}
  kill -0 "$(cat "$f")" 2>/dev/null && echo "following: $p (pid $(cat "$f"))"; done
echo "--- recent messages (spool) ---"
tail -n 20 "$D/inbox.ndjson" 2>/dev/null || echo "(none yet)"
```

The spool (`$HOME/.agent-talk/users/<user>/inbox.ndjson`) is the durable record;
push (the monitor) is best-effort + interactive-CLI only, so reading the spool
always shows every delivered message.

## Always-on (survive reboots)
A systemd user service running the scoped follower (the store holds the relay):
```
[Service]
ExecStart=/usr/bin/env retalk receive --peer <peer> --follow --dir %h/.agent-talk/users/<user>/identity
StandardOutput=append:%h/.agent-talk/users/<user>/inbox.ndjson
Restart=always
# Environment=RETALK_PASSPHRASE=<secret>   # only if the identity is encrypted
```
