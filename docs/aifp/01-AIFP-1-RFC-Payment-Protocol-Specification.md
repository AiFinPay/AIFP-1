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

| Route class | AiFinPay protocol fee | Creator/referral fee | Settlement semantics | Purpose |
|---|---:|---:|---|---|
| **AIFP-1** | `100` bps / **1%** | `0` bps | **Gross-inclusive:** 99% merchant + 1% AiFinPay | Merchant AI-traffic/resource monetization |
| **AIFP-2/x402** | `0` bps / **0%** | `0` bps | Provider receives the quoted amount | Separate agent-payment route |

For AIFP-1, the commercial price shown or quoted to the payer is the **gross amount**. The 1% AiFinPay protocol fee is deducted from that gross amount; it MUST NOT be added on top of the AIFP-1 action price.

An implementation MUST NOT silently substitute one route profile for the other.

### 1.2 Current reference action tiers

| Tier | Gross reference price paid by agent | Typical workload |
|---|---:|---|
| `standard` | `$0.0005` | Simple read, single record, lightweight API request |
| `complex` | `$0.002` | Search, aggregation, multi-source query, higher compute |
| `premium` | `$0.005` | AI inference, GPU workload, deep analytics, premium data |

These are current AiFinPay reference tiers. The reference price is the gross commercial amount before the AIFP-1 99/1 split and excludes external network/gas costs. A merchant-facing implementation MUST make the effective quoted gross price machine-readable and deterministic. Any future custom/dynamic pricing rules require an explicit protocol/profile update and MUST NOT be inferred from superseded examples.

---

## 2. Requirements Language

The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHOULD**, **SHOULD NOT**, and **MAY** are normative when written in uppercase.

---

## 3. Roles

- **Agent / Payer:** software requesting a protected merchant resource and executing payment according to its own wallet/budget policy.
- **Merchant:** provider of the protected resource and beneficiary of the merchant portion of the gross AIFP-1 amount.
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
3. **Gross amount and split are explicit.** The quote MUST identify the gross payer amount, merchant amount, AiFinPay protocol-fee amount, creator/referral amount, and selected economic profile.
4. **Current AIFP-1 economics are gross-inclusive `100/0`.** The agent pays the gross quoted amount; AiFinPay receives exactly 1% of gross; creator/referral receives zero; the merchant receives the remaining 99% before external network/settlement costs. The 1% MUST NOT be added on top of the AIFP-1 quoted action price.
5. **AIFP-2 is isolated.** AIFP-2 `0/0` payments MUST NOT fall back to fee-bearing AIFP-1 or legacy splitter routes.
6. **Replay/idempotency is enforced.** Reusing a unique payment/settlement identifier outside its allowed semantics MUST fail closed.
7. **Resource access is scoped.** A receipt MUST NOT unlock a merchant/resource/scope it was not issued for.
8. **Exact arithmetic.** Monetary values MUST use integer minor units or exact decimal representations, not binary floating point.
9. **Deployment does not imply payment-live.** A network/contract address alone is insufficient evidence that an AIFP-1 route is safe to quote.
10. **Historical economics are not active economics.** Legacy `100/1`, fee-on-top AIFP-1 semantics, or earlier price examples MAY be retained as audit evidence only when clearly marked legacy/superseded.
11. **Pre-payment policy cannot become a post-payment receipt veto.** Budget/policy and quote-validity decisions MUST be resolved before a new settlement is authorized or initiated. A valid settlement matching an already-issued payable quote MUST NOT lose its receipt entitlement solely because a budget threshold is discovered or wall-clock verification occurs after quote expiry.

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
- pricing tier or effective gross price basis;
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

`reference_price_usd` is the gross reference price paid by the agent, not a merchant-net amount.

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
- `gross_amount`: the commercial amount the payer settles for the AIFP-1 action, excluding external gas/network cost;
- `merchant_amount`: the 99% merchant share derived from gross;
- `protocol_fee_amount`: the 1% AiFinPay share derived from gross;
- `creator_amount`: zero under the current profile;
- `payer_total_amount`: the settlement-rail amount paid by the payer, which MUST equal `gross_amount` for current AIFP-1 economics;
- AiFinPay fee profile (`treasury_bps = 100`);
- creator/referral profile (`creator_bps = 0`);
- asset/token;
- chain/network or settlement rail;
- canonical contract/program/address where applicable;
- unique payment/order binding;
- quote expiry;
- verifier capability/version identifier when applicable.

