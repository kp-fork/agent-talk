# relay setup — Hugging Face Space (free public HTTPS)

A Docker Space gives a public HTTPS URL (TLS terminated by HF) on the free CPU
tier — no domain, no firewall. Trade-offs: **no persistent disk** (the db is
wiped on each restart; retalk self-heals via republish + outbox resend, but mail
sitting undelivered at a reset is lost) and it **sleeps after ~48h idle** (a
`receive --follow` client keeps it awake). Good for personal/testing relays; for
durability use `gcp.md`.

## Audience rule
The public URL is deterministic: `https://<owner>-<space>.hf.space` (lowercased,
`/` replaced by `-`). `RETALK_SERVER_AUDIENCE` MUST equal it exactly, or every
request fails `bad signature`.

## 1. Two files in an empty folder

`README.md` (the YAML header makes it a Docker Space):

    ---
    title: Retalk Relay
    emoji: 🔁
    colorFrom: blue
    colorTo: green
    sdk: docker
    app_port: 7860
    pinned: false
    ---

    # retalk relay
    Untrusted relay for retalk. Stores only public keys and ciphertext.

`Dockerfile`:

    FROM python:3.12-slim
    RUN pip install --no-cache-dir retalk
    RUN useradd -m -u 1000 user
    USER user
    ENV HOME=/home/user \
        PATH=/home/user/.local/bin:$PATH \
        RETALK_SERVER_HOST=0.0.0.0 \
        RETALK_SERVER_PORT=7860 \
        RETALK_SERVER_DB=/home/user/server.db
    WORKDIR /home/user
    EXPOSE 7860
    CMD ["sh","-c",": \"${RETALK_SERVER_AUDIENCE:?set the RETALK_SERVER_AUDIENCE Space variable to https://<owner>-<space>.hf.space}\"; echo \"retalk audience: $RETALK_SERVER_AUDIENCE\"; exec retalk-server --audience \"$RETALK_SERVER_AUDIENCE\""]

`app_port` and `RETALK_SERVER_PORT` must match (7860).

## 2. Create the Space + set the audience (CLI)
`pip install huggingface_hub`, `hf auth login`, then (ask via AskUserQuestion for
`<owner>` and the space name if not given):

    hf repo create <owner>/retalk-relay --repo-type space --space-sdk docker
    python -c "from huggingface_hub import HfApi; HfApi().add_space_variable('<owner>/retalk-relay','RETALK_SERVER_AUDIENCE','https://<owner>-retalk-relay.hf.space')"
    hf upload <owner>/retalk-relay . --repo-type space   # from the folder with the two files

The Space MUST be **public** — a private Space requires an HF token that retalk
clients do not send, so remote clients could not reach it.

## 3. Verify
In the Space **Logs**, wait for: `retalk audience: https://<owner>-retalk-relay.hf.space`.
That audience is the relay URL clients use as `RETALK_RELAY`.

## Delete
`hf repo delete <owner>/retalk-relay --repo-type space` (or the Space Settings page).
