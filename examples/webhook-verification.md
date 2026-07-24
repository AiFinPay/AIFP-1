# Webhook Verification Example

AIFP webhooks must be signed and timestamp-verified.

```ts
import { verifyWebhook } from "@aifinpay/merchant";

app.post(
  "/webhooks/aifp",
  express.raw({ type: "application/json" }),
  (req, res) => {
    const event = verifyWebhook({
      payload: req.body,
      signature: req.header("AIFP-Signature"),
      timestamp: req.header("AIFP-Timestamp"),
      secret: process.env.AIFP_WEBHOOK_SECRET
    });

    if (await webhookStore.seen(event.id)) {
      return res.sendStatus(204);
    }

    if (event.type === "settlement.completed") {
      // Update internal ledger after signature and replay checks.
    }

    await webhookStore.markSeen(event.id, { ttlSeconds: 86400 });

    res.sendStatus(204);
  }
);
```

Webhook handlers should reject missing signatures, stale timestamps, duplicate event
IDs, malformed payloads, and unexpected event types.
