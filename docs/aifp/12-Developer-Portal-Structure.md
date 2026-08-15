# AIFP-1 Developer Portal Structure

**Document:** AIFP-DOC-12  
**Status:** Draft information architecture  
**Governed by:** AIFP-1 repository documentation

This document describes the intended information architecture for AIFP-1 developer documentation. It is a design target, not a claim that every portal feature, package download, sandbox endpoint, or interactive tool already exists.

## 1. Portal Principles

The portal should:

- make **AIFP-1 merchant monetization** the primary subject of this repository;
- separate AIFP-1 from AIFP-2/x402 and AIFP-3 identity;
- render canonical repository content rather than creating a second source of truth;
- generate API/reference pages from OpenAPI and schemas where practical;
- label draft, experimental, verified, and payment-live status precisely;
- avoid showing stale pricing, legacy `100/1`, or fee-on-top AIFP-1 economics as current.

## 2. Current Economics Block

Every relevant pricing page should consistently show that the AIFP-1 action price is the **gross payer amount**, with 1% deducted from gross rather than added on top:

| AIFP-1 item | Current value |
|---|---:|
| Standard gross payer price | `$0.0005` |
| Standard merchant / AiFinPay | `$0.000495` / `$0.000005` |
| Complex gross payer price | `$0.002` |
| Complex merchant / AiFinPay | `$0.00198` / `$0.00002` |
| Premium gross payer price | `$0.005` |
| Premium merchant / AiFinPay | `$0.00495` / `$0.00005` |
| AiFinPay protocol fee | `1%` of gross / `100` bps |
| Creator/referral fee | `0` bps |
| Merchant amount | `99%` of gross before external network/settlement costs |
| Payer settlement | `100%` of gross (`payer_total_amount = gross_amount`) |
| Fee-on-top | Not permitted for current AIFP-1 |

AIFP-2/x402 must be shown separately as a `0/0` AiFinPay fee profile.

## 3. Suggested Information Architecture

```text
AIFP-1 Docs
├── Home
│   ├── What AIFP-1 is
│   ├── Current gross-inclusive economics
│   ├── HTTP 402 flow
│   └── Draft / implementation-status notice
├── Get Started
│   ├── Merchant integration
│   ├── Agent payment flow
│   └── Receipt verification
├── Concepts
│   ├── AIFP-1 vs AIFP-2/x402
│   ├── Payment Challenge
│   ├── Binding Quote
│   ├── Gross / Merchant / Protocol Fee Amounts
│   ├── Non-custodial Settlement
│   ├── Settlement Verification
│   ├── Receipts & Scope
│   ├── Pricing & Metering
│   ├── Budgets & Idempotency
│   └── Route Registry / Deployment Provenance
├── API Reference
│   ├── Quote
│   ├── Settlement verification / Pay
│   ├── Receipt
│   ├── Assisted Verify
│   └── JWKS
├── Machine-Readable
│   ├── OpenAPI 3.1
│   ├── JSON Schemas
│   └── Postman Collection
├── Protocol
│   ├── AIFP-1 RFC
│   ├── Economics
│   ├── Security
│   ├── AIP Process
│   ├── Whitepaper
│   └── Changelog
└── Implementation Status
    ├── SDK/package links verified from actual registries
    ├── Payment-live route evidence
    └── Legacy / deprecated material
```

## 4. Protocol Boundaries In Navigation

The portal must not put Passport APIs or generic x402 migration APIs inside the AIFP-1 API reference unless a page is explicitly describing a cross-protocol integration.

Recommended cross-links:

- AIFP-1 page → "Agent payments via AIFP-2/x402" as a separate protocol link;
- AIFP-1 page → "Agent identity via AIFP-3" as a separate protocol link.

Do not rename AIFP-1's own HTTP `402` challenge as an x402 challenge.

## 5. API Reference

The API reference should be generated from `08-OpenAPI-3.1-Specification.yaml`.

For each operation show:

- request schema;
- response schema;
- gross payer amount and merchant/protocol-fee/creator breakdown where payment-bearing;
- route/profile requirements;
- error cases;
- whether the route is only a protocol definition or currently backed by a verified implementation;
- copyable examples that use current economics.

A "Try it" control should only be enabled when a corresponding environment is actually configured and safe to use. Documentation must not invent test keys or a sandbox/faucet that has not been verified.

## 6. SDK / Package Pages

Package cards must be generated or manually verified against real package registries and source repositories.

Each card should show:

- package name;
- current published version;
- source repository;
- language/runtime;
- supported AIFP route classes;
- supported chains/assets based on current release evidence;
- release date/hash where useful.

Do not list planned Rust/Java/PHP/.NET packages as downloadable merely because the protocol has language examples.

## 7. Chain / Route Status

A network status page should distinguish:

| Status | Meaning |
|---|---|
| `deployed` | some relevant code/contract exists on the network |
| `canonical target identified` | source/address relationship is resolved |
| `verifier ready` | backend can independently verify the selected payment path |
| `SDK ready` | client can construct the correct current route |
| `economics verified` | actual settlement semantics preserve payer gross and the 99/1/0 split |
| `E2E verified` | complete payment evidence bundle exists |
| `payment-live` | explicitly approved for current product use |
| `legacy` | historical/superseded deployment, not selected for current payments |

Never reduce these dimensions to one unsupported "12 chains" or "13 chains live" claim in protocol documentation.

## 8. Search And Cross-Linking

Search should index:

- protocol docs;
- OpenAPI/schema objects;
- error names;
- AIPs;
- changelog;
- route/economics terms such as `gross_amount`, `merchant_amount`, `protocol_fee_amount`, `100/0`, `0/0`, `treasuryBps`, `creatorBps`.

Useful query aliases:

- `402` → AIFP-1 HTTP 402 flow;
- `x402` → AIFP-1 vs AIFP-2 boundary page;
- `1%` → AIFP-1 gross-inclusive economics;
- `0%` → AIFP-2 route link;
- `standard price` → gross `$0.0005`.

## 9. Quality Gates

Portal/document CI should detect:

- broken links;
- invalid OpenAPI;
- malformed JSON/Postman;
- Markdown errors where configured;
- current-product occurrences of superseded `$0.00001 / $0.00006 / $0.00010` pricing;
- current-product `100/1` or `0.01% creator` examples;
- gross Standard `$0.0005` incorrectly used as `merchant_amount`;
- fee-on-top AIFP-1 interpretations;
- contradictory AIFP-1 vs AIFP-2 fee statements.

Historical/changelog/migration sections may retain old values only when explicitly labeled legacy or superseded.

## 10. Security And Secrets

Documentation/examples must never contain:

- private keys;
- recovery phrases;
- live API secrets;
- production signing key material;
- merchant origin secrets;
- reusable authentication tokens.

Examples should use unmistakable placeholders.

## 11. Status Language

Use precise labels:

- `Draft specification` for the protocol document;
- `Reference implementation` only when source exists;
- `Verified deployment` only with deployment evidence;
- `Payment-live` only after the current route passes the required release/conformance gate;
- `Production-ready` only if explicitly approved and evidenced.

The portal is a documentation surface, not proof of production readiness.
