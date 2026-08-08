# MCP Server Quick Start

## What You Need

- Node.js 20 LTS or newer.
- A local MCP host or editor integration.
- An AiFinPay sandbox merchant endpoint.
- A test wallet funded with sandbox tokens.
- A sandbox API key that starts with `sk_test_`.
- A test token source for sandbox funds. The public faucet URL is published with the hosted sandbox.

## Install

```bash
npm install @aifinpay/mcp @aifinpay/agent
```

`alpha` means the API may change while the SDK surface is still being settled.

## Sandbox Example

```ts
import { AIFPMCPServer } from "@aifinpay/mcp";

async function main() {
  const server = new AIFPMCPServer({
    apiKey: process.env.AIFP_AGENT_KEY!,
    walletId: process.env.AIFP_WALLET_ID!,
    baseUrl: "https://sandbox.api.aifinpay.io",
  });

  await server.start();

  // The MCP layer exposes protocol calls to the developer tool or agent host.
  const response = await server.call("aifinpay.quote", {
    merchant_id: "mrch_sandbox_01",
    resource: "/api/data",
    pricing_tier: "standard"
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
  "tool": "aifinpay.quote",
  "quote_id": "qt_sbx_01",
  "merchant_id": "mrch_sandbox_01",
  "resource": "/api/data",
  "pricing_tier": "standard",
  "amount": "0.0005",
  "currency": "USD"
}
```

## What Happened Under The Hood

The MCP server exposes protocol actions to a developer tool without embedding payment logic in
the app itself. The sandbox path still starts with a `402` challenge, then a quote, then a payment,
then a receipt-bound retry. This keeps the protocol aligned with [x402 Flow](../core-concepts/x402-flow.md).
Machine-action policy is declared in `.well-known/aifinpay.json`.

## Going To Production

- Audit the merchant contract and receipt verification path.
- Set explicit spend limits on the wallet.
- Switch the base URL from sandbox to production only after approval.
- Replace sandbox keys with production keys.
- Add monitoring for 402, 409, 410, 422, and 429 responses.
- Confirm the payout account and settlement rail before enabling live spend.

## Common Mistakes

- Starting the MCP server without a wallet policy.
- Pointing the MCP host at a production endpoint during testing.
- Forgetting to clear sandbox credentials after the demo.
- Reusing an expired quote.
- Reusing a nonce.
