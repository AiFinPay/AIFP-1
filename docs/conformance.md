# Conformance

Conformance defines what it means for an implementation to correctly support the **AIFP-1 merchant-monetization profile**. It is evidence-based and route-specific; this repository does not claim that a formal certification program already exists.

## Required AIFP-1 Properties

| Implementer | Minimum requirements |
|---|---|
| Merchant | AIFP-1 `402` challenge, resource/pricing policy, local receipt validation, atomic replay/quota handling, fail-closed access |
| Agent/client | Distinguish AIFP-1 from AIFP-2/x402, validate `100/0`, enforce budget before signing, sign/broadcast locally, reconcile `tx_ref`, avoid duplicate spend |
| Wallet | Local key custody for the non-custodial flow, route/asset policy, exact amount construction, concurrency-safe budget behavior where promised |
| Quote/verifier backend | Refuse unverifiable routes before payment, verify actual settlement, issue receipt only after success, preserve idempotency |
| SDK | Typed route objects, exact monetary handling, canonical deployment/route selection, route isolation, explicit unsupported-version errors |
| Ledger/reconciliation | Separate merchant/treasury/creator amounts, settlement identity/finality, duplicate/reorg corrections, detect economics mismatch |

## Current Economics Assertions

AIFP-1 conformance tests must assert:

```text
standard = $0.0005/action
complex  = $0.002/action
premium  = $0.005/action
treasuryBps = 100
creatorBps  = 0
```

AIFP-2/x402 conformance is separate and must assert AiFinPay `0/0` rather than reusing AIFP-1.

## Minimum Test Areas

- AIFP-1 challenge classification and shape.
- Binding quote merchant/resource/scope/expiry.
- Verifier-readiness gate before payment.
- Local payer signing and settlement reference submission.
- Actual settlement verification: route, target, asset, amount, payment binding, finality.
- `100/0` accepted; legacy `100/1` rejected for current AIFP-1.
- Exact decimal/base-unit handling and supported asset decimals.
- Payment idempotency and duplicate settlement rejection.
- Receipt signature, issuer, audience, scope, expiry, amount/quota validation.
- Atomic quota/replay behavior under concurrency.
- Budget behavior under parallel calls and process restart where durability is promised.
- AIFP-1/AIFP-2 route mismatch fails closed.
- Gateway/webhook security where those implementation surfaces are used.

## Route Evidence

A chain/asset route should only be called `payment-live` after evidence ties together:

1. exact source/release commit;
2. canonical contract/program/settlement target;
3. supported asset and decimals;
4. current AIFP-1 economic profile;
5. SDK transaction construction;
6. settlement verifier;
7. CI/tests and appropriate independent review;
8. end-to-end `402 → quote → settlement → verification → receipt → access → replay rejection` evidence;
9. ledger/reconciliation evidence where financial state is maintained.

A raw network deployment count is not a conformance result.

## Future Certification

A future public certification suite may generate machine-readable conformance reports, but until such a program actually exists, use precise claims such as `E2E verified` or `passes repository conformance tests` rather than an invented certification badge.
