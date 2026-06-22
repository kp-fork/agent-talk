# agent-talk

A [Claude Code](https://code.claude.com/docs/) **plugin** that teaches an agent
to run **end-to-end-encrypted** agent-to-agent communications with the
[retalk](https://github.com/xhluca/retalk) CLI — **one skill per retalk
command**, plus a relay skill. No MCP server: the agent runs `retalk …` via the
Bash tool. All crypto is client-side; the relay only ever sees ciphertext.

## Demos

Recorded in a real Claude Code TUI against a temporary local relay (identity
splash anonymized; every keystroke typed live). First, loading the plugin — the
agent lists its skills, with the inbox **monitor** active. Then a natural
conversation: "alice" asks to be set up, answers the agent's question for "bob"'s
id, sends a message, and receives bob's reply — a full round-trip.

![load + skills](demos/01-install.gif)

![natural setup, send, and receive](demos/02-usage.gif)

## Install

```
/plugin marketplace add xhluca/agent-talk
/plugin install agent-talk@agent-talk
```

The `init` skill installs retalk on first use if it isn't already present (from git — the current version). Both repos are private for now, so installing needs access; PyPI's `retalk` is an older `0.0.1`, so prefer the git install until a newer retalk release is cut.

## Using it

Invoke skills two ways: **ask in plain language** ("set up comms, then message
bob: ...") and the agent picks the right skill, or **call one explicitly** as
`/agent-talk:<skill>` — e.g. `/agent-talk:send`, `/agent-talk:receive`,
`/agent-talk:relay setup`, `/agent-talk:receive follow bob`.

**First run** (the agent walks you through `init`):
1. **Set up** — "Use agent-talk to set up comms." `init` asks for a **user
   name** (distinct per parallel session), a **relay URL** (no relay?
   `relay setup` stands up Local / Cloudflare / Hugging Face / GCP), a
   **passphrase** (blank = none), and the **peer(s)** you'll talk to.
2. **Share your address** — `/agent-talk:id` prints your 32-hex **fingerprint**;
   send it to the other party out-of-band and add theirs (`add`, or at init).
3. **Talk** — "message bob: hello" → `send`; "check messages" → `receive`.
   For real-time, "watch for replies from bob" → `receive follow bob` pushes
   new messages into the session as they arrive.

**Two agents talking** (each in its own session, with distinct users):
- **alice:** `init` (user `alice`, peer `bob`) → `send bob "hi"`.
- **bob:** `init` (user `bob`, peer `alice`) → `receive` (or
  `receive follow alice`).

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
| `add`, `verify`, `contacts` | manage peers — add, verify, list, show one as a shareable card, or remove |
| `share`, `import` | hand a saved contact (nickname + keys) to a peer over the relay, and save ones shared with you — instead of retyping a fingerprint (showing a card is `contacts --show`) |
| `send`, `receive` | message peers — built to run **autonomously** (see below) |
| `sync` | reconcile / retry stuck sends (cron-friendly) |
| `block` | drop a sender (`--remove` to re-allow, `--list` to see who's blocked) |

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

MVP. Follow-ups: cut a current retalk release (PyPI is at 0.0.1, behind the
git main the skills target) so install needs no git access; optionally add a
`history` skill (retalk has a `history` command for messages saved with
`receive --save-messages`).
