# AIFP-1 — Merchant AI-Traffic Monetization Protocol

**Document:** AIFP-1  
**Category:** Standards Track  
**Status:** Draft Specification  
**Version:** 1.0.0-draft  
**Updated:** August 15, 2026  
**Maintainer:** AiFinPay Protocol Team  
**Contact:** protocol@aifinpay.io

> AIFP-1 is an experimental/open protocol specification. This document defines the target protocol behavior and conformance requirements. It does **not** claim that every documented network, SDK surface, hosted service, or settlement route is production-ready.

---

## 1. Scope

AIFP-1 defines a merchant-side monetization protocol for AI-agent traffic to websites, APIs, MCP servers, data products, content, and digital services.

AIFP-1 uses HTTP `402 Payment Required` as the payment-required signal and defines an AIFP-specific sequence:

`request → 402 challenge → binding quote → payer settlement → settlement verification → receipt → retry`

AIFP-1 is economically and operationally distinct from **AIFP-2/x402**. AIFP-2 is not specified by this document.

### 1.1 Current economic profiles

| Route class | AiFinPay protocol fee | Creator/referral fee | Purpose |
|---|---:|---:|---|
| **AIFP-1** | `100` bps / **1%** | `0` bps | Merchant AI-traffic/resource monetization |
| **AIFP-2/x402** | `0` bps / **0%** | `0` bps | Separate agent-payment route |

An implementation MUST NOT silently substitute one route profile for the other.

### 1.2 Current reference action tiers

| Tier | Reference price | Typical workload |
|---|---:|---|
| `standard` | `$0.0005` | Simple read, single record, lightweight API request |
| `complex` | `$0.002` | Search, aggregation, multi-source query, higher compute |
| `premium` | `$0.005` | AI inference, GPU workload, deep analytics, premium data |

These are current AiFinPay reference tiers. A merchant-facing implementation MUST make the effective quoted price machine-readable and deterministic. Any future custom/dynamic pricing rules require an explicit protocol/profile update and MUST NOT be inferred from superseded examples.

---

## 2. Requirements Language

The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHOULD**, **SHOULD NOT**, and **MAY** are normative when written in uppercase.

---

## 3. Roles

- **Agent / Payer:** software requesting a protected merchant resource and executing payment according to its own wallet/budget policy.
- **Merchant:** provider of the protected resource and beneficiary of the commercial amount.
- **AiFinPay Quote Service:** issues a binding payment quote for an AIFP-1 request.
- **Settlement Rail:** blockchain or other explicitly supported rail on which payment is executed.
- **Settlement Verifier:** validates that a submitted settlement reference satisfies the quote.
- **Receipt Authority:** issues a signed receipt only after settlement verification succeeds.
- **Merchant Verifier:** validates a receipt locally before granting protected access.

A single implementation MAY combine logical services, but combining them MUST NOT weaken the security requirements below.

---

## 4. Protocol Invariants

A conforming AIFP-1 implementation MUST preserve these invariants:

1. **No receipt before verified payment.** A receipt MUST NOT be issued merely because the client supplies a transaction hash or claims payment succeeded.
2. **No payment into an unverifiable route.** A quote MUST NOT instruct a payer to settle through a route that the active verifier cannot validate.
3. **Merchant amount is explicit.** The quote MUST identify the merchant amount and the selected economic profile.
4. **Current AIFP-1 fee is exactly `100/0`.** AiFinPay fee is 1%; creator/referral fee is zero.
5. **AIFP-2 is isolated.** AIFP-2 `0/0` payments MUST NOT fall back to fee-bearing AIFP-1 or legacy splitter routes.
6. **Replay/idempotency is enforced.** Reusing a unique payment/settlement identifier outside its allowed semantics MUST fail closed.
7. **Resource access is scoped.** A receipt MUST NOT unlock a merchant/resource/scope it was not issued for.
8. **Exact arithmetic.** Monetary values MUST use integer minor units or exact decimal representations, not binary floating point.
9. **Deployment does not imply payment-live.** A network/contract address alone is insufficient evidence that an AIFP-1 route is safe to quote.
10. **Historical economics are not active economics.** Legacy `100/1` or earlier price examples MAY be retained as audit evidence only when clearly marked legacy/superseded.

---

## 5. HTTP 402 Challenge

### 5.1 When to return 402

A merchant returns HTTP `402 Payment Required` when the requested resource requires an AIFP-1 payment and the request does not carry sufficient valid paid authorization/receipt state.

Issuing a challenge MUST be side-effect free: it MUST NOT itself charge the payer or consume a paid quota.

### 5.2 Required challenge semantics

