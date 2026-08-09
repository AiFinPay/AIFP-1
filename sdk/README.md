# SDKs

AiFinPay SDKs provide merchant middleware, agent auto-pay clients, receipt verification, wallet binding, pricing helpers, and generated protocol types.

## Language Matrix

| Language | Merchant SDK | Agent SDK | Package Target | Status |
|---|---:|---:|---|---|
| TypeScript / Node | Yes | Yes | `@aifinpay/merchant`, `@aifinpay/agent` | Design ready |
| Python | Yes | Yes | `aifinpay-merchant`, `aifinpay-agent` | Design ready |
| Go | Yes | Yes | `github.com/aifinpay/aifp-go` | Design ready |
| Rust | Planned | Planned | `aifinpay` | Planned |
| Java | Planned | Planned | `io.aifinpay:aifp` | Planned |
| PHP | Planned | Planned | `aifinpay/aifp` | Planned |
| .NET | Planned | Planned | `AiFinPay` | Planned |

## Pricing Helpers

| Helper | Value |
|---|---|
| `standard` | `$0.0005` for simple reads, single records, and lightweight API requests. |
| `complex` | `$0.002` for search, aggregation, multi-source queries, and higher compute. |
| `premium` | `$0.005` for AI inference, GPU workloads, deep analytics, and premium data. |
| `protocolFeeRate` | `0.01`, representing the AiFinPay Protocol Fee of 1%. |
| `merchantSettlementRate` | `0.99`, before applicable network or settlement costs. |

## SDK Architecture

```mermaid
flowchart TD
    Core["Protocol Core"] --> Types["Generated Types"]
    Core --> Receipt["Receipt Verifier"]
    Core --> Errors["Error Registry"]
    Core --> Pricing["Pricing Helpers"]
    Types --> Merchant["Merchant Middleware"]
    Types --> Agent["Agent Client"]
    Types --> Wallet["Wallet Client"]
    Pricing --> Merchant
    Pricing --> Agent
    Receipt --> Merchant
    Merchant --> Frameworks["Express / Fastify / Next / Django / Rails / Go HTTP"]
    Agent --> Fetch["fetch / requests / http clients"]
    Wallet --> Settlement["Stablecoin / fiat adapters"]
```

## Package Design

- [TypeScript SDK](typescript/README.md)
- [Python SDK](python/README.md)
- [Go SDK](go/README.md)

## Source Documents

- [AI Agent SDK Specification](../docs/aifp/03-AI-Agent-SDK-Specification.md)
- [SDK Reference](../docs/aifp/11-SDK-Reference.md)
- [OpenAPI 3.1](../docs/aifp/08-OpenAPI-3.1-Specification.yaml)
- [JSON Schemas](../docs/aifp/10-JSON-Schemas.md)

