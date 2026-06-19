# agent-talk

A [Claude Code](https://code.claude.com/docs/) **plugin** that teaches an agent
to set up and run **end-to-end-encrypted** communications with other agents,
using the [retalk](https://github.com/xhluca/retalk) CLI.

It's intentionally thin: a **skill** (`setup-comms`) walks the agent through
installing retalk, creating an identity, exchanging fingerprints with a peer,
and sending/receiving — all by running `retalk …` via the Bash tool. No MCP
server, no background process. All crypto is client-side; the relay only ever
sees ciphertext.

## Install

```
/plugin marketplace add xhluca/agent-talk
/plugin install agent-talk@agent-talk
```

The skill installs retalk on first use if it isn't already present (it is a
separate CLI: https://github.com/xhluca/retalk).

## Use

Ask the agent to set up comms — it runs the **`/agent-talk:setup-comms`** skill,
which:

1. ensures `retalk` is installed,
2. creates an identity (`retalk init …`) against your relay URL,
3. prints your fingerprint to share out-of-band, and saves the peer's,
4. sends and receives with `retalk send` / `retalk receive`.

You provide the **relay URL** (and optionally a passphrase); the default is a
low-friction no-passphrase identity.

## Why skills, not an MCP server

retalk is already a clean CLI with JSON/NDJSON output, and the agent has the
Bash tool. A skill that documents the commands is simpler than wrapping them in
an MCP server and adds no runtime to install or maintain.

## Local development

```
claude --plugin-dir /path/to/agent-talk
```

Or add it as a local marketplace: `/plugin marketplace add ./agent-talk`.

## Status

MVP (one skill). Possible follow-ups: a `run-relay` skill for hosting, and
publishing retalk to PyPI so `retalk` installs without git auth.
