# Demos

One live **agent-to-agent conversation**, shown from both sides: **04-alice**
and **05-bob** were recorded simultaneously in two Claude Code sessions (two
docker sandboxes talking through a **temporary local relay**). All setup —
identity, keys, adding + verifying the peer, and arming the auto-receive wake
monitor — happens **before** the recording and is cleared away, so each clip
opens on a clean screen. On **05-bob** the human types just **one short task
prompt**; on **04-alice** the human types **nothing at all** — her primed
session simply wakes on Bob's message and answers. Everything after that is the
two agents talking to each other over agent-talk on their own: every message is
**agent-authored**, and each incoming message **wakes the receiving session by
itself** (the receive skill's persistent wake monitor fires; nobody types any
conversation content). The prompt types in quickly (~5s on screen) and the
conversation plays at **2×**. The two casts share the **exact same total
duration** and are rendered to **identical GIF length** so they loop in
lockstep side by side. `.cast` files are asciinema recordings (replay with
`asciinema play <file>`); the GIFs are rendered with `agg` (zoomed in with a
larger font size).

The scenario mirrors the "Why agent-talk?" example in the top-level README:
Alice is a data engineer whose agent owns a freshly built dataset,
`customer-churn-v3`; Bob is a research scientist training a churn model on it,
and his agent has a concrete question before it starts.

- **05-bob** — Bob's side. His one typed prompt asks Alice's agent whether
  `customer-churn-v3`'s train/test splits are grouped by `customer_id` or split
  row-wise, to rule out leakage before training. His agent sends the question,
  wakes on Alice's answer, and replies that it'll switch to `v3.1`.
- **04-alice** — Alice's side of the same run, with **no typed prompt**. Her
  primed agent wakes on Bob's incoming message, checks the dataset, and replies
  that v3's splits are **row-wise** (so a customer can leak across
  train/val/test), pointing him to the customer-grouped **v3.1** — the mirror
  image of the transcript in 05-bob.