A challenge MUST provide, directly or through a discoverable quote endpoint, enough information for the agent to determine:

- protocol/profile: `AIFP-1`;
- merchant identity;
- protected resource or scope;
- pricing tier or effective price basis;
- quote endpoint;
- expiry/freshness information;
- supported route/asset information when known.

Illustrative challenge:

```json
{
  "error": "AIFP-402",
  "protocol": "AIFP-1",
  "merchant_id": "mrch_example",
  "resource": "/api/data",
  "pricing_tier": "standard",
  "reference_price_usd": "0.0005",
  "quote_endpoint": "https://api.example/v1/quote"
}
```

A challenge MUST NOT label itself x402 merely because it uses HTTP status `402`.

---

## 6. Binding Quote

The quote is the authoritative pre-payment statement of what the payer is expected to settle.

### 6.1 Required quote bindings

A quote SHOULD include, and the settlement verifier MUST be able to bind to, at least:

- `quote_id`;
- `route_class` = `AIFP-1`;
- merchant identifier and settlement recipient;
- protected resource/scope;
- merchant amount;
- AiFinPay fee profile (`treasury_bps = 100`);
- creator/referral profile (`creator_bps = 0`);
- total amount according to the selected settlement contract/rail semantics;
- asset/token;
- chain/network or settlement rail;
- canonical contract/program/address where applicable;
- unique payment/order binding;
- quote expiry;
- verifier capability/version identifier when applicable.

### 6.2 Reference pricing

When a merchant selects the standard reference tiers, the quote MUST use:

```text
standard = 0.0005 USD/action
complex  = 0.002  USD/action
premium  = 0.005  USD/action
```

Batch settlement MAY aggregate many metered actions into one payment. The per-action meter and the actual settlement amount MUST remain mathematically reconcilable.

### 6.3 Verifier-readiness gate

Before returning a payable quote, the quote service MUST determine that the route is verifiable under the currently deployed verifier.

If the verifier is unavailable, unsupported, stale, or unable to validate the quoted contract/profile, the service MUST fail **before payment** rather than issuing a quote that could strand payer funds without a receipt.

---

## 7. Settlement

### 7.1 Non-custodial payer flow

The preferred AIFP-1 crypto flow is non-custodial:

1. quote is issued;
2. payer wallet constructs and signs the settlement transaction locally;
3. payer broadcasts the transaction;
4. payer receives a settlement reference/transaction hash;
5. payer submits the quote identifier plus settlement reference to AiFinPay;
6. AiFinPay independently verifies settlement;
7. only then is a receipt issued.

The protocol does not require the payer to expose a private key or recovery phrase to AiFinPay.

### 7.2 AIFP-1 fee semantics

For the current AIFP-1 route profile:

```text
treasuryBps       = 100
creatorBps        = 0
AiFinPay fee       = 1%
merchant economics = 99% before external network/settlement costs
```

Implementations MAY use fee-on-top or fee-from-total contract semantics only if the quote makes the payer total and merchant amount unambiguous and the verifier validates the actual deployed semantics.

A `MAX_TOTAL_FEE_BPS` contract constant, where present, is a **security ceiling**, not the active fee rate.

### 7.3 Small-payment handling

Fee-rounding checks MUST be conditional on a non-zero configured fee leg.

For AIFP-1, a route MAY reject a settlement amount too small to produce the required 1% treasury amount under integer arithmetic. Such a minimum MUST be derived from the asset decimals and contract semantics; it MUST NOT rely on an asset-agnostic raw-unit constant that changes economic meaning across token decimal systems.

### 7.4 Asset decimals

Stablecoin and token conversions MUST be decimal-aware. A route MUST verify configured token decimals against canonical chain/token metadata or trusted deployment configuration before being payment-live.

---

## 8. Settlement Verification

A settlement verifier is security-critical.

### 8.1 Minimum checks

For on-chain settlement, the verifier MUST check as applicable:

- transaction exists and reached required finality;
- transaction did not revert/fail;
- expected chain/network;
- expected contract/program/address;
- expected entrypoint/instruction/event;
- expected payer binding where required;
- expected merchant recipient;
- expected token/asset;
- expected merchant amount and total amount;
- expected `quote_id`, order ID, payment ID, nonce, or equivalent binding;
- selected route economics are AIFP-1 `100/0`;
- the settlement has not already been consumed for another receipt.

A verifier MUST NOT pass merely because an RPC call succeeded or because a transaction hash exists.

### 8.2 Unsupported routes

If a chain or asset lacks a complete verifier, that route MUST NOT be exposed as payable AIFP-1 settlement.

---

