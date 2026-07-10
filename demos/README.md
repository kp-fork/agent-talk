# Demos

One live two-agent conversation, shown from both sides: **04-alice** and
**05-bob** were recorded simultaneously in two Claude Code sessions (two docker
sandboxes talking through a **temporary local relay**). Both recordings are
trimmed to start right at the messaging beat — the identity/setup preamble is
cut — and play at **2× speed**, with long "agent is working" spinner
stretches time-compressed. The two casts have the exact same duration, so the
GIFs stay in sync when shown side by side. `.cast` files are asciinema
recordings (replay with `asciinema play <file>`); the GIFs are rendered with
`agg`.

- **04-alice** — Alice's side. Opens as her agent, already resumed as `alice`,
  says "Now let's send the message": it sends bob "are we still on for the
  10am demo?" over the relay, renders the outgoing 📤 transcript, and starts a
  background listener. Bob's reply then **wakes the session by itself** (the
  monitor fires) and lands as a both-sides 📤/📥 chat transcript — "still on —
  10am sharp, the relay is ready. bring coffee."
- **05-bob** — Bob's side of the same run. Opens as the listener's monitor
  event fires: alice's message surfaces on its own as a 📥 transcript, the
  agent asks "Want me to reply, or do you want to answer this one yourself?",
  the user dictates the reply in plain language, and the agent sends it —
  closing the round trip shown in 04-alice.
