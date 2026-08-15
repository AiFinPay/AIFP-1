# AIFP-1 AI Agent SDK Specification

**Document:** AIFP-DOC-03  
**Audience:** AI-agent/SDK developers  
**Status:** Draft implementation specification  
**Governed by:** [AIFP-1 RFC](./01-AIFP-1-RFC-Payment-Protocol-Specification.md)

This document defines the expected behavior of an AIFP-1-aware agent client. It does not claim that every language package or chain adapter is already released or payment-live.

AIFP-1 is the merchant AI-traffic/resource monetization profile. **AIFP-2/x402 is separate.** A client may support both, but it must classify and route them explicitly.

## 1. Core Behavior

An AIFP-1-aware client handles this loop:

`request → AIFP-1 402 → policy → quote → local settlement → verify → receipt → retry`

The SDK should make payment automation possible without giving the AiFinPay receipt service custody of the payer's private key.

## 2. Current Economics

The AIFP-1 reference action price is the **gross amount paid by the agent**. The 1% AiFinPay protocol fee is deducted from gross; it is not added on top.

| Tier | Gross payer price | Merchant 99% | AiFinPay 1% |
|---|---:|---:|---:|
| `standard` | `$0.0005` | `$0.000495` | `$0.000005` |
| `complex` | `$0.002` | `$0.00198` | `$0.00002` |
| `premium` | `$0.005` | `$0.00495` | `$0.00005` |

A valid current AIFP-1 quote uses:

```text
routeClass          = AIFP-1
treasuryBps         = 100
creatorBps          = 0
payerTotalAmount    = grossAmount
protocolFeeAmount   = 1% of gross
creatorAmount       = 0
merchantAmount      = grossAmount - protocolFeeAmount
```

AIFP-2/x402 uses `0/0`. A client MUST NOT silently substitute route classes or convert an AIFP-1 gross price into a merchant-net price plus an added fee.

## 3. 402 Detection

HTTP status `402` alone does not prove the response is AIFP-1 or x402.

The client should inspect protocol-specific metadata. An AIFP-1 challenge should identify itself as AIFP-1 or provide enough AIFP-specific structure to classify it safely.

If the response is an unsupported payment protocol/version, the client must report that explicitly instead of guessing a payment path.

## 4. Payment State Machine

```mermaid
stateDiagram-v2
    [*] --> Requesting
    Requesting --> Done: non-payment response
    Requesting --> Challenged: AIFP-1 402
    Challenged --> PolicyCheck
    PolicyCheck --> Rejected: budget/policy fails
    PolicyCheck --> Quoting: allowed
    Quoting --> Rejected: route/profile/gross split mismatch
    Quoting --> Signing: verifier-ready gross-inclusive AIFP-1 quote
    Signing --> Broadcasting
    Broadcasting --> Verifying: tx_ref obtained
    Verifying --> Pending: finality pending
    Pending --> Verifying
    Verifying --> Receipted: settlement verified
    Verifying --> Rejected: settlement mismatch
    Receipted --> Replaying
    Replaying --> Done: protected response
    Replaying --> Rejected: repeat payment challenge after configured limit
```

The SDK must not enter `Signing/Broadcasting` if the quote says the route is unsupported/unverifiable or if the route economics are not gross-inclusive AIFP-1.

## 5. Quote Validation

Before signing anything, validate the binding quote:

- protocol/route class is `AIFP-1`;
- merchant matches the challenge/request;
- resource/scope is expected;
- quote is not expired;
- `grossAmount` is within caller policy;
- `payerTotalAmount === grossAmount` under exact arithmetic;
- `treasuryBps === 100`;
- `creatorBps === 0`;
- `creatorAmount === 0`;
- `merchantAmount + protocolFeeAmount + creatorAmount === grossAmount` in exact settlement units;
- `protocolFeeAmount` is exactly the required 1% share under the selected asset/base-unit arithmetic;
- asset/chain is permitted by caller policy;
- settlement target is trusted/canonical for the selected route when a registry is used;
- verifier readiness/capability is present when required by the implementation.

If any required binding fails, do not pay. In particular, a quote or target that adds 1% above the displayed/quoted AIFP-1 action price MUST be rejected.