A current AIFP-1 quote MUST satisfy:

```text
protocol_fee_amount = gross_amount × 1%
creator_amount      = 0
merchant_amount     = gross_amount - protocol_fee_amount
payer_total_amount  = gross_amount
merchant_amount + protocol_fee_amount + creator_amount = gross_amount
```

The actual base-unit calculation MUST use exact integer arithmetic and the selected asset decimals.

### 6.2 Reference pricing

When a merchant selects the standard reference tiers, the quote MUST use these **gross** action prices:

```text
standard = 0.0005 USD/action
complex  = 0.002  USD/action
premium  = 0.005  USD/action
```

Reference split examples:

| Tier | Gross paid by agent | Merchant 99% | AiFinPay 1% |
|---|---:|---:|---:|
| `standard` | `$0.0005` | `$0.000495` | `$0.000005` |
| `complex` | `$0.002` | `$0.00198` | `$0.00002` |
| `premium` | `$0.005` | `$0.00495` | `$0.00005` |

For a 6-decimal settlement asset:

```text
standard: 500 gross units  → 495 merchant + 5 AiFinPay
complex:  2000 gross units → 1980 merchant + 20 AiFinPay
premium:  5000 gross units → 4950 merchant + 50 AiFinPay
```

Batch settlement MAY aggregate many metered actions into one payment. The per-action meter, gross amount, merchant amount, and protocol-fee amount MUST remain mathematically reconcilable.

### 6.3 Verifier-readiness gate

Before returning a payable quote, the quote service MUST determine that the route is verifiable under the currently deployed verifier.

If the verifier is unavailable, unsupported, stale, or unable to validate the quoted contract/profile, the service MUST fail **before payment** rather than issuing a quote that could strand payer funds without a receipt.

### 6.4 Budget, policy, and quote expiry

Payer/account budget and spend-policy checks MUST be resolved before signing/broadcasting. A budget rejection MAY be returned by the quote/policy layer or locally by the payer SDK/wallet, but MUST NOT be introduced later as a reason to deny receipt for a valid settlement matching an already-issued payable quote.

`expires_at` is an authorization boundary for **starting a new settlement**. A client MUST NOT initiate a new settlement using an expired quote.

Where the selected rail or settlement contract can bind expiry atomically, it SHOULD enforce that validity before value transfer. A payment-live route SHOULD avoid designs in which funds can move and only afterwards be declared invalid solely because the quote expired.

If a settlement matching the quote already succeeded, the later `/v1/pay` request time or receipt-processing time MUST NOT by itself be used to deny receipt. The verifier SHOULD evaluate authoritative settlement/authorization timing evidence when the rail exposes it. If reliable pre-transfer expiry enforcement or timing evidence is unavailable, that limitation MUST be part of the route's risk/readiness assessment; the service MUST NOT manufacture a payer-loss condition by treating delayed verification alone as proof that a previously successful matching settlement is invalid.

---

## 7. Settlement

### 7.1 Non-custodial payer flow

The preferred AIFP-1 crypto flow is non-custodial:

1. quote is issued;
2. payer policy validates budget, route, economics, and quote validity before signing;
3. payer wallet constructs and signs the settlement transaction locally;
4. payer broadcasts the transaction;
5. payer receives a settlement reference/transaction hash;
6. payer submits the quote identifier plus settlement reference to AiFinPay;
7. AiFinPay independently verifies settlement;
8. only then is a receipt issued.

The protocol does not require the payer to expose a private key or recovery phrase to AiFinPay.

### 7.2 AIFP-1 fee semantics

For the current AIFP-1 route profile:

```text
treasuryBps        = 100
creatorBps         = 0
gross payer amount = 100%
AiFinPay fee        = 1% of gross
creator amount      = 0%
merchant amount     = 99% of gross before external network/settlement costs
```

