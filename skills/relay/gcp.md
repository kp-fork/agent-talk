# relay setup — Google Cloud VM (durable) + Cloudflare

A small `e2-micro` VM runs `retalk-server`; its **public HTTPS URL comes from a
Cloudflare tunnel** (the VM keeps NO inbound ports open). Roughly $3.65/mo
(free-tier compute) up to ~$10/mo on-demand. Ask (AskUserQuestion) for the
project name / zone / machine type if not given; the defaults below are fine for
10–100 users.

## 1. Project + APIs  (needs the gcloud CLI, `gcloud auth login`)

    gcloud projects create my-retalk --name="my-retalk"
    gcloud billing projects link my-retalk --billing-account=XXXXXX-XXXXXX-XXXXXX
    gcloud config set project my-retalk
    gcloud services enable compute.googleapis.com iap.googleapis.com

## 2. Lock down SSH (no public inbound ports)

    gcloud compute firewall-rules delete default-allow-ssh default-allow-rdp --quiet
    gcloud compute firewall-rules create allow-iap-ssh --direction=INGRESS --action=ALLOW \
      --rules=tcp:22 --source-ranges=35.235.240.0/20

## 3. Create the VM (no cloud identity — a stolen metadata token is then useless)

    gcloud compute instances create retalk-server --zone=us-central1-a \
      --machine-type=e2-micro --image-family=debian-12 --image-project=debian-cloud \
      --boot-disk-size=10GB --boot-disk-type=pd-standard --no-service-account --no-scopes

## 4. Install + run retalk

    gcloud compute ssh retalk-server --zone us-central1-a --tunnel-through-iap
    # on the VM:
    sudo apt-get update && sudo apt-get install -y python3-venv
    python3 -m venv ~/rt && ~/rt/bin/pip install retalk

Expose it with a **Cloudflare tunnel** (see retalk's `docs/server/cloudflare.md`)
and set `RETALK_SERVER_AUDIENCE` to the tunnel's public https URL:

    RETALK_SERVER_DB=~/server.db RETALK_SERVER_HOST=127.0.0.1 RETALK_SERVER_PORT=8766 \
      RETALK_SERVER_AUDIENCE=https://<your-tunnel-url> ~/rt/bin/retalk-server

Give clients that audience as `RETALK_RELAY`.

## Stop / delete

    gcloud compute instances stop retalk-server --zone us-central1-a     # stop: disk-only cost
    gcloud compute instances delete retalk-server --zone us-central1-a   # delete the VM
    gcloud compute firewall-rules delete allow-iap-ssh
    gcloud projects delete my-retalk                                     # or remove everything
