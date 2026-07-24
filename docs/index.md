# AiFinPay Documentation Portal

Welcome to the AiFinPay Paywall documentation portal. This is the public entry point for protocol implementers, merchant engineers, AI-agent builders, wallet teams, and ecosystem contributors.

## Start Here

| Role | Recommended Path | Outcome |
|---|---|---|
| New developer | [Quick Start](quickstart/index.md) | Understand the end-to-end HTTP 402 flow |
| Merchant engineer | [Merchant Guide](merchant.md) -> [Integration Guide](aifp/02-Merchant-Integration-Guide.md) | Protect a route and verify receipts |
| Agent builder | [Agent Guide](agent.md) -> [Agent SDK Spec](aifp/03-AI-Agent-SDK-Specification.md) | Pay automatically within budget policy |
| Agent protocol engineer | [ACP Spec](aifp/16-Agent-Communication-Protocol-Specification.md) | Agent-to-agent messaging and cross-agent payments |
| Wallet/platform engineer | [Wallet Guide](wallet.md) -> [Security Spec](aifp/04-Security-and-Cryptography-Specification.md) | Bind wallets and enforce settlement policy |
| Protocol implementer | [AIFP-1 RFC](aifp/01-AIFP-1-RFC-Payment-Protocol-Specification.md) | Implement the normative protocol |
| API tooling | [OpenAPI 3.1](aifp/08-OpenAPI-3.1-Specification.yaml) + [JSON Schemas](aifp/10-JSON-Schemas.md) | Generate clients and validators |
| Maintainer | [Repository Architecture](aifp/15-Repository-Architecture.md) + [AIP Process](aifp/06-AIP-Improvement-Proposal-Process.md) | Evolve the project safely |

## Documentation Sections

| Section | Description |
|---|---|
| [Architecture](architecture.md) | System model, trust boundaries, data plane, control plane |
| [Core Concepts](core-concepts/index.md) | x402 flow, pricing, security, and conformance |
| [Protocol Economics](economics.md) | Pricing tiers, protocol fee, merchant settlement model |
| [Security Model](security-model.md) | Receipt signing, replay prevention, wallet policy, key rotation |
| [Conformance](conformance.md) | Compatibility matrix and future certification plan |
| [Developer Experience](developer-experience.md) | SDKs, examples, sandbox, OpenAPI, Postman, schemas |
| [Quick Start](quickstart/index.md) | Sandbox-first Node, Python, and MCP onboarding |
| [Navigation](navigation.md) | Complete documentation map |
| [AIFP Docs](aifp/README.md) | Canonical documentation package |
| [SDKs](../sdk/README.md) | SDK package strategy and language matrix |
| [Examples](../examples/README.md) | Runnable examples and recipes |
| [Sandbox](../sandbox/README.md) | Development and testing environment |
| [Schemas](../schemas/README.md) | Validation and machine-readable contracts |
| [Reference](reference/index.md) | Error codes and low-level protocol reference |

## Protocol In One Flow

```mermaid
flowchart LR
    A["Agent requests resource"] --> B["Merchant returns 402 challenge"]
    B --> C["Agent requests quote"]
    C --> D["Agent pays within wallet policy"]
    D --> E["AiFinPay signs receipt"]
    E --> F["Agent retries request"]
    F --> G["Merchant verifies receipt locally"]
    G --> H["Access granted"]
```

## Real-World Use Cases

| Use case | How AIFP is used |
|---|---|
| Paid data APIs | Agents buy individual records or pages after free quota, then retry with `Payment-Receipt`. |
| RAG and research agents | Pipelines pay for search, enrichment, and premium corpus access within budget policy. |
| AI inference and compute | Merchants price GPU/model calls as `premium` and use async settlement for high-value jobs. |
| Licensed crawler access | Crawlers present Passport for reputation and pay instead of being blocked by WAF rules. |
| Webhook reconciliation | Merchants verify signed lifecycle events and reconcile settlement, payout, and dispute records. |
| Cross-agent payments | Agent A pays Agent B for search, retrieval, or inference via ACP messages and x402 receipts. |

## Canonical Documents

The canonical documentation package lives in [`docs/aifp/`](aifp/README.md). These documents govern protocol behavior and should be treated as source of truth.

