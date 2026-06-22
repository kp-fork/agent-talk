# agent-talk tests

`python -m unittest discover -s tests`

- **test_plugin.py** — static checks: manifests are valid JSON, every skill has
  frontmatter/description, expected skills present, `receive --all` only appears
  as a safety note, `bin/*.sh` pass `bash -n`. (no deps)
- **test_monitor.py** — `bin/inbox-monitor.sh` resolves this session's user from
  the session->user map and pushes new spool lines; idles safely without a
  session id. (no deps)
- **test_roundtrip.py** — a scoped `retalk receive --peer X --follow` follower
  feeds the per-user spool, against a local relay. **Opt-in:** runs only when `AGENT_TALK_E2E=1` and `retalk` is on PATH
  (so it stays out of CI, which guards the plugin's own artifacts). Run locally
  with `AGENT_TALK_E2E=1 python -m unittest discover -s tests`.

Not covered here (needs an interactive Claude Code session, not CI): plugin
loading, monitor injection, AskUserQuestion flows, `${CLAUDE_SESSION_ID}`
substitution.
