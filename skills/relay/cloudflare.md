# relay setup — Cloudflare Tunnel (expose a LOCAL server publicly)

Run `retalk-server` on your own machine (or any box) and give it a public HTTPS
URL via Cloudflare — no open firewall port, no TLS cert, no cloud VM.
`cloudflared` makes an outbound connection to Cloudflare, which forwards public
requests down it to your local server (TLS terminated at Cloudflare's edge; the
server still speaks plain HTTP). Two ways:

- **Quick tunnel** — free, no account, no domain. Random
  `https://<words>.trycloudflare.com` URL that lasts only while `cloudflared`
  runs. Best for a quick or throwaway public relay.
- **Named tunnel** — your own domain on a Cloudflare account; a stable hostname
  that survives restarts. Use for anything lasting.

**The one rule:** `RETALK_SERVER_AUDIENCE` must equal the public `https://…`
Cloudflare URL (not `http://localhost:…`), or every request fails `bad
signature`.

Install `cloudflared` first: https://github.com/cloudflare/cloudflared

## Quick tunnel (free, no account)
1. Start the tunnel on the server's port; copy the URL it prints:

       cloudflared tunnel --url http://localhost:8766
       # -> https://<words>.trycloudflare.com

2. In another terminal, start the server with that URL as its audience:

       RETALK_SERVER_DB=./relay.db RETALK_SERVER_PORT=8766 \
         RETALK_SERVER_AUDIENCE=https://<words>.trycloudflare.com retalk-server

3. Clients use that same URL as `RETALK_RELAY`.

The URL changes each time you restart the quick tunnel.

## Named tunnel (your domain, stable) — preferred for real use
Use a per-tunnel **token** (safer than `cloudflared tunnel login`, which scopes
to your whole Cloudflare zone):

1. Cloudflare Zero Trust dashboard → Networks → Tunnels → Create a tunnel; copy
   the token.
2. `cloudflared tunnel run --token <TOKEN>`
3. On that page, add a public hostname (e.g. `retalk.example.com`) routing to
   `http://localhost:8766`.
4. Start the server:

       RETALK_SERVER_PORT=8766 RETALK_SERVER_AUDIENCE=https://retalk.example.com retalk-server

   Clients use `https://retalk.example.com`.

## Stop / delete
- Stop both processes: stop `retalk-server` and the tunnel (`pkill -f cloudflared`).
- A quick tunnel leaves nothing behind. A named tunnel:
  `cloudflared tunnel delete <name>`, then remove its CNAME from Cloudflare DNS.