The current AIFP-1 protocol uses **fee-from-gross** semantics. Fee-on-top settlement is not conformant with the current AIFP-1 profile, even if it uses `treasuryBps = 100`. A contract, SDK, quote service, or backend that interprets the displayed action price as the merchant amount and adds 1% on top MUST NOT be marked AIFP-1 payment-live under this specification.

External network/gas costs are separate from the AIFP-1 commercial split and MAY be paid according to the selected rail's transport rules.

A `MAX_TOTAL_FEE_BPS` contract constant, where present, is a **security ceiling**, not the active fee rate.

### 7.3 Small-payment handling

Fee-rounding checks MUST be conditional on a non-zero configured fee leg.

For AIFP-1, a route MAY reject a gross settlement amount too small to produce the required 1% treasury amount under integer arithmetic. Such a minimum MUST be derived from the asset decimals and contract semantics; it MUST NOT rely on an asset-agnostic raw-unit constant that changes economic meaning across token decimal systems.

An implementation MAY batch multiple metered actions so that the gross amount can be split exactly. It MUST NOT solve fee rounding by adding the protocol fee on top of the advertised AIFP-1 action price.

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
- expected `gross_amount` / payer settlement amount;
- expected merchant amount;
- expected AiFinPay protocol-fee amount;
- expected creator/referral amount of zero;
- exact conservation: `merchant + protocol fee + creator = gross`;
- expected `quote_id`, order ID, payment ID, nonce, or equivalent binding;
- selected route economics are AIFP-1 gross-inclusive `100/0`;
- quote-validity/authorization evidence where the selected rail exposes it;
- the settlement has not already been consumed for another receipt.

A verifier MUST NOT pass merely because an RPC call succeeded or because a transaction hash exists.

A verifier also MUST NOT reject an otherwise valid matching settlement solely because budget/policy evaluation or `/v1/pay` processing occurs after payment, or because the later verification timestamp is after quote expiry. Post-payment decisions must be based on settlement validity, finality, quote binding, route economics, replay/idempotency, and any authoritative validity evidence available from the selected rail.

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
- gross amount and/or paid quota semantics;
- merchant/protocol-fee split where the active receipt profile carries settlement economics;
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

The merchant MUST charge/meter the actual requested action at its configured gross weight/price. A wider receipt scope MUST NOT allow a premium action to consume only a standard-action amount.

Metering state MUST be concurrency-safe where double consumption could create financial loss.

---

## 11. Free Access And Policy

Merchants MAY provide free requests or allowlists before requiring payment.

Free-tier identity MUST NOT rely solely on a caller-controlled header such as `AIFP-Agent-Id`; otherwise an agent can rotate identifiers to reset quota. A production implementation SHOULD bind durable quota/policy to a stronger authenticated agent, wallet, session, credential, or equivalent identity mechanism appropriate to the integration.

Paid-spend budget/policy decisions belong before settlement authorization/signing. They MUST NOT be evaluated post-settlement in a way that strands valid payer funds without the receipt entitlement created by a matching payable quote.

---

## 12. Idempotency And Replay Protection

Quote, payment, receipt, and webhook processing SHOULD use unique identifiers and idempotent state transitions.

Required behavior includes:

- duplicate settlement consumption does not create a second receipt entitlement;
- retries of the same idempotent request return the same logical result or a deterministic conflict;
- cross-merchant and cross-resource receipt reuse fails;
- an expired quote cannot authorize a **new** settlement;
- an already-successful matching settlement remains reconcilable according to Section 6.4 rather than being rejected solely because verification happens after quote expiry;
- expired receipts fail according to the active receipt profile;
- settlement identifiers are unique in the financial ledger/reconciliation layer.

After an ambiguous transport/process failure where a broadcast may already have occurred, the client MUST reconcile the existing quote/payment/transaction identity before authorizing another spend.

---

## 13. Error Semantics

Implementations SHOULD return machine-readable error bodies.

Recommended classes:

