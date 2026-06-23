# Demos

Recorded in a real Claude Code TUI against a **temporary local relay**; the
identity splash is anonymized and every keystroke is typed live (not pasted).
`.cast` files are asciinema recordings (replay with `asciinema play <file>`);
the GIFs are rendered with `agg`.

- **01-install** — loading the plugin; asked in plain language what it can do,
  the agent lists the plugin skills, with the inbox **monitor** active
  (`1 monitor`).
- **02-usage** — a natural conversation: "alice" asks the agent to set her up on
  agent-talk, the agent runs `init` and asks for her friend "bob"'s id, she
  answers, the agent `send`s the message, and on the next turn `receive`s bob's
  reply — a full end-to-end round-trip.
- **03-askuserquestion** — the fuller guided setup path: `init` gathers relay,
  user, and peer details through questions, Alice sends Bob a message, Bob's
  reply comes back, and the agent offers to start a live listener.
- **04-alice** — Alice's side of a two-session run. She is already configured,
  resolves Bob from contacts, sends him a message, and checks for the reply.
- **05-bob** — Bob's side of the same two-session run. He starts as a separate
  user, follows Alice's messages, receives Alice's note, and sends a reply.