Canonical Standard example:

```json
{
  "gross_amount": "0.0005",
  "payer_total_amount": "0.0005",
  "merchant_amount": "0.000495",
  "protocol_fee_amount": "0.000005",
  "creator_amount": "0",
  "treasury_bps": 100,
  "creator_bps": 0
}
```

## 6. Non-Custodial Settlement

The default crypto flow keeps signing local:

```text
quote
  ↓
SDK validates gross amount + 99/1/0 split
  ↓
SDK builds transaction / wallet request for exactly gross amount
  ↓
payer wallet signs locally
  ↓
payer broadcasts
  ↓
tx_ref / settlement reference
  ↓
POST /v1/pay for independent verification
  ↓
receipt only after verifier success
```

A client must never send a recovery phrase/private key/raw signer secret as part of `POST /v1/pay`.

## 7. Settlement Construction

The SDK must construct the call appropriate to the **actual canonical deployment version** for the selected chain/asset.

It should not infer the ABI/IDL from a stale version string alone. A deployment registry, when used, should bind at least:

- network/chain ID;
- contract/program address;
- implementation/version identifier;
- supported payment entrypoint;
- fee profile;
- gross-vs-net settlement semantics;
- supported asset/token metadata;
- verifier status/provenance.

Legacy `100/1` splitters and fee-on-top implementations must not be selected for current AIFP-1 payments. A target with `treasuryBps=100` is not sufficient evidence of compatibility unless its actual transfer semantics preserve `payer total = gross` and the 99/1/0 split.

## 8. Monetary Arithmetic

Use integer token units or exact decimal arithmetic.

Do not use JavaScript/Python/other binary floats to decide whether a settlement paid enough or whether the split is correct.

Token-decimal conversion must be based on the actual token decimals for the selected chain/asset. A 6-decimal token and an 18-decimal token cannot share a hard-coded raw-unit divisor unless the conversion explicitly normalizes them.

Where practical, validate in settlement base units:

```text
payer_total = gross
merchant + protocol_fee + creator = gross
```

## 9. Budget Control

Budget policy is checked before signing/broadcasting against the **gross payer amount**, with separately disclosed network/gas costs handled according to caller policy.

Recommended limits include:

- per payment;
- rolling/daily spend;
- per merchant;
- allowed chains/assets;
- allowed route classes;
- optional approval threshold.

### 9.1 Concurrency and durability

If an SDK promises a durable spending cap, it must survive process restart and must not be bypassable by concurrent requests.

A safe pattern is:

`reserve → payment attempt → commit | release`

where reservations participate in subsequent budget checks atomically.

A process-local counter is not sufficient for a persistent/durable cap.

## 10. Idempotency And Replay

The SDK should attach a unique idempotency key to settlement-verification submission.

It must treat a unique quote/payment/settlement ID as consumable according to protocol rules and must not intentionally submit the same on-chain settlement as payment for multiple receipts/resources.

Retries caused by transport errors must not cause a second payment.

## 11. Receipt Handling

A client may sanity-check a receipt before replay, but merchant verification remains authoritative for resource access.

Receipt cache keys should include enough scope to prevent cross-merchant/resource reuse.

Do not cache an expired or invalid receipt. Do not convert a failed receipt replay into an automatic second payment without an explicit retry policy and budget check.

## 12. High-Level `fetchPaid` Behavior

Pseudocode:

```ts
async function fetchPaid(url, options) {
  const first = await fetch(url, options);
  if (first.status !== 402) return first;

  const challenge = detectAifp1(first);
  if (!challenge) return routeOrReturnUnsupported(first);

  await policy.assertAllowed(challenge);

  const quote = await createQuote(challenge);
  validateAifp1Quote(quote); // gross-inclusive 100/0 + 99/1/0 conservation
  await policy.reserve(quote.grossAmount);

  try {
    const tx = await buildSettlement(quote); // settle exactly grossAmount
    const txRef = await wallet.signAndBroadcast(tx);
    const receipt = await submitForVerification({ quote, txRef });
    await policy.commit(quote.grossAmount);
    return retryWithReceipt(url, options, receipt);
  } catch (error) {
    await policy.release(quote.grossAmount);
    throw error;
  }
}
```

