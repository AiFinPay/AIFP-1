# Schemas

Schemas define machine-readable validation for AIFP protocol objects.

## Sources

| Artifact | Source |
|---|---|
| Protocol object shapes | [`docs/aifp/10-JSON-Schemas.md`](../docs/aifp/10-JSON-Schemas.md) |
| API request and response models | [`docs/aifp/08-OpenAPI-3.1-Specification.yaml`](../docs/aifp/08-OpenAPI-3.1-Specification.yaml) |
| SDK generated types | [`sdk/README.md`](../sdk/README.md) |

## Pricing Contract

Every price-bearing schema should model action pricing as a tiered micropayment contract.

| Tier | Fixed price per action | Intended use |
|---|---:|---|
| `standard` | `$0.0005` | Simple reads, single-record retrieval, lightweight API requests. |
| `complex` | `$0.002` | Search, aggregation, multi-source queries, and higher-compute requests. |
| `premium` | `$0.005` | AI inference, GPU workloads, deep analytics, and premium data. |

Successful transactions apply the AiFinPay Protocol Fee of `1%`; the remaining `99%` settles to the merchant, excluding applicable payment-network or settlement costs.

## Validation Targets

- Payment Challenge.
- Quote request and response.
- Pay request and response.
- Receipt token claims.
- Agent Passport objects.
- Merchant configuration.
- Wallet binding.
- Webhook events.
- Error bodies.
- Pricing tiers, protocol fee, and merchant settlement fields.

## CI Expectations

Schema validation should run on every pull request:

1. Validate JSON examples.
2. Validate OpenAPI 3.1.
3. Generate SDK type snapshots.
4. Run conformance fixtures.
