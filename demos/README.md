# Demos

Recorded in a real Claude Code TUI against a **temporary local relay**; the
identity splash is anonymized and every keystroke is typed live (not pasted).
`.cast` files are asciinema recordings (replay with `asciinema play <file>`);
the GIFs are rendered with `agg`.

- **01-install** — loading the plugin; asked in plain language what it can do,
  the agent lists its 12 skills, with the inbox **monitor** active (`1 monitor`).
- **02-usage** — a natural conversation: "alice" asks the agent to set her up on
  agent-talk, the agent runs `init` and asks for her friend "bob"'s id, she
  answers, the agent `send`s the message, and on the next turn `receive`s bob's
  reply — a full end-to-end round-trip.
