# Conformance

Conformance defines what it means for an implementation to correctly support the **AIFP-1 merchant-monetization profile**. It is evidence-based and route-specific; this repository does not claim that a formal certification program already exists.

## Required AIFP-1 Properties

| Implementer | Minimum requirements |
|---|---|
| Merchant | AIFP-1 `402` challenge, gross resource/pricing policy, local receipt validation, atomic replay/quota handling, fail-closed access |
| Agent/client | Distinguish AIFP-1 from AIFP-2/x402, validate gross-inclusive `100/0` and 99/1/0 conservation, enforce budget against gross before signing, sign/broadcast locally, reconcile `tx_ref`, avoid duplicate spend |
| Wallet | Local key custody for the non-custodial flow, route/asset policy, exact gross amount construction, concurrency-safe budget behavior where promised |
| Quote/verifier backend | Refuse unverifiable or fee-on-top routes before payment, bind gross/merchant/protocol-fee/creator amounts, verify actual settlement, issue receipt only after success, preserve idempotency |
| SDK | Typed gross/split route objects, exact monetary handling, canonical deployment/route selection, route isolation, explicit unsupported/economics-mismatch errors |
| Ledger/reconciliation | Record gross/merchant/treasury/creator amounts, settlement identity/finality, duplicate/reorg corrections, detect economics mismatch |

## Current Economics Assertions

AIFP-1 conformance tests must assert:

```text
standard gross = $0.0005/action
complex gross  = $0.002/action
premium gross  = $0.005/action
payer_total_amount = gross_amount
treasuryBps = 100
creatorBps  = 0
protocol_fee_amount = 1% of gross
creator_amount = 0
merchant_amount = gross_amount - protocol_fee_amount
merchant_amount + protocol_fee_amount + creator_amount = gross_amount
```

Reference Standard split:

```text
$0.0005 gross → $0.000495 merchant + $0.000005 AiFinPay + $0 creator
```

For a 6-decimal asset: `500 gross → 495 merchant + 5 AiFinPay`.

A fee-on-top result such as payer `505` for a Standard `500`-unit gross quote is **not conformant**, even if the configured BPS values are `100/0`.

AIFP-2/x402 conformance is separate and must assert AiFinPay `0/0` rather than reusing AIFP-1.

## Minimum Test Areas

- AIFP-1 challenge classification and shape.
- Binding quote merchant/resource/scope/expiry.
- Gross payer amount and explicit merchant/protocol-fee/creator breakdown.
- `payer_total_amount = gross_amount`.
- `merchant + protocol fee + creator = gross` using exact decimal/base-unit arithmetic.
- Standard/Complex/Premium exact 99/1/0 examples.
- Verifier-readiness gate before payment.
- Fee-on-top route rejected before signing/payment.
- Local payer signing and settlement reference submission.
- Actual settlement verification: route, target, asset, gross amount, split, payment binding, finality.
- Gross-inclusive `100/0` accepted; legacy `100/1` rejected for current AIFP-1.
- Exact decimal/base-unit handling and supported asset decimals.
- Payment idempotency and duplicate settlement rejection.
- Receipt signature, issuer, audience, scope, expiry, gross amount/quota validation.
- Atomic quota/replay behavior under concurrency.
- Budget behavior under parallel calls and process restart where durability is promised.
- AIFP-1/AIFP-2 route mismatch fails closed.
- Gateway/webhook security where those implementation surfaces are used.

## Route Evidence

A chain/asset route should only be called `payment-live` after evidence ties together:

1. exact source/release commit;
2. canonical contract/program/settlement target;
3. supported asset and decimals;
4. current AIFP-1 gross-inclusive economic profile;
5. quote showing payer gross and 99/1/0 split;
6. SDK transaction construction that settles exactly gross;
7. settlement verifier that checks the actual split;
8. CI/tests and appropriate independent review;
9. end-to-end `402 → gross quote → gross settlement → 99/1 verification → receipt → access → replay rejection` evidence;
10. ledger/reconciliation evidence where financial state is maintained.

A raw network deployment count is not a conformance result.

## Future Certification

A future public certification suite may generate machine-readable conformance reports, but until such a program actually exists, use precise claims such as `E2E verified` or `passes repository conformance tests` rather than an invented certification badge.