## 9. Receipt Token

### 9.1 Issuance

A receipt is issued only after successful settlement verification.

A receipt SHOULD bind:

- receipt identifier;
- issuer;
- merchant/audience;
- payer/agent identifier when available;
- resource/scope;
- pricing/paid quota semantics;
- quote/payment/settlement identifier;
- issuance time;
- expiry;
- protocol/profile version.

### 9.2 Signature

The current AIFP-1 receipt design uses Ed25519/EdDSA signatures with merchant-verifiable public-key distribution (for example JWKS).

Implementations MUST reject disallowed algorithms and unsigned receipts.

### 9.3 Merchant verification

Before granting paid access, the merchant verifier MUST validate the claims required by the receipt profile, including at least:

- signature and trusted key;
- issuer;
- merchant/audience;
- resource/scope;
- expiry;
- amount/quota sufficiency;
- replay/idempotency/consumption state where required.

Verification failures MUST fail closed.

---

## 10. Scope And Metering

A receipt MAY authorize:

- one exact resource;
- a prefix/resource group;
- a merchant-wide paid quota;
- another explicitly defined scope.

The merchant MUST charge/meter the actual requested action at its configured weight/price. A wider receipt scope MUST NOT allow a premium action to consume only a standard-action amount.

Metering state MUST be concurrency-safe where double consumption could create financial loss.

---

## 11. Free Access And Policy

Merchants MAY provide free requests or allowlists before requiring payment.

Free-tier identity MUST NOT rely solely on a caller-controlled header such as `AIFP-Agent-Id`; otherwise an agent can rotate identifiers to reset quota. A production implementation SHOULD bind durable quota/policy to a stronger authenticated agent, wallet, session, credential, or equivalent identity mechanism appropriate to the integration.

---

## 12. Idempotency And Replay Protection

Quote, payment, receipt, and webhook processing SHOULD use unique identifiers and idempotent state transitions.

Required behavior includes:

- duplicate settlement consumption does not create a second receipt entitlement;
- retries of the same idempotent request return the same logical result or a deterministic conflict;
- cross-merchant and cross-resource receipt reuse fails;
- expired quotes/receipts fail;
- settlement identifiers are unique in the financial ledger/reconciliation layer.

---

## 13. Error Semantics

Implementations SHOULD return machine-readable error bodies.

Recommended classes:

| HTTP | Meaning |
|---|---|
| `400` | malformed request |
| `401` | missing/invalid API authentication where applicable |
| `402` | AIFP-1 payment required |
| `403` | policy or receipt authorization failure |
| `409` | replay/idempotency/duplicate conflict |
| `410` | quote no longer valid |
| `422` | settlement/receipt mismatch |
| `425` | settlement observed but not sufficiently final |
| `429` | rate/policy limit |
| `5xx` | service/route unavailable; MUST NOT imply payment success |

An implementation MUST distinguish **pending** settlement from **invalid** settlement.

---

## 14. Route Registry And Deployment Provenance

For each payment-live chain/route, implementations SHOULD maintain a canonical registry containing:

- chain/network ID;
- contract/program/address;
- contract version/ABI/IDL identifier;
- runtime/source provenance where available;
- economic profile;
- supported assets and decimals;
- verifier capability;
- activation/review status.

A legacy fee-bearing splitter or historical deployment MUST NOT be automatically selected for new AIFP-2 traffic and MUST NOT be presented as current AIFP-1 `100/0` unless its actual deployed configuration matches that profile.

---

## 15. Ledger And Reconciliation

Financial state SHOULD be durable and append-only or equivalently auditable.

A canonical ledger entry SHOULD record enough information to reconcile:

- route class;
- quote/payment/receipt IDs;
- merchant amount;
- AiFinPay fee amount;
- creator/referral amount;
- asset and decimals;
- chain/network;
- transaction hash and event/instruction identity;
- finality state;
- reversal/reorg correction where applicable.

For current AIFP-1, reconciliation MUST be able to detect deviation from `100/0` economics.

---

## 16. Webhooks

Where webhooks are implemented, they MUST be authenticated and replay-resistant.

Webhook consumers SHOULD:

- verify the configured signature scheme;
- reject duplicate event identifiers;
- tolerate out-of-order delivery without corrupting financial state;
- reconcile settlement data against the canonical ledger/source of truth.

Webhook delivery does not replace settlement verification.

---

## 17. AIFP-1 And AIFP-2/x402 Separation

AIFP-1 and AIFP-2 may coexist in the same SDK or merchant stack, but detection and payment execution MUST remain explicit.

### AIFP-1

