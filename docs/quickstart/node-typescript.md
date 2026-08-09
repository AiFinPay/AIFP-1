# Node / TypeScript Quick Start

## What You Need

- Node.js 20 LTS or newer.
- An AiFinPay sandbox merchant endpoint.
- A test wallet funded with sandbox tokens.
- A sandbox API key that starts with `sk_test_`.
- A test token source for sandbox funds. The public faucet URL is published with the hosted sandbox.

## Install

```bash
npm install @aifinpay/agent@alpha @aifinpay/merchant@alpha
```

`alpha` means the API may change while the SDK surface is still being settled.

## Sandbox Example

```ts
import { AIFPAgent } from "@aifinpay/agent";

async function main() {
  const agent = new AIFPAgent({
    apiKey: process.env.AIFP_AGENT_KEY!,
    walletId: process.env.AIFP_WALLET_ID!,
    baseUrl: "https://sandbox.api.aifinpay.io"
  });

  const response = await agent.call("https://sandbox.merchant.example/api/data", {
    method: "GET",
    headers: {
      "Accept-Payment": "aifp/1.0"
    }
  });

  console.log(JSON.stringify(response, null, 2));
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
```

Example sandbox response:

```json
{
  "ok": true,
  "resource": "/api/data",
  "pricing_tier": "standard",
  "quote_id": "qt_sbx_01",
  "receipt_id": "rcpt_sbx_01",
  "receipt_status": "settled",
  "charged_amount": "0.0005",
  "protocol_fee": "0.0000001",
  "merchant_settlement": "0.0000099"
}
```

## What Happened Under The Hood

The SDK detected a `402 Payment Required` response, requested a quote, paid the sandbox price,
received a receipt token, and retried the original request. The receipt is a signed capability
that the merchant can verify locally without a round trip. For the protocol mechanics, see
[x402 Flow](../core-concepts/x402-flow.md). The receipt is bound to the merchant, resource, amount,
and nonce so it cannot be replayed elsewhere.

## Going To Production

- Audit the merchant contract and receipt verification path.
- Set explicit spend limits on the wallet.
- Switch the base URL from sandbox to production only after approval.
- Replace sandbox keys with production keys.
- Add monitoring for 402, 409, 410, 422, and 429 responses.
- Confirm the payout account and settlement rail before enabling live spend.

## Common Mistakes

- Using a production key against the sandbox URL.
- Forgetting to attach an `Idempotency-Key` for repeated payment attempts.
- Reusing an expired quote.
- Reusing a nonce.
- Calling the production endpoint before wallet policy is in place.
