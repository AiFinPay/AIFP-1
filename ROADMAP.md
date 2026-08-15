# AiFinPay AIFP-1 Roadmap

AIFP-1 is a draft protocol/specification project. The roadmap separates protocol/documentation work from implementation, deployment, conformance, and production authorization.

## Current Baseline

- AIFP-1 merchant monetization uses gross reference prices `$0.0005 / $0.002 / $0.005` for Standard / Complex / Premium.
- AIFP-1 settlement semantics are gross-inclusive `100/0`: payer settles gross, merchant receives 99% of gross, AiFinPay receives 1% of gross, creator/referral receives 0%; the 1% fee is not added on top.
- AIFP-2/x402 is a separate `0/0` AiFinPay fee profile.
- Payer settlement is non-custodial in the preferred crypto flow: local signing/broadcast, then `tx_ref` verification.
- Payable quotes require verifier-ready routes whose gross/net semantics match the quote.
- Receipt issuance follows verified settlement.

Canonical AIFP-1 amount invariant:

```text
payer_total_amount = gross_amount
merchant_amount + protocol_fee_amount + creator_amount = gross_amount
protocol_fee_amount = 1% of gross under exact settlement base-unit arithmetic
creator_amount = 0
```

## Workstreams

| Workstream | Goal | Repository status |
|---|---|---|
| Protocol | Keep RFC/economics/protocol boundaries internally consistent | Draft specification |
| Machine-readable contracts | Keep OpenAPI, schemas, Postman aligned with the RFC and gross/split invariant | Active |
| Documentation | Keep developer surfaces aligned and evidence-based | Active |
| Implementation | Maintain real SDK/backend/contracts in their implementation repositories | External to this repo |
| Conformance | Build repeatable route/profile test vectors and evidence | Planned / partial |
| Governance | Use AIP/repository review process without inventing unevidenced councils/certification bodies | Active process |

## Near-Term Priorities

1. Maintain one canonical gross-inclusive AIFP-1 economics and route model across all active documentation.
2. Keep automated regressions that reject superseded active economics, gross-as-merchant examples, fee-on-top AIFP-1 semantics, and route confusion.
3. Publish/maintain conformance vectors for gross `100/0`, exact 99/1/0 conservation, verifier-before-receipt, replay/idempotency, low-value rounding, and asset decimals.
4. Link actual SDK/backend/contract releases to exact commits and deployment evidence.
5. Prove route-specific end-to-end flows before marking chains/assets payment-live.
6. Keep AIFP-2/x402 and AIFP-3 normative specifications in their own protocol homes.

## Generated Artifacts

Generated PDFs that no longer match the current canonical Markdown are removed rather than left as contradictory protocol copies. PDF distribution may be restored after regeneration is automated from the current canonical sources and checked for drift in CI.

## Conformance Milestone

A useful AIFP-1 conformance bundle should cover:

- challenge classification;
- binding quote with gross, merchant, protocol-fee, creator, and payer-total amounts;
- `payer_total_amount = gross_amount`;
- exact `merchant + protocol fee + creator = gross` conservation;
- Standard/Complex/Premium 99/1/0 vectors;
- fee-on-top rejection before payment;
- verifier readiness before payment;
- local payer signing/broadcast for exactly gross;
- actual settlement verification;
- receipt issuance only after verifier success;
- merchant scope/gross-amount/quota verification;
- replay/idempotency/concurrency behavior;
- asset-decimal and low-value fee-rounding cases;
- explicit AIFP-1/AIFP-2 route isolation.

## Release Milestone

A protocol tag or documentation release does not itself authorize production payments. Production/payment-live claims belong to the relevant implementation release and should include exact source/deployment provenance, verifier support, matching gross-inclusive settlement semantics, tests, appropriate independent review, and end-to-end evidence.

## Non-Goals

- AIFP-1 does not introduce or require a native token.
- AIFP-1 does not require merchants to call AiFinPay synchronously for every receipt verification when local verification is supported.
- AIFP-1 does not replace ordinary HTTP authentication/authorization; it adds paid-access semantics for machine traffic.
- This roadmap does not promise unpublished SDK packages, public sandbox infrastructure, formal certification programs, or a particular number of payment-live networks.
