# Schemas

Schemas define machine-readable validation for AIFP-1 protocol objects.

## Sources

| Artifact | Source |
|---|---|
| Protocol object shapes | [`docs/aifp/10-JSON-Schemas.md`](../docs/aifp/10-JSON-Schemas.md) |
| API request and response models | [`docs/aifp/08-OpenAPI-3.1-Specification.yaml`](../docs/aifp/08-OpenAPI-3.1-Specification.yaml) |
| SDK generated types | [`sdk/README.md`](../sdk/README.md) |

## Pricing Contract

Every price-bearing AIFP-1 schema must model the reference action price as the **gross amount paid by the agent**, excluding separately disclosed external network/gas cost.

| Tier | Gross payer amount | Merchant 99% | AiFinPay 1% | Intended use |
|---|---:|---:|---:|---|
| `standard` | `$0.0005` | `$0.000495` | `$0.000005` | Simple reads, single-record retrieval, lightweight API requests. |
| `complex` | `$0.002` | `$0.00198` | `$0.00002` | Search, aggregation, multi-source queries, and higher-compute requests. |
| `premium` | `$0.005` | `$0.00495` | `$0.00005` | AI inference, GPU workloads, deep analytics, and premium data. |

For the current AIFP-1 merchant-monetization profile:

```text
payer_total_amount = gross_amount
merchant_amount + protocol_fee_amount + creator_amount = gross_amount
protocol_fee_amount = 1% of gross (treasury_bps = 100)
merchant_amount = 99% of gross
creator_amount = 0 (creator_bps = 0)
```

The 1% AiFinPay fee is deducted from gross and is **not added on top** of the displayed/quoted action price. AIFP-2/x402 is a separate `0/0` route profile.

## Validation Targets

- AIFP-1 Payment Challenge.
- Quote request and gross-inclusive Quote response.
- Pay/settlement-verification request and response.
- Receipt envelope and receipt claims represented by the active AIFP-1 profile.
- Optional assisted receipt verification request/response.
- Error bodies.
- Pricing tiers and gross/merchant/protocol-fee/creator amount invariants.

AIFP-3 Agent Passport and AIFP-2/x402 objects are separate protocol surfaces and are not part of the normative AIFP-1 schema contract merely because an implementation may integrate them.

## CI Expectations

Schema validation should run on every pull request:

1. Validate JSON examples.
2. Validate OpenAPI 3.1.
3. Generate SDK type snapshots where implemented.
4. Run conformance fixtures where implemented.
5. Reject active examples that reintroduce fee-on-top AIFP-1 semantics or use the gross reference tier as `merchant_amount`.