- merchant traffic monetization;
- AIFP-1 challenge/quote/receipt lifecycle;
- current AiFinPay economics `100/0`.

### AIFP-2/x402

- separate x402-compatible agent payment route;
- current AiFinPay economics `0/0`;
- x402 wire-version support and interoperability are defined outside this AIFP-1 specification.

A generic HTTP `402` status alone is not enough to classify a response as x402.

---

## 18. Security Requirements

A conforming implementation SHOULD address at minimum:

- receipt forgery;
- settlement spoofing;
- replay and duplicate processing;
- cross-resource/cross-merchant reuse;
- SSRF in hosted gateway/upstream configurations;
- quote manipulation;
- token decimal mismatch;
- route/registry drift;
- compromised owner/admin authority;
- RPC unavailability and stale chain state;
- reorg/finality handling;
- secret/key rotation;
- budget/concurrency races;
- free-quota identity spoofing.

Smart-contract and payment-path changes require independent review appropriate to their financial risk before production authorization.

---

## 19. Conformance

A route is not AIFP-1 payment-live merely because code compiles or a contract exists.

A conformance evidence bundle SHOULD include:

1. exact source commit/version;
2. canonical deployment address/program;
3. contract/program provenance or runtime hash where applicable;
4. CI/test evidence;
5. independent review for high-risk payment/smart-contract changes;
6. successful real or appropriately isolated end-to-end flow:
   - protected request;
   - AIFP-1 `402`;
   - binding quote;
   - payer settlement;
   - verifier confirmation;
   - merchant amount correct;
   - AiFinPay fee exactly 1%;
   - creator/referral amount zero;
   - receipt issuance;
   - protected retry success;
   - replay rejection;
7. ledger/reconciliation evidence where the implementation maintains financial state.

A public claim of network/payment support SHOULD be scoped to the routes for which this evidence exists.

---

## 20. Legacy And Migration Rules

The following are superseded current-product economics:

- Standard `$0.00001`;
- Complex `$0.00006`;
- Premium `$0.00010`;
- AIFP-1 `100/1` or any `0.01%` creator/referral leg.

Historical documents, transaction evidence, or deployment manifests MAY retain these values only when clearly labeled **legacy/historical/superseded**.

New AIFP-1 guidance MUST use `$0.0005 / $0.002 / $0.005` and `100/0`.

---

## 21. Machine-Readable Contracts

The machine-readable surfaces of this repository must remain consistent with this RFC:

- OpenAPI 3.1 specification;
- JSON schema documentation/examples;
- Postman collection;
- SDK/reference examples;
- `.well-known` discovery metadata where present.

A CI/conformance check SHOULD fail when active documentation reintroduces superseded economics outside explicitly historical sections.

---

## 22. Governance

Changes to normative AIFP-1 behavior SHOULD be proposed and reviewed through the repository's AIP/governance process.

Economic changes require explicit approval and coordinated updates to:

- normative RFC;
- economics document;
- OpenAPI/schemas/examples;
- SDK/backend route policy;
- contract/deployment profile;
- tests/conformance evidence.

No single stale example may override the current canonical economics.

---

## 23. Current Normative Summary

A current AIFP-1 implementation MUST, at minimum:

- identify itself as AIFP-1, not generic x402;
- use HTTP `402` for payment-required merchant access;
- use the current reference prices when selecting the standard preset tiers;
- enforce AIFP-1 economics `100/0`;
- verify settlement before receipt issuance;
- fail before payment when the selected settlement route cannot be verified;
- bind payment/receipt to merchant and resource/scope;
- use exact monetary arithmetic;
- reject replay/duplicate settlement consumption;
- keep AIFP-2 `0/0` isolated;
- avoid describing unsupported/unverified routes as payment-live or production-ready.

---

## Appendix A — Current Economics

```text
AIFP-1
  Standard: $0.0005/action
  Complex:  $0.002/action
  Premium:  $0.005/action
  treasuryBps: 100
  creatorBps:  0

AIFP-2/x402
  treasuryBps: 0
  creatorBps:  0
```

## Appendix B — References

- HTTP Semantics / `402 Payment Required`
- Ed25519 / EdDSA
- JSON Web Token / JWKS specifications where used by the receipt profile
- Repository OpenAPI and JSON schema surfaces
- `docs/economics.md` for the current economics summary

## Appendix C — Change Note

**2026-08-15:** Canonical AIFP-1 RFC realigned with the founder-approved August 14 economic model and current product architecture. Superseded microcent tiers and the old `100/1` creator-fee profile are no longer current AIFP-1 guidance. AIFP-2/x402 is explicitly separated as a `0/0` route profile.
