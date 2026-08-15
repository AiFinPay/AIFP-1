# AIFP-1 SDK Reference

**Document:** AIFP-DOC-11  
**Status:** Draft SDK contract  
**Governed by:** [AIFP-1 RFC](./01-AIFP-1-RFC-Payment-Protocol-Specification.md)  
**Aligned to:** [OpenAPI](./08-OpenAPI-3.1-Specification.yaml) · [JSON Schemas](./10-JSON-Schemas.md)

This document defines the behavior an AIFP-1 SDK should expose. It does **not** assert that every language package, class name, or method shown in older drafts is published or production-ready. Package-specific documentation must be verified against the actual package/repository before being presented as available.

## 1. Route Model

An SDK must distinguish the product route before it constructs or signs a payment:

| Route | Economics | Purpose |
|---|---|---|
| `AIFP-1` | `treasuryBps=100`, `creatorBps=0` | Merchant AI-traffic/resource monetization |
| `AIFP-2/x402` | `treasuryBps=0`, `creatorBps=0` | Separate agent-payment route |

AIFP-1 helpers MUST NOT silently fall back to an AIFP-2 or legacy `100/1` settlement target.

## 2. Current AIFP-1 Reference Prices

| Tier | Price/action |
|---|---:|
| `standard` | `$0.0005` |
| `complex` | `$0.002` |
| `premium` | `$0.005` |

SDKs should treat the server-issued binding quote as authoritative for a specific transaction while exposing the tier/reference price to the caller for policy decisions.

## 3. Required Agent-Side Capabilities

A conforming AIFP-1 client SDK should provide equivalents of:

```ts
type Aifp1QuoteRequest = {
  merchantId: string;
  resource: string;
  scope?: string;
  pricingTier: "standard" | "complex" | "premium";
  units?: number;
  preferredAsset?: string;
  preferredChain?: string;
};

type Aifp1Quote = {
  quoteId: string;
  routeClass: "AIFP-1";
  merchantId: string;
  resource: string;
  merchantAmount: string;
  totalAmount?: string;
  treasuryBps: 100;
  creatorBps: 0;
  asset: string;
  chain: string;
  settlementTarget?: string;
  expiresAt: string;
};
```

### Quote

```ts
quoteAifp1(request: Aifp1QuoteRequest): Promise<Aifp1Quote>
```

The SDK MUST reject a quote when:

- `routeClass !== "AIFP-1"`;
- `treasuryBps !== 100`;
- `creatorBps !== 0`;
- the quote is expired;
- merchant/resource binding does not match the request;
- the selected route is not in the SDK's trusted/verified registry when such a registry is used.

### Settlement construction

The SDK should construct the transaction for the payer but keep signing local to the payer wallet.

```ts
buildAifp1Settlement(quote: Aifp1Quote): Promise<UnsignedOrWalletReadyTransaction>
```

AIFP-1 SDK code MUST NOT require sending a private key, recovery phrase, or raw signing secret to the AiFinPay receipt service.

### Settlement submission

After local signing/broadcast, the SDK submits the settlement reference for verification:

```ts
submitAifp1Settlement(input: {
  quoteId: string;
  chain: string;
  asset: string;
  txRef: string;
  idempotencyKey: string;
}): Promise<Aifp1Receipt | PendingSettlement>
```

A successful receipt response means the verifier accepted the settlement. A `txRef` by itself is not proof of success.

## 4. Pay-Through Helper

An SDK may expose a high-level helper such as:

```ts
fetchPaid(url, options)
```

Expected behavior:

1. issue original request;
2. if response is not an AIFP-1 `402`, return/route it normally;
3. parse the AIFP-1 challenge;
4. enforce caller budget/policy;
5. obtain and validate the binding quote;
6. build/sign/broadcast settlement locally;
7. submit the settlement reference for verification;
8. receive a receipt only after verification;
9. retry the original request with the receipt;
10. never retry through AIFP-2 merely to bypass an AIFP-1 budget or route error.

## 5. Budget Safety

Budget enforcement must be concurrency-safe. A daily/window cap that resets on process restart or can be bypassed by two simultaneous calls is not sufficient for an autonomous payment SDK.

An SDK implementation should use an atomic reserve/commit/release model or another durable equivalent when a persistent spend cap is promised.

## 6. Merchant-Side Verification

A merchant SDK/verifier should expose an equivalent of:

```ts
verifyAifp1Receipt(receipt, {
  merchantId,
  resource,
  requiredAmount
})
```

It must validate the required active receipt profile, including:

- signature and allowed algorithm;
- issuer/trusted key;
- merchant/audience;
- resource/scope;
- expiry;
- paid amount or quota sufficiency;
- replay/consumption/idempotency state where applicable.

The result must fail closed on ambiguity.

## 7. Numeric Handling

All SDKs MUST use exact integer minor units or arbitrary/exact decimal handling for money. Binary floating-point comparisons are not acceptable for settlement validation.

Token/stablecoin amounts must be converted using the actual configured token decimals for the selected route.

## 8. Error Classes

SDKs should expose typed errors or equivalent machine-readable codes for at least:

- payment required / AIFP-1 challenge;
- quote expired;
- unsupported or unverifiable route;
- route economics mismatch;
- budget exceeded;
- settlement pending;
- settlement mismatch/underpayment;
- duplicate/replay/idempotency conflict;
- invalid receipt;
- rate/service unavailable.

An unsupported verifier route should be reported **before** the payer is instructed to send funds whenever possible.

## 9. Cross-Language Guarantees

Any language implementation claiming AIFP-1 conformance should preserve the same protocol semantics:

1. AIFP-1 route identification.
2. Current reference prices `$0.0005 / $0.002 / $0.005`.
3. Exact `100/0` economics.
4. Local payer signing/non-custodial settlement behavior where the selected rail supports it.
5. Settlement verification before receipt issuance.
6. Merchant/resource/scope binding.
7. Exact monetary arithmetic.
8. Replay/idempotency protection.
9. Explicit isolation from AIFP-2 `0/0` and legacy fee-bearing targets.

Actual package names, release versions, supported chains, and published APIs must be documented in their own repositories/package registries and must not be invented here.
