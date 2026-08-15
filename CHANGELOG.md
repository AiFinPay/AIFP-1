# Changelog

All notable changes to this repository are documented here.

This project follows semantic versioning for code artifacts and explicit protocol versioning for AIFP specifications.

## Unreleased

### Added

- Premium repository README with architecture diagrams, navigation, quick starts, and protocol overview.
- Documentation portal structure under `docs/`.
- Repository governance files: contributing guide, security policy, support policy, code of conduct, roadmap, and license.
- GitHub issue templates, pull request template, and workflow skeletons.
- SDK, examples, sandbox, schemas, scripts, assets, and tests entry points.

### Changed

- Repositioned the repository as the official AiFinPay AIFP-1 merchant-monetization protocol home.
- **Canonical economics amendment (2026-08-14):** AIFP-1 reference action tiers are now `standard=$0.0005`, `complex=$0.002`, `premium=$0.005`; the current AIFP-1 fee profile is exactly `100/0` (1% AiFinPay, 0 bps creator/referral), while AIFP-2/x402 is a separate `0/0` AiFinPay fee profile.
- Superseded current-looking microcent pricing and non-zero creator/referral fee examples across the active documentation surfaces. Historical changelog entries below are retained as historical evidence and do not define current economics.

### Security & Architecture Audit (2026-07-24)

Applied fixes from `AUDIT_REPORT.md` (P0/P1/P2 + Track A):

- **Pricing (historical):** at that time, the repository de-duplicated `PricingTier` to `[standard, complex, premium]` and replaced older example amounts with then-canonical minimums (`0.00001/0.00006/0.00010`). **Those values were superseded on 2026-08-14 by `0.0005/0.002/0.005`.**
- **Webhooks:** aligned JSON Schema to HMAC-SHA256 + `AIFP-Signature` (was incorrectly Ed25519/JWKS); unified the event-type enum with the RFC.
- **Receipt header:** standardized on `Payment-Receipt` (removed `X-AIFP-Receipt` split).
- **Verification:** gated `/v1/verify` as an optional fallback (DoS note added); added `required_amount` to `VerifyRequest`; replaced float amount comparisons with decimal/integer arithmetic in the reference pseudocode and all framework examples; enforced nonce `minLength: 22` (≥128 bits) in schemas.
- **Schemas:** aligned Payment Challenge field names to the RFC (`version`/`scheme`/`quote_endpoint`/`estimated_amount`); made `pricing_tier` required in `QuoteRequest`; added optional `quota` claim; relaxed `decimalUsd` for settlement/budget fields via a new `monetaryUsd` definition.
- **Cross-references:** fixed dangling `§38/§42` anchors; marked `/.well-known/aifp` and CWT/COSE receipts as Future Extensions; documented the revoked-receipt residual risk in degraded mode; unified the JWKS path to `/.well-known/jwks.json`.

Open (deferred to AIP / conformance program): settlement-risk circuit breaker (L1), publishable-key split (L4), conformance runner (L3, ROADMAP v0.4).

## 0.1.0 - 2026-06-28

### Added

- Initial AIFP documentation entrypoint.
- Repository architecture document.
