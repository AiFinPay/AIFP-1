# AiFinPay AIFP-1 Roadmap

AIFP-1 is a draft protocol/specification project. The roadmap separates protocol/documentation work from implementation, deployment, conformance, and production authorization.

## Current Baseline

- AIFP-1 merchant monetization: `$0.0005 / $0.002 / $0.005`, `100/0`.
- AIFP-2/x402: separate `0/0` AiFinPay fee profile.
- Payer settlement is non-custodial in the preferred crypto flow: local signing/broadcast, then `tx_ref` verification.
- Payable quotes require verifier-ready routes.
- Receipt issuance follows verified settlement.

## Workstreams

| Workstream | Goal | Repository status |
|---|---|---|
| Protocol | Keep RFC/economics/protocol boundaries internally consistent | Draft specification |
| Machine-readable contracts | Keep OpenAPI, schemas, Postman aligned with the RFC | Active |
| Documentation | Keep developer surfaces aligned and evidence-based | Active |
| Implementation | Maintain real SDK/backend/contracts in their implementation repositories | External to this repo |
| Conformance | Build repeatable route/profile test vectors and evidence | Planned / partial |
| Governance | Use AIP/repository review process without inventing unevidenced councils/certification bodies | Active process |

## Near-Term Priorities

1. Maintain one canonical AIFP-1 economics and route model across all active documentation.
2. Add automated regressions that reject superseded active economics and route confusion.
3. Publish/maintain conformance vectors for `100/0`, verifier-before-receipt, replay/idempotency, low-value rounding, and asset decimals.
4. Link actual SDK/backend/contract releases to exact commits and deployment evidence.
5. Prove route-specific end-to-end flows before marking chains/assets payment-live.
6. Keep AIFP-2/x402 and AIFP-3 normative specifications in their own protocol homes.

## Generated Artifacts

Generated PDFs that no longer match the current canonical Markdown are removed rather than left as contradictory protocol copies. PDF distribution may be restored after regeneration is automated from the current canonical sources and checked for drift in CI.

## Conformance Milestone

A useful AIFP-1 conformance bundle should cover:

- challenge classification;
- binding quote and current economics;
- verifier readiness before payment;
- local payer signing/broadcast;
- actual settlement verification;
- receipt issuance only after verifier success;
- merchant scope/amount/quota verification;
- replay/idempotency/concurrency behavior;
- asset-decimal and low-value fee-rounding cases;
- explicit AIFP-1/AIFP-2 route isolation.

## Release Milestone

A protocol tag or documentation release does not itself authorize production payments. Production/payment-live claims belong to the relevant implementation release and should include exact source/deployment provenance, verifier support, tests, appropriate independent review, and end-to-end evidence.

## Non-Goals

- AIFP-1 does not introduce or require a native token.
- AIFP-1 does not require merchants to call AiFinPay synchronously for every receipt verification when local verification is supported.
- AIFP-1 does not replace ordinary HTTP authentication/authorization; it adds paid-access semantics for machine traffic.
- This roadmap does not promise unpublished SDK packages, public sandbox infrastructure, formal certification programs, or a particular number of payment-live networks.