Actual implementations must handle the ambiguity of whether a broadcast occurred before a transport/process failure. They should reconcile by payment/transaction ID rather than blindly broadcasting again.

## 13. Route Isolation With AIFP-2/x402

A combined SDK may support both:

```text
AIFP-1 challenge → gross-inclusive AIFP-1 path: payer gross = merchant 99% + AiFinPay 1%
x402 challenge   → AIFP-2 0/0 path
```

Rules:

- forced/explicit x402 intent must not be reinterpreted as AIFP-1;
- an AIFP-1 budget rejection must not be bypassed by retrying through x402;
- a legacy fee-bearing splitter must not be used as fallback for AIFP-2;
- a fee-on-top target must not be accepted as current AIFP-1 merely because its configured BPS are `100/0`;
- unsupported x402 versions should produce an explicit unsupported-version error, not a false success or unrelated facilitator error.

## 14. Agent Identity

A caller-supplied `AIFP-Agent-Id` string is an identifier/hint, not sufficient authenticated identity by itself.

Durable free quota, reputation, or delegated authority must be bound to an identity mechanism that cannot be reset by simply changing an arbitrary header.

Agent Passport belongs to the separate AIFP-3 identity protocol surface and should not be presented as part of the normative AIFP-1 payment object model.

## 15. Wallet Packaging

Wallet creation/derivation should be separable from heavy on-chain transaction dependencies when practical. An agent that only needs to create/show a wallet should not necessarily need the entire settlement stack.

Package names and current published versions belong to their actual SDK repository/package registry and must not be invented in this specification.

## 16. Error Model

An AIFP-1 SDK should distinguish at least:

- unsupported payment protocol/version;
- budget/policy rejection;
- quote expired;
- quote route/economics mismatch;
- gross/net/fee conservation mismatch;
- fee-on-top route mismatch;
- no verifier-ready route;
- insufficient balance/gas;
- local signing failure;
- broadcast unknown/pending;
- settlement pending/finality;
- settlement mismatch/underpayment;
- replay/idempotency conflict;
- invalid receipt;
- protected replay still challenged.

Errors before signing should not spend funds. Errors after a possible broadcast need reconciliation before any retry that could duplicate payment.

## 17. Test Requirements

A conforming SDK implementation should test:

1. AIFP-1 challenge detection.
2. AIFP-2/x402 not misclassified as AIFP-1.
3. Current reference tier values as gross payer prices.
4. Standard preset produces gross `$0.0005`, merchant `$0.000495`, protocol fee `$0.000005`, creator `0`.
5. `payer_total_amount = gross_amount`.
6. `merchant + protocol fee + creator = gross` in exact settlement units.
7. Gross-inclusive `100/0` accepted; `100/1` and fee-on-top `100/0` rejected for current AIFP-1.
8. `0/0` rejected on the AIFP-1 route.
9. Merchant/resource mismatch rejected.
10. Expired quote rejected before signing.
11. Unsupported verifier route rejected before signing.
12. Tiny supported payments use correct decimal/rounding semantics.
13. Parallel payments cannot bypass budget caps.
14. Restart does not reset a promised durable cap.
15. Broadcast/retry logic does not duplicate settlement.
16. Valid verified settlement yields one receipt.
17. Replay/duplicate settlement consumption is rejected.
18. Receipt is scoped to the intended merchant/resource.

## 18. Conformance Statement

An SDK should only claim AIFP-1 support for the chains/assets/routes for which its transaction builder, registry, settlement verifier, tests, gross-inclusive economics, and release evidence are mutually consistent.

A list of deployed networks is not equivalent to a list of AIFP-1 payment-live routes.

## References

- [AIFP-1 RFC](./01-AIFP-1-RFC-Payment-Protocol-Specification.md)
- [Merchant Guide](./02-Merchant-Integration-Guide.md)
- [Security Specification](./04-Security-and-Cryptography-Specification.md)
- [OpenAPI](./08-OpenAPI-3.1-Specification.yaml)
- [JSON Schemas](./10-JSON-Schemas.md)
- [Protocol Economics](../economics.md)
