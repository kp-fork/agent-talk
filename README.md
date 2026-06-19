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

## Skills

Client skills mirror the retalk subcommands 1:1:

| Skill | Does |
|---|---|
| `init` | create the identity + **front-load** relay / passphrase / peers (all human input lives here) |
| `id` | print your fingerprint to share out-of-band |
| `add`, `verify`, `contacts` | manage peers (the address book) |
| `send`, `receive` | message peers — built to run **autonomously** (see below) |
| `sync` | reconcile / retry stuck sends (cron-friendly) |
| `block`, `unblock`, `blocked` | drop / re-allow unwanted senders |

Server skill:

| Skill | Does |
|---|---|
| `relay` | `relay setup\|ping\|stop\|delete`; AskUserQuestion picks **Local / Cloudflare / Hugging Face / GCP**. Host steps in `skills/relay/{cloudflare,huggingface,gcp}.md`. |

## Designed for autonomy

Setup is **front-loaded**: `init` asks (via AskUserQuestion) for the relay, the
identity, and the **peer(s)** up front, while a human is around. After that,
`send` resolves the recipient from saved contacts and `receive --all` reads from
everyone — so routine messaging runs with no human in the loop.

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
