# agent-talk

A [Claude Code](https://code.claude.com/docs/) **plugin** that teaches an agent
to run **end-to-end-encrypted** agent-to-agent communications with the
[retalk](https://github.com/xhluca/retalk) CLI — **one skill per retalk
command**, plus a relay skill. No MCP server: the agent runs `retalk …` via the
Bash tool. All crypto is client-side; the relay only ever sees ciphertext.

## Install

```
/plugin marketplace add xhluca/agent-talk
/plugin install agent-talk@agent-talk
```

The `init` skill installs retalk on first use if it isn't already present.

## Users (one per session, two scopes)

agent-talk has **no default user**. Each session runs as one user, fully
isolated (own keys, contacts, inbox, followers). The agent manages two scopes —
nothing for you to configure:

- **global** `~/.agent-talk/users/<name>/`
- **local** `<project-root>/.agent-talk/users/<name>/` (git toplevel, else cwd)

At `init` the agent lists existing users from **both** scopes and lets you
**reuse** one or **create** a new one (default scope: local if `./.agent-talk`
exists, else global; creating locally also adds `.agent-talk/` to `.gitignore`).
Pick **distinct users for parallel sessions** so they never collide (a
live-follower guard warns if one is already in use). Every command targets the
session's user by its **absolute dir** inline (`--dir "<userdir>/identity"`) —
Claude Code starts a fresh shell per Bash call, so env vars like `RETALK_USER`
wouldn't carry over.

## Skills

Client skills mirror the retalk subcommands 1:1:

| Skill | Does |
|---|---|
| `init` | pick or create this session's user (global or local scope) + front-load relay / passphrase / peers |
| `id` | print your fingerprint to share out-of-band |
| `add`, `verify`, `contacts` | manage peers (the address book) |
| `show`, `share`, `import` | hand a saved contact (nickname + keys) to someone, and save ones shared with you — instead of retyping a fingerprint |
| `send`, `receive` | message peers — built to run **autonomously** (see below) |
| `sync` | reconcile / retry stuck sends (cron-friendly) |
| `block`, `unblock`, `blocked` | drop / re-allow unwanted senders |

Server skill:

| Skill | Does |
|---|---|
| `relay` | `relay setup\|ping\|stop\|delete`; AskUserQuestion picks **Local / Cloudflare / Hugging Face / GCP**. Host steps in `skills/relay/{cloudflare,huggingface,gcp}.md`. |

## Designed for autonomy

Setup is **front-loaded**: `init` asks (via AskUserQuestion) for this session's user, the relay, the **peer(s)**, and **which sender(s) to receive from**, up front
while a human is around. After that, `send` resolves the recipient from saved
contacts and `receive` reads only from your designated sender(s) — **never the
whole mailbox** (`receive --all` is disallowed, for safety) — so routine
messaging runs with no human in the loop.

## Real-time receive (push)

`receive follow <peer>` runs a background reader (`retalk receive --peer <peer>
--follow`, scoped — never `--all`) that appends that peer's messages to the
user's durable spool (`<userdir>/inbox.ndjson`). The plugin's
**monitor** (`monitors/monitors.json` → `bin/inbox-monitor.sh`) resolves this
session's user from the session->user map that `init` writes, tails that user's
spool, and pushes each new message into the session as it arrives — no polling.
The spool is the source of truth, so if push misses one (monitors are
experimental + interactive-CLI only) the agent still sees every message by
reading the spool. For always-on across reboots, run the follower under systemd
(see the `receive` skill).

## Why skills, not an MCP server

retalk is already a clean CLI with JSON/NDJSON output and the agent has Bash, so
skills that document the commands need no server or venv to install or maintain.

## Local development

```
claude --plugin-dir /path/to/agent-talk      # or: /plugin marketplace add ./agent-talk
```

## Status

MVP. Follow-ups: publish retalk to PyPI so install needs no git auth; an
optional Cloudflare-only relay path.
