#!/usr/bin/env bash
# agent-talk inbox monitor (a Claude Code plugin monitor command).
#
# Pushes THIS session's user's incoming messages into the session: it resolves
# the user from the session->user map that `init` writes
# ($HOME/.agent-talk/by-session/<session-id>), then tails that user's spool.
# $1 is ${CLAUDE_SESSION_ID}; if it did not substitute or is empty, it idles
# (push off — pull via the `receive` skill still works). Diagnostics to stderr;
# only message lines go to stdout.
set -uo pipefail
sid="${1:-}"
case "$sid" in ""|*'${'*) exec tail -f /dev/null;; esac      # no session id -> no push
sid="$(printf '%s' "$sid" | tr -c 'A-Za-z0-9._-' '_')"
map="$HOME/.agent-talk/by-session/$sid"
while [ ! -f "$map" ]; do sleep 2; done                      # init writes it after we start
SPOOL="$HOME/.agent-talk/users/$(cat "$map")/inbox.ndjson"
mkdir -p "$(dirname "$SPOOL")" 2>/dev/null || true
: >> "$SPOOL" 2>/dev/null || true
while true; do tail -n0 -F "$SPOOL" 2>/dev/null; sleep 1; done
