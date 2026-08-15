# AIFP-1 Quick Start Guide

**Document:** AIFP-DOC-07 · **Status:** Draft implementation guidance · **Governed by:** AIFP-1 (Doc 01)

AIFP-1 is the merchant AI-traffic monetization profile built around HTTP `402 Payment Required`. The intended loop is:

`request → AIFP-1 402 challenge → binding quote → payer settlement → settlement verification → receipt → retry`

This repository is a protocol/specification project. Examples below describe the required behavior; they do not by themselves prove that every SDK, network, asset, or hosted endpoint is production-live.

---

## 1. Current Economics

| Tier | Reference action price | Typical action |
|---|---:|---|
| `standard` | `$0.0005` | Simple read, single record, lightweight API request |
| `complex` | `$0.002` | Search, aggregation, multi-source query, higher compute |
| `premium` | `$0.005` | AI inference, GPU workload, deep analytics, premium data |

Current AIFP-1 merchant-monetization profile:

- AiFinPay protocol fee: exactly **1% (`100` bps)**;
- creator/referral fee: **0 bps**;
- merchant amount: **99% before external network/settlement costs**.

AIFP-2/x402 is a separate agent-payment route profile with `treasuryBps=0` and `creatorBps=0`. Do not apply the AIFP-1 1% fee to an AIFP-2 payment.

---

## 2. Merchant Flow

A merchant integration needs four behaviors:

1. identify the merchant and protected resource/scope;
2. return an AIFP-1 `402` challenge when payment is required;
3. verify an AIFP-1 receipt locally before serving protected access;
4. meter or consume the receipt/quota according to its scope and replay rules.

Illustrative middleware shape:

```ts
app.use(aifpPaywall({
  merchantId: "mrch_example",
  pricing: {
    "/api/data": { tier: "standard" },
    "/api/search": { tier: "complex" },
    "/api/inference": { tier: "premium" }
  }
}));
```

A conforming implementation must fail closed when receipt signature, audience, scope/resource, expiry, amount/quota, or replay/idempotency checks fail.

---

## 3. Agent Flow

An AIFP-1-aware agent should:

1. request the protected resource;
2. recognize an AIFP-1 `402` challenge;
3. enforce its own spend/budget policy;
4. request a binding quote;
5. verify that the selected settlement route is supported and verifiable **before paying**;
6. sign and broadcast settlement from the payer wallet or explicitly supported payment rail;
7. submit the settlement reference for verification;
8. receive a receipt only after settlement verification succeeds;
9. retry the original request with the receipt.

Conceptual HTTP sequence:

```http
GET /api/data
→ 402 + AIFP-1 challenge

POST /v1/quote
→ quote_id + merchant + resource/scope + amount + asset/route + expiry

[payer signs and broadcasts settlement]

POST /v1/pay
{ "quote_id": "...", "chain": "...", "asset": "...", "tx_ref": "..." }
→ receipt only after verification

GET /api/data
Payment-Receipt: <receipt>
→ protected response when receipt validation succeeds
```

A quote must not instruct the agent to pay through a route whose settlement verifier is unavailable or unable to validate the quoted economic profile.

---

## 4. Economic Route Isolation

AIFP-1 and AIFP-2 are intentionally distinct:

| Route class | AiFinPay fee | Creator/referral | Intended use |
|---|---:|---:|---|
| AIFP-1 | `100` bps | `0` bps | Merchant AI-traffic/resource monetization |
| AIFP-2/x402 | `0` bps | `0` bps | Agent x402-style payment route |

Implementations must not silently fall back between these profiles. A route mismatch must fail closed.

---

## 5. Settlement Safety

Before a route is treated as payment-live, the implementation should have evidence for:

- canonical contract/program/address and source provenance;
- correct route economics (`100/0` for AIFP-1);
- supported asset decimals and amount conversion;
- quote binding to merchant, resource/scope, amount, asset, chain, and expiry;
- settlement verification before receipt issuance;
- replay/idempotency rejection;
- finality/reorg handling appropriate to the network;
- ledger/reconciliation and operational monitoring where applicable.

A chain being deployed does **not** automatically mean every AIFP-1 payment route on that chain is live.

---

## 6. Receipt Verification

Merchant-side verification should validate at least the claims required by the active receipt profile:

- allowed signature algorithm and trusted key;
- issuer;
- merchant/audience;
- resource or scope;
- paid amount/quota semantics;
- expiry;
- nonce/payment/replay binding.

Monetary values must use exact decimal or integer minor-unit arithmetic, not binary floating-point comparisons.

---

## 7. Testing Checklist

Before declaring an integration ready, test:

- unpaid request → `402` with machine-readable AIFP-1 challenge;
- correct quote uses `$0.0005 / $0.002 / $0.005` reference tiers when those presets are selected;
- AIFP-1 settlement results in `100/0`, not `100/1`;
- merchant receives the quoted merchant amount according to the selected contract semantics;
- creator/referral amount is zero;
- receipt is never issued for an unverifiable or mismatched settlement;
- valid receipt unlocks only its intended resource/scope;
- expired, malformed, cross-merchant, underpaid, or replayed proofs fail closed;
- AIFP-2 `0/0` routes cannot be confused with AIFP-1 `100/0` routes.

---

## 8. Related Documents

- [AIFP-1 RFC](./01-AIFP-1-RFC-Payment-Protocol-Specification.md)
- [Merchant Integration Guide](./02-Merchant-Integration-Guide.md)
- [AI Agent SDK Specification](./03-AI-Agent-SDK-Specification.md)
- [Security & Cryptography Specification](./04-Security-and-Cryptography-Specification.md)
- [Protocol Economics](../economics.md)
- [OpenAPI 3.1](./08-OpenAPI-3.1-Specification.yaml)
- [JSON Schemas](./10-JSON-Schemas.md)
