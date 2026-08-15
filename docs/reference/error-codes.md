# Error Codes

This table uses the public registry codes currently documented in the repository. Bridge-specific codes are maintained in the related bridge implementations and are not listed as part of this public registry page.

## Verification Scope

- Public registry codes are sourced from the AIFP documents in this repository.
- Bridge implementation codes should be verified in the corresponding bridge repositories.
- SDK wrapper errors should map back to the documented `AIFP-*` registry where possible.
- Error handling must preserve the protocol lifecycle: policy rejection before payment, settlement verification after payment.

## Registry

| Code | Meaning | Typical reason | What to do |
|---|---|---|---|
| `AIFP-400` | Bad request | Missing field, invalid JSON, malformed challenge | Fix the request shape and retry |
| `AIFP-401` | Unauthorized | Missing or invalid API authentication where required | Supply valid authentication for the active environment |
| `AIFP-402` | Payment required | Protected resource needs AIFP-1 payment | Request a binding quote, settle the gross amount, verify settlement, then retry with the receipt |
| `AIFP-402-ONBOARDING` | Payment required plus onboarding | Agent does not yet speak AIFP | Return onboarding guidance without charging the payer |
| `AIFP-403` | Forbidden | Pre-payment policy/account restriction | Resolve policy/account status before payment |
| `AIFP-403-BUDGET-EXCEEDED` | Budget exceeded | Proposed gross payment would exceed a payer/account policy | Reject before signing/broadcasting; raise the budget or wait for the next window |
| `AIFP-404` | Not found | Quote, receipt, merchant, or resource not found | Re-check IDs and endpoints |
| `AIFP-409` | Conflict | Receipt replay, duplicate settlement consumption, or idempotency conflict | Reconcile existing state; do not blindly send another payment |
| `AIFP-410` | Gone / expired | Quote expired | Request a fresh quote before payment |
| `AIFP-422-SIGNATURE` | Invalid receipt signature | Verification-key mismatch, stale key ID, or tampered receipt | Refresh trusted verification keys and verify again |
| `AIFP-422-AMOUNT` | Settlement/amount mismatch | Gross payer amount or 99/1/0 split does not match the binding quote | Treat payment as mismatch and reconcile; do not issue receipt automatically |
| `AIFP-425` | Settlement pending | Settlement observed but required finality not reached | Honor retry guidance and reconcile the same settlement reference |
| `AIFP-429` | Rate limited | Too many requests in a window | Back off and retry later |
| `AIFP-5xx` | Server/route error | Merchant, verifier, or gateway failure | If payment may have been broadcast, reconcile before any new spend |

## Budget Lifecycle Rule

`AIFP-403-BUDGET-EXCEEDED` belongs **before payment**:

```text
challenge → budget/policy → quote → sign/broadcast → settlement verification → receipt
             ↑ reject here, not after valid settlement
```

For AIFP-1, budget comparisons use the **gross payer amount**. Once a payer has executed a settlement that matches an already-issued payable quote, `/v1/pay` must not deny the corresponding receipt solely because a budget threshold was crossed. At that stage the service validates settlement, finality, quote binding, economics, replay and idempotency.

## SDK Mapping

SDKs should expose typed equivalents for at least budget rejection, invalid receipt, quote expiry, unsupported/verifier-unready route, economics mismatch, settlement pending, replay/idempotency conflict, and rate limiting.

See [SDK Reference](../aifp/11-SDK-Reference.md) for the current AIFP-1 client behavior.