| HTTP | Meaning |
|---|---|
| `400` | malformed request |
| `401` | missing/invalid API authentication where applicable |
| `402` | AIFP-1 payment required |
| `403` | pre-payment budget/policy restriction, or receipt authorization failure on protected access |
| `409` | replay/idempotency/duplicate conflict |
| `410` | quote no longer authorizes a new settlement under its validity rules |
| `422` | settlement/receipt/economic split mismatch |
| `425` | settlement observed but not sufficiently final |
| `429` | rate/policy limit |
| `5xx` | service/route unavailable; MUST NOT imply payment success |

An implementation MUST distinguish **pending** settlement from **invalid** settlement.

`403` budget/policy rejection MUST occur before signing/broadcasting. `/v1/pay` MUST NOT use a newly discovered budget threshold as the sole reason to deny a receipt for an otherwise valid settlement matching an already-issued payable quote.

`410` MUST NOT be returned solely because `/v1/pay`, finality, or receipt processing happens after `expires_at`. Quote expiry prevents initiating a new settlement; successful matching settlements are handled according to the validity rules in Section 6.4. Where a selected settlement mechanism can enforce expiry atomically, it SHOULD reject before funds move.

A `5xx` after a possible or confirmed broadcast MUST lead the client to reconcile/retry verification of the **same** settlement reference before any replacement payment is considered.

---

## 14. Route Registry And Deployment Provenance

For each payment-live chain/route, implementations SHOULD maintain a canonical registry containing:

- chain/network ID;
- contract/program/address;
- contract version/ABI/IDL identifier;
- runtime/source provenance where available;
- economic profile and gross-vs-net semantics;
- supported assets and decimals;
- verifier capability;
- quote-expiry enforcement/timing capability where relevant;
- activation/review status.

A legacy fee-bearing splitter or historical deployment MUST NOT be automatically selected for new AIFP-2 traffic and MUST NOT be presented as current AIFP-1 gross-inclusive `100/0` unless its actual deployed behavior matches the 99/1 fee-from-gross profile.

---

## 15. Ledger And Reconciliation

Financial state SHOULD be durable and append-only or equivalently auditable.

A canonical ledger entry SHOULD record enough information to reconcile:

- route class;
- quote/payment/receipt IDs;
- quote validity/expiry metadata where required for settlement reconciliation;
- gross payer amount;
- merchant amount;
- AiFinPay fee amount;
- creator/referral amount;
- asset and decimals;
- chain/network;
- transaction hash and event/instruction identity;
- finality state;
- reversal/reorg correction where applicable.

For current AIFP-1, reconciliation MUST be able to prove:

```text
payer_settlement_amount = gross_amount
merchant_amount + AiFinPay_fee_amount + creator_amount = gross_amount
AiFinPay_fee_amount = 1% of gross under exact base-unit arithmetic
creator_amount = 0
```

Any fee-on-top result is an AIFP-1 economics mismatch.

A verifier outage, delayed finality, or delayed `/v1/pay` call MUST NOT cause the system to forget or replace a settlement that may already have moved value. Reconciliation must preserve the original settlement identity until it reaches a deterministic valid/invalid/finality outcome.

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
- current AiFinPay economics `100/0`;
- action price is gross; 99% merchant / 1% AiFinPay / 0% creator.

### AIFP-2/x402

- separate x402-compatible agent payment route;
- current AiFinPay economics `0/0`;
- provider/merchant receives the quoted amount; AiFinPay adds no protocol percentage;
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
- post-payment budget/expiry denial that can strand valid payer funds;
- gross/net/fee semantic mismatch;
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
   - pre-payment budget/policy approval against gross;
   - binding quote with explicit gross, merchant, protocol-fee, and creator amounts;
   - expired quote rejected before initiating a new settlement;
   - payer settlement equal to the quoted gross amount;
   - verifier confirmation using the same settlement reference through pending/retry states;
   - no receipt denial solely because budget or wall-clock verification occurs after a valid settlement;
   - merchant amount exactly 99% of gross under the selected asset/base-unit arithmetic;
   - AiFinPay fee exactly 1% of gross;
   - creator/referral amount zero;
   - conservation `merchant + fee + creator = gross`;
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
- AIFP-1 `100/1` or any `0.01%` creator/referral leg;
- AIFP-1 fee-on-top behavior where the displayed/quoted action price is treated as the merchant amount and 1% is added above it.

