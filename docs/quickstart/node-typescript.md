# Node / TypeScript AIFP-1 Quick Start

This page shows the AIFP-1 protocol flow in TypeScript-style pseudocode. Verify the actual published SDK package/version and its current API in the SDK repository/package registry before copying package-specific code into production.

## Current AIFP-1 Economics

```ts
const AIFP1 = {
  pricesUsd: {
    standard: "0.0005",
    complex: "0.002",
    premium: "0.005"
  },
  treasuryBps: 100,
  creatorBps: 0
} as const;
```

AIFP-2/x402 is a separate `0/0` route profile.

## Protocol-Oriented Flow

```ts
async function payAifp1Resource(url: string) {
  const first = await fetch(url);
  if (first.status !== 402) return first;

  const challenge = await first.json();
  if (challenge.protocol !== "AIFP-1") {
    throw new Error("not an AIFP-1 challenge");
  }

  const quoteRes = await fetch(challenge.quote_endpoint, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({
      merchant_id: challenge.merchant_id,
      resource: challenge.resource,
      pricing_tier: challenge.pricing_tier,
      units: 1
    })
  });

  if (!quoteRes.ok) throw new Error(`quote failed: ${quoteRes.status}`);
  const quote = await quoteRes.json();

  if (quote.route_class !== "AIFP-1") throw new Error("route mismatch");
  if (Number(quote.treasury_bps) !== 100 || Number(quote.creator_bps) !== 0) {
    throw new Error("AIFP-1 economics mismatch");
  }

  // Budget/policy check must happen before signing.
  await assertBudgetAllows(quote);

  // Implementation-specific: build the transaction for the canonical verified
  // deployment, then ask the payer wallet to sign and broadcast locally.
  const tx = await buildSettlementFromVerifiedRegistry(quote);
  const txRef = await payerWallet.signAndBroadcast(tx);

  // Submit only the settlement reference — never the private key/recovery phrase.
  const payRes = await fetch("https://api.aifinpay.io/v1/pay", {
    method: "POST",
    headers: {
      "content-type": "application/json",
      "idempotency-key": crypto.randomUUID()
    },
    body: JSON.stringify({
      quote_id: quote.quote_id,
      chain: quote.chain,
      asset: quote.asset,
      tx_ref: txRef
    })
  });

  if (payRes.status === 202) throw new Error("settlement pending; reconcile before retrying payment");
  if (!payRes.ok) throw new Error(`settlement verification failed: ${payRes.status}`);

  const receipt = await payRes.json();

  return fetch(url, {
    headers: {
      "Payment-Receipt": receipt.receipt
    }
  });
}
```

## Required Safety Properties

- classify AIFP-1 separately from x402;
- validate quote economics `100/0` before signing;
- enforce budget before signing/broadcasting;
- use exact decimal/integer money arithmetic;
- use the canonical deployment/ABI/IDL for the selected route;
- keep signing local to the payer wallet;
- do not issue/trust a receipt until settlement verification succeeds;
- reconcile ambiguous broadcast errors before retrying a payment;
- prevent replay/duplicate settlement consumption.

## Going Live

Do not switch a route to live spend merely by changing a base URL. Confirm that the selected chain/asset has:

1. canonical current settlement target;
2. current AIFP-1 `100/0` economics;
3. correct token decimals;
4. SDK transaction builder support;
5. settlement verifier support;
6. end-to-end payment/receipt/replay evidence;
7. appropriate review/approval for the financial path.

See [AIFP-1 HTTP 402 Flow](../core-concepts/x402-flow.md) and [SDK Specification](../aifp/03-AI-Agent-SDK-Specification.md).
