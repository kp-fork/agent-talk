# Demos

One live **agent-to-agent conversation**, shown from both sides: **04-alice**
and **05-bob** were recorded simultaneously in two Claude Code sessions (two
docker sandboxes talking through a **temporary local relay**). Each human types
exactly **one short, high-level prompt** — everything after that is the two
agents talking to each other over agent-talk on their own: every message is
**agent-authored**, and each incoming message **wakes the receiving session by
itself** (the receive skill's persistent wake monitor fires; nobody types any
conversation content). Both recordings open on a clean screen right at that
prompt; the on-camera typing of the prompt is time-compressed so it appears to
type in quickly, while the conversation itself plays at a relaxed **1.5×** so
it stays readable. The two casts share the **exact same total duration**, so
the GIFs loop in sync side by side. `.cast` files are asciinema recordings
(replay with `asciinema play <file>`); the GIFs are rendered with `agg`.

The scenario mirrors the "Why agent-talk?" example in the top-level README:
Alice is a data engineer whose agent owns a freshly built dataset,
`customer-churn-v3`; Bob is a research scientist training a churn model on it,
and his agent has a concrete question before it starts.

- **04-alice** — Alice's side. Her one prompt: resume the `alice` identity and
  answer Bob's agent's questions about `customer-churn-v3` over agent-talk. Her
  agent checks the dataset files, then replies to Bob that v3's splits are
  **row-wise** (so a customer can leak across train/val/test) and points him to
  the customer-grouped **v3.1**, then acknowledges his sign-off.
- **05-bob** — Bob's side of the same run. His one prompt: ask Alice's agent
  whether `customer-churn-v3`'s train/test splits are grouped by `customer_id`
  or split row-wise, to rule out leakage before training. His agent sends the
  question, wakes on Alice's answer, and replies that it'll switch to v3.1 —
  the mirror image of the transcript in 04-alice.
