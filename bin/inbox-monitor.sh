#!/usr/bin/env bash
# agent-talk inbox monitor (a Claude Code plugin monitor command).
#
# Streams NEW incoming retalk messages into the session: it tails the inbox
# spool that the background follower (started by the `watch` skill) appends to.
# Each new line is one message (JSON) -- that line is what Claude Code injects.
# It needs no retalk identity: it only follows a file. Diagnostics go to stderr;
# only message lines go to stdout. `tail -F` survives the spool being recreated,
# and the loop relaunches tail if it ever exits.
set -uo pipefail
SPOOL="${AGENT_TALK_SPOOL:-$HOME/.agent-talk/inbox.ndjson}"
mkdir -p "$(dirname "$SPOOL")" 2>/dev/null || true
: >> "$SPOOL" 2>/dev/null || true
while true; do
  tail -n0 -F "$SPOOL" 2>/dev/null
  sleep 1
done
