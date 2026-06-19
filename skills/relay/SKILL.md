---
description: Set up, check, stop, or delete a retalk relay server (retalk-server). Use when the user needs their OWN relay rather than an existing URL. Invoke as `relay setup`, `relay ping`, `relay stop`, or `relay delete`. Uses AskUserQuestion to pick the host (Local / Hugging Face / GCP) and gather settings.
---

# relay — run a retalk relay (`relay <action>`)

A relay is the untrusted server clients connect to; its **audience URL** is what
clients set as `RETALK_RELAY`. Read the action from `$ARGUMENTS`: `setup`,
`ping`, `stop`, or `delete`. If none is given, use **AskUserQuestion** to choose.

**The one rule for every host:** clients sign requests against the relay URL, so
the server's **`RETALK_SERVER_AUDIENCE` must exactly equal the URL clients use as
`RETALK_RELAY`** (scheme included, no trailing slash). A mismatch makes every
request fail with `bad signature`.

## setup
1. **AskUserQuestion — where to host?**
   - **Local** — quickest; testing or same-machine agents; no public URL.
   - **Hugging Face Space** — free public HTTPS, zero infra; sleeps when idle,
     no persistent disk. Full steps: `huggingface.md` (this folder).
   - **GCP VM (+ Cloudflare)** — durable, ~$3.65–10/mo. Full steps: `gcp.md`.
2. Follow that host's reference file. Then hand the user the **audience URL** to
   use as `RETALK_RELAY` in the **init** skill.
3. **Optional hardening** — AskUserQuestion whether to add any of: mailbox caps
   (`--max-mailbox`, `--max-mailbox-per-sender`), `--rate-limit`, or a *closed*
   relay (`--admin-password` to mint API keys at `/admin`; `--require-api-key`
   to require one on every request). Apply as flags/env on the server.

### Local quick start
```
RETALK_SERVER_DB=./relay.db RETALK_SERVER_HOST=127.0.0.1 RETALK_SERVER_PORT=8766 \
  RETALK_SERVER_AUDIENCE=http://127.0.0.1:8766 retalk-server
```
Set the DB via the **`RETALK_SERVER_DB` env var, not the `--db` flag** (the flag
does not create the schema).

## ping
Probe reachability (URL from `$ARGUMENTS`, else `RETALK_RELAY`, else ask):
```
curl -s -o /dev/null -w '%{http_code}\n' <relay_url>
```
Any HTTP status (e.g. `404`) = the relay is **up** (a GET to `/` returns
`404 {"error":"not found"}`); a connection error/timeout = down. For a Hugging
Face Space this request also wakes it from sleep (allow a cold start).

## stop
Infer the host from the URL (`*.hf.space` → Hugging Face; a gcloud VM → GCP;
else Local) or ask:
- **Local:** stop the process, e.g. `pkill -f retalk-server`.
- **Hugging Face:** pause the Space (Settings page), or let it idle.
- **GCP:** `gcloud compute instances stop retalk-server --zone <zone>`
  (a stopped VM costs only its disk).

## delete
- **Local:** stop it, then remove its `server.db`.
- **Hugging Face:** `hf repo delete <owner>/<space> --repo-type space`.
- **GCP:** `gcloud compute instances delete retalk-server --zone <zone>` plus
  `gcloud compute firewall-rules delete allow-iap-ssh`, or remove the whole
  project: `gcloud projects delete <project>`.

Full host steps live in **huggingface.md** and **gcp.md** in this folder.
