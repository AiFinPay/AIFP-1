---
aip: TBD
title: Merchant-specific AIFP-1 gross-inclusive fee profiles
author: AiFinPay maintainers
type: Standards Track
category: Economics
status: Draft
created: 2026-11-27
updated: 2026-11-27
requires: 2, 19
---

## Abstract

Introduce a versioned AIFP-1 settlement profile with an individually negotiated AiFinPay treasury fee between 100 and 500 basis points inclusive (1%–5%). Preserve gross-inclusive pricing and zero creator/referral fees. The active fixed-100-bps baseline remains unchanged until this proposal is accepted, implemented and activated per route.

## Motivation

Different merchant contracts, transaction volumes and integration requirements may justify different rates. A universal fixed rate prevents contractual differentiation. Microtransactions should continue to be settled in the native settlement asset using exact atomic-unit arithmetic, with optional aggregation.

## Specification

The proposed profile identifier is `AIFP1-MERCHANT-FEE-V1`. A merchant-scoped, authenticated configuration record MUST include merchant ID, fee profile ID, immutable revision, treasury_bps (integer 100–500), creator_bps (zero), treasury destination, effective validity and audit reference. Rates may differ between merchants and be updated prospectively by authorized operators under the applicable agreement. Missing, conflicting or ineligible configuration MUST NOT generate a payable quote. No payer or merchant request parameter may override the authoritative assigned rate.

For a quote using this profile, let G be the positive gross settlement amount in token atomic units and B be the agreed treasury_bps.

```text
100 <= B <= 500
F = floor(G * B / 10000)
C = 0
M = G - F
payer_total_atomic = G
M + F + C = G
```

All arithmetic MUST use exact integers, and token decimals MUST come from verified asset metadata. If F is zero, reject before funds move or aggregate authorized usage into a larger payable batch. Do not round a fee upward or add it on top. Effective rate may differ slightly due to atomic-unit rounding; expose the actual amounts. See the [candidate schema](../schemas/merchant-fee-profile-v1.schema.json) and [candidate vectors](../tests/merchant-fee-profile-v1-vectors.json).

The payer sees the gross price, the selected profile revision, fee rate, merchant net, protocol fee, creator amount and exact asset/chain before signing. The authenticated quote and execution authorization MUST bind these values, the merchant and treasury destination, settlement route/deployment, resource, payer, payment identity, expiry and nonce. Receipt verification MUST use the quoted immutable revision and actual settlement events, never the merchant's current fee setting. Receipt claims bind the profile revision, fee and actual split.

Changing a fee requires a new configuration revision for subsequent quotes. An already authorized quote MUST either execute exactly its bound economics within its validity rules or fail atomically before funds move; a valid completed settlement MUST remain verifiable even after a rate change. Preserve the pre-payment budget/expiry safety rules of AIP-19. Disabled or expired unexecuted routes MUST fail before payment.

### Batches

Batch only compatible payment obligations with the same payer authorization, merchant, asset/chain, destination and fee revision. The quote MUST bind each underlying metered obligation or a deterministic commitment, gross batch amount, fee and allocation rules; reconcile every receipt and reject duplicates. Apply floor rounding once to the batch and distribute actual fee/net amounts deterministically, conserving the batch totals. Do not pool unrelated merchants' assets, or create unapproved stored-value custody. Use prepaid resource entitlements or another explicitly authorized and secured payment mechanism; do not assume unsecured deferred payment.

## Protocol / Route Scope

AIFP-1 only. AIFP-2/x402 remains its current separate 0/0 provider-preserving profile. No fee-on-top, creator/referral fee, pricing tier, native token, Bridge tariff, or fiat settlement change. AIFP-6 can record the actual settlement and AIFP-3 identity where verified, without imposing passports on baseline interoperable clients.

## Backward Compatibility

MINOR only as a negotiated opt-in profile with a distinct version and no change to legacy wire semantics. Enabling it on an existing route without explicit negotiation is a breaking behavior change and is prohibited. Historical quotes and receipts remain valid according to their original profile. The current fixed-100-bps profile is not silently reinterpreted. Legacy verifiers and SDKs MUST reject unknown profiles before payment.

## Migration Plan

1. Accept and assign an AIP number through the repository governance process.
2. Synchronize the RFC, economics guide, OpenAPI, JSON Schemas, discovery, Postman, SDK docs, examples, conformance checks and public developer guidance. Preserve fixed-rate examples explicitly labeled legacy or example-only; advertise supported range/profile rather than a universal rate.
3. Backend: add immutable, merchant-scoped profile revisions, authenticated configuration and audit history; quote, receipt and verifier use exact bound rate and split. Test cross-tenant access and rate changes.
4. Contract: audit the deployed route registry and splitter. Current v1.4 source has MAX_TREASURY_BPS=500 but mutable route profiles; a signed route ID alone does not bind immutable economics. Implement and review immutable versioned routes or a new signed quote format that enforces expected rate/split and treasury destination atomically. Protect all effective treasury changes and routes. Do not mutate old route economics while quotes remain executable.
5. Synchronize SDK/MCP, AIFP-6 evidence and settlement registry; run sandbox and independent security review before enabling a new route. Production enablement is a separate explicit decision.

## Security Considerations

Reject out-of-range/fractional rates, wrong merchant, stale revisions, tampered quotes, unknown profile versions, incompatible asset decimals, creator fees, unexpected treasury destination, nonce/replay conflicts and split mismatches. Do not infer active fees from a security ceiling. No secrets or live configuration belong in this proposal. Keep reconciliation and historical settlement evidence intact.

## Reference Implementation

The candidate JSON Schema describes a proposed economics envelope, not the complete existing quote/receipt or a deployed endpoint. Candidate arithmetic vectors and a dependency-free checker demonstrate the proposed rule only. Cross-field semantics, authentication, policy and actual contract behavior require integration tests.

## Test / Conformance Evidence

Run `python scripts/check-merchant-fee-profile.py` for candidate arithmetic vectors and `python scripts/check-economics.py` for the unchanged legacy profile. Additional release gates: 100/250/500 bps, rate boundaries 99/501, atomic rounding and zero fee, two merchant rates, immutable in-flight quote across updates, wrong merchant/treasury, stale profile, replay, batch conservation, AIFP-2 isolation and end-to-end reconciliation.

## Deployment Considerations

No change to live routes, contracts or current fee settings in this draft. Contract and SDK/backend version alignment, supported chain/token verification, audit and production approval are prerequisites.

## Copyright

Apache-2.0 for code artifacts; repository documentation license for prose.
