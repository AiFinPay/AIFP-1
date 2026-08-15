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
2. The agent quotes the Standard tier at a **gross payer price of `$0.0005`**.
3. Under current AIFP-1 economics, the agent settles `$0.0005`; the merchant receives `$0.000495` (99%), AiFinPay receives `$0.000005` (1%), and creator/referral receives `0`. The 1% is deducted from gross and is not added on top.
4. The settlement verifier confirms the gross amount and 99/1/0 split before a receipt is issued.
5. Requests retried with a valid receipt return `200`.
6. Invalid, expired, underpaid, fee-on-top, or replayed receipts/settlements are rejected.
