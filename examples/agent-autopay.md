# Agent Autopay Example

This example shows an agent consuming a paid resource without human checkout.

```ts
import { AIFPAgent } from "@aifinpay/agent";

const agent = new AIFPAgent({
  apiKey: process.env.AIFP_AGENT_KEY,
  walletId: "wlt_3a1b",
  budget: {
    dailyUsd: 5,
    maxPerRequestUsd: 0.10
  }
});

const response = await agent.fetch("https://merchant.example.com/api/data", {
  headers: { "Accept-Payment": "aifp/1.0" }
});

console.log(await response.json());
```

For AIFP-1, budget policy is evaluated against the **gross payer amount**. Under the current Standard profile, gross `$0.0005` means merchant `$0.000495`, AiFinPay `$0.000005`, creator `0`; no extra 1% is added above `$0.0005`.

The SDK should:

1. Detect and classify the AIFP-1 `402 Payment Required` challenge.
2. Parse merchant/resource/pricing data.
3. Check budget policy against the gross payer price.
4. Request a binding quote.
5. Validate `route_class=AIFP-1`, `treasury_bps=100`, `creator_bps=0`, `payer_total_amount=gross_amount`, and exact `merchant + protocol_fee + creator = gross` conservation.
6. Reject a fee-on-top target before signing.
7. Build the canonical settlement transaction for exactly the gross amount.
8. Sign and broadcast from the payer wallet locally.
9. Submit the `quote_id` and `tx_ref` with an idempotency key for independent settlement verification.
10. Receive a receipt only after successful verification.
11. Retry the original request with `Payment-Receipt`.

A transport retry after possible broadcast must reconcile the existing payment before initiating another spend.
