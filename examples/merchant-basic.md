# Merchant Basic Example

This example shows a merchant protecting `/api/data` with AIFP.

```ts
import express from "express";
import { aifpPaywall } from "@aifinpay/merchant";

const app = express();

app.use(aifpPaywall({
  merchantId: "mrch_9f3a1c2b",
  pricing: {
    "/api/data": { tier: "standard" }
  }
}));

app.get("/api/data", (req, res) => {
  res.json({ data: "premium machine-readable resource" });
});

app.listen(3000);
```

Expected behavior:

1. Paid actions return `402 Payment Required` when no valid receipt is present.
2. The agent quotes the Standard tier, starting from `$0.0005`.
3. Under the current AIFP-1 merchant-monetization profile, AiFinPay applies exactly 1% (`100` bps), creator/referral fee is 0 bps, and the merchant receives 99% before network or settlement costs.
4. Requests retried with a valid receipt return `200`.
5. Invalid, expired, or replayed receipts are rejected.
