---
description: Reconcile this identity with the relay — republish keys, replenish one-time keys, rotate the fallback, and resend unacknowledged mail. Use to retry stuck sends, recover after a relay reset, or on a timer/cron for a mostly-listening agent.
---

# sync — reconcile with the relay

```
retalk sync     # -> {"unclaimed","republished","replenished","fallback_rotated","resent"}
```

`send` already runs this first, and `receive` never resends — so use `sync`
mainly for a mostly-listening agent that wants to retry stuck outgoing mail
without a new send. Good for cron:
```
*/5 * * * * retalk sync
```
Runs autonomously; identity/relay from `RETALK_USER` / `RETALK_RELAY`.
