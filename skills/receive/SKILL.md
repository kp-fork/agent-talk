---
description: Read incoming retalk messages from this agent's DESIGNATED sender(s) — one-shot, or as a background --follow reader that PUSHES new messages into the session in real time. agent-talk only ever receives from specific saved peers, never the whole mailbox (safety). Use to check mail or to stay reachable.
---

# receive — read messages (`receive`, or `receive follow …`)

**Safety rule (mandatory):** agent-talk **never** runs `retalk receive --all`.
It only reads from **specific saved peers**, so this agent never pulls, acks, or
processes mail from senders it was not set up to talk to. Who it receives from is
chosen during **init** and recorded in `$HOME/.agent-talk/receive-from`:
- a single peer name/fingerprint (the usual case), or
- the token `*contacts*` (read from every saved peer in `retalk contacts`).

## Resolve the designated source(s)
```
SRC="$(cat "$HOME/.agent-talk/receive-from" 2>/dev/null)"
# SRC is a peer (individual mode) or "*contacts*" (loop saved peers).
# Empty? run the init skill to choose — never fall back to --all.
```

## One-shot read
Individual (the usual case):
```
retalk receive --peer <peer>     # NDJSON: {"id","from","name","text"}; auto-acked
```
Contact-list mode — loop saved peers (still per-peer, never `--all`; needs jq):
```
retalk contacts --json | jq -r .fingerprint | while read -r fp; do
  [ -n "$fp" ] && retalk receive --peer "$fp"
done
```
Identity/relay come from `RETALK_USER` / `RETALK_RELAY` (set at init).

## Background follow — push, real-time (per peer)
Get a designated peer's new messages **pushed into the session as they arrive**
(no polling): a background `--follow` reader **scoped to that peer**; the
plugin's inbox monitor streams each new line in.

`receive follow <peer>` — start (idempotent; survives sessions until stopped):
```
P=<peer>; D="$HOME/.agent-talk"; mkdir -p "$D"; PID="$D/follow.$P.pid"
if [ -f "$PID" ] && kill -0 "$(cat "$PID")" 2>/dev/null; then
  echo "already following $P (pid $(cat "$PID"))"
else
  nohup env RP="$P" bash -c 'while true; do retalk receive --peer "$RP" --follow >> "$HOME/.agent-talk/inbox.ndjson" 2>> "$HOME/.agent-talk/follow.err"; sleep 2; done' >/dev/null 2>&1 &
  echo $! > "$PID"; echo "following $P (pid $(cat "$PID"))"
fi
```
(Contact-list mode: start one such follower per saved peer.)

`receive follow stop <peer>`:
```
P=<peer>; D="$HOME/.agent-talk"
[ -f "$D/follow.$P.pid" ] && kill "$(cat "$D/follow.$P.pid")" 2>/dev/null
pkill -f "retalk receive --peer $P --follow" 2>/dev/null
rm -f "$D/follow.$P.pid"; echo "stopped following $P"
```

`receive follow status`:
```
D="$HOME/.agent-talk"
for f in "$D"/follow.*.pid; do [ -e "$f" ] || continue
  p=$(basename "$f" .pid); p=${p#follow.}
  kill -0 "$(cat "$f")" 2>/dev/null && echo "following: $p (pid $(cat "$f"))"; done
echo "--- recent messages (spool) ---"
tail -n 20 "$D/inbox.ndjson" 2>/dev/null || echo "(none yet)"
```

The spool (`$HOME/.agent-talk/inbox.ndjson`) is the durable record; push (the
monitor) is best-effort + interactive-CLI only, so reading the spool always shows
every delivered message.