Historical documents, transaction evidence, or deployment manifests MAY retain these values only when clearly labeled **legacy/historical/superseded**.

New AIFP-1 guidance MUST use `$0.0005 / $0.002 / $0.005`, gross-inclusive `100/0`, and the 99/1 split defined in this RFC.

Historical interface behavior that applied `AIFP-403-BUDGET-EXCEEDED` at `/v1/pay` after payer settlement is also superseded. Current budget/policy rejection is pre-payment only.

---

## 21. Machine-Readable Contracts

The machine-readable surfaces of this repository must remain consistent with this RFC:

- OpenAPI 3.1 specification;
- JSON schema documentation/examples;
- Postman collection;
- SDK/reference examples;
- `.well-known` discovery metadata where present.

A CI/conformance check SHOULD fail when active documentation reintroduces superseded economics, fee-on-top AIFP-1 semantics, ambiguous use of the reference tier as `merchant_amount`, or post-payment policy semantics that can strand a valid matching settlement.

---

## 22. Governance

Changes to normative AIFP-1 behavior SHOULD be proposed and reviewed through the repository's AIP/governance process.

Economic or payer-loss-sensitive lifecycle changes require explicit review and coordinated updates to:

- normative RFC;
- economics document when economics are affected;
- OpenAPI/schemas/examples;
- SDK/backend route and policy logic;
- contract/deployment profile where settlement semantics are affected;
- tests/conformance evidence.

No single stale example may override the current canonical economics or lifecycle safety rules.

---

## 23. Current Normative Summary

A current AIFP-1 implementation MUST, at minimum:

- identify itself as AIFP-1, not generic x402;
- use HTTP `402` for payment-required merchant access;
- use the current reference prices as gross payer prices when selecting the standard preset tiers;
- enforce AIFP-1 gross-inclusive `100/0` economics;
- ensure payer settlement amount equals gross quoted amount, not gross plus a protocol fee;
- derive merchant amount as 99% of gross and AiFinPay amount as 1% of gross under exact asset/base-unit arithmetic;
- keep creator/referral amount at zero;
- resolve budget/policy and quote-validity decisions before initiating a new settlement;
- never deny receipt for an otherwise valid matching settlement solely because a budget threshold is discovered after payment;
- never use the later verification time alone as the reason to reject an otherwise valid matching settlement after quote expiry;
- verify settlement before receipt issuance;
- fail before payment when the selected settlement route cannot be verified;
- reconcile the same settlement reference across pending/verifier-unavailable states before any replacement payment;
- bind payment/receipt to merchant and resource/scope;
- use exact monetary arithmetic;
- reject replay/duplicate settlement consumption;
- keep AIFP-2 `0/0` isolated;
- avoid describing unsupported/unverified routes as payment-live or production-ready.

---

## Appendix A — Current Economics

```text
AIFP-1
  Standard gross: $0.0005/action  → merchant $0.000495 + AiFinPay $0.000005
  Complex gross:  $0.002/action   → merchant $0.00198  + AiFinPay $0.00002
  Premium gross:  $0.005/action   → merchant $0.00495  + AiFinPay $0.00005
  treasuryBps: 100
  creatorBps:  0
  payer settlement amount: gross
  fee-on-top: not permitted

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

**2026-08-15:** Canonical AIFP-1 RFC realigned with the founder-approved August 14 economic model and clarified as strictly gross-inclusive. The AIFP-1 displayed/quoted action price is the gross payer amount; 1% AiFinPay is deducted from gross and the merchant receives 99%. Fee-on-top AIFP-1 semantics, superseded microcent tiers, and the old `100/1` creator-fee profile are not current AIFP-1 guidance. AIFP-2/x402 remains explicitly separated as a `0/0` route profile.

**2026-08-15 lifecycle safety audit:** Budget/policy and quote-expiry decisions were made explicitly pre-payment. `/v1/pay` is a post-payment settlement-verification endpoint and cannot use a newly discovered budget threshold or delayed verification timestamp as a standalone reason to strand a valid matching settlement without its receipt entitlement. Pending/verifier-unavailable states must reconcile the same settlement reference before any replacement payment.
