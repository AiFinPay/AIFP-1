<p align="center">
  <img src="assets/brand/aifp-1-protocol-hero.png" alt="AIFP-1 Protocol" width="720" />
</p>

<h1 align="center">AiFinPay AIFP-1 Protocol</h1>

<p align="center">
  <strong>Payment infrastructure for autonomous AI agents, premium APIs, data products, and machine-to-machine commerce.</strong>
</p>

<p align="center">
  <a href="docs/index.md"><img alt="Documentation" src="https://img.shields.io/badge/docs-protocol%20portal-2F5FD6?style=for-the-badge"></a>
  <a href="LICENSE"><img alt="License" src="https://img.shields.io/badge/license-Apache--2.0%20%2B%20CC--BY--4.0-0B1020?style=for-the-badge"></a>
  <a href="docs/aifp/01-AIFP-1-RFC-Payment-Protocol-Specification.md"><img alt="Protocol" src="https://img.shields.io/badge/protocol-AIFP--1-14B8A6?style=for-the-badge"></a>
  <a href="docs/aifp/08-OpenAPI-3.1-Specification.yaml"><img alt="OpenAPI" src="https://img.shields.io/badge/OpenAPI-3.1-6BA539?style=for-the-badge"></a>
  <a href="ROADMAP.md"><img alt="Status" src="https://img.shields.io/badge/status-draft%20standard-F59E0B?style=for-the-badge"></a>
</p>

---

## The Payment Layer For The Agent Economy

AiFinPay AIFP-1 turns HTTP `402 Payment Required` into a structured payment handshake for AI agents. A merchant can price any API action, content object, data query, or compute job. An agent can discover the price, pay automatically within policy, receive a cryptographic receipt, and retry the original request without a human checkout screen.

```mermaid
flowchart LR
    Agent["AI Agent"] -->|1. Request protected resource| Merchant["Merchant API"]
    Merchant -->|2. HTTP 402 payment challenge| Agent
    Agent -->|3. Quote + pay| AIFP["AiFinPay Control Plane"]
    AIFP -->|4. Wallet policy + settlement| Wallet["Agent Wallet"]
    AIFP -->|5. Signed receipt token| Agent
    Agent -->|6. Retry with receipt| Merchant
    Merchant -->|7. Verify locally + grant access| Agent
```

### Why This Exists

| Today | Problem For Agents | AiFinPay |
|---|---|---|
| Ads | Agents do not view or click ads | Per-action machine payments |
| Subscriptions | Agents touch too many sources | Stateless paid receipts scoped to resources |
| Manual API keys | Discovery and onboarding are too slow | Machine-readable `402` challenge |
| Card checkout | Fees exceed tiny machine-action value | Micropayments with wallet policy |
| Bot blocking | Providers lose agent demand | Monetize machine traffic safely |

## How AIFP Relates to x402

x402 established a practical model for using HTTP `402 Payment Required` as a payment interaction
between clients and protected resources. AIFP-1 uses the same HTTP foundation and extends it into a
broader protocol surface for autonomous AI agents, merchant APIs, wallets, receipts, policy controls,
and machine-to-machine commerce. The intent is compatibility and specialization, not replacement.

### Key Differences

- x402 standardized HTTP `402 Payment Required` payment interactions for web resources.
- AIFP adopts the same foundation while expanding the protocol for autonomous AI agents.
- AIFP introduces quote negotiation, receipt lifecycle, wallet policies, merchant-side verification, governance, SDKs, and protocol specifications.
- AIFP targets machine-to-machine commerce where software can discover, purchase, and access digital resources autonomously.
- The two approaches are complementary, and AIFP can coexist with x402-based ecosystems.

---

## Product Surface

| Surface | What It Does | Primary Docs |
|---|---|---|
| Protocol | HTTP 402 challenge, quote, payment, receipt, retry | [AIFP-1 RFC](docs/aifp/01-AIFP-1-RFC-Payment-Protocol-Specification.md) |
| Merchant SDK | Protect routes, price actions, verify receipts locally | [Merchant Integration](docs/aifp/02-Merchant-Integration-Guide.md) |
| Agent SDK | Detect paywalls, quote, pay, retry, enforce budgets | [Agent SDK Spec](docs/aifp/03-AI-Agent-SDK-Specification.md) |
| Wallet Layer | Bind wallets, budgets, assets, rails, settlement policy | [Wallet Guide](docs/wallet.md) |
| Receipt Authority | Ed25519 receipt token issuance and verification | [Security Spec](docs/aifp/04-Security-and-Cryptography-Specification.md) |
| Developer Portal | OpenAPI, JSON schemas, Postman, examples, SDK references | [Docs Portal](docs/index.md) |
| Governance | AIP proposal flow, ecosystem roles, conformance | [AIP Process](docs/aifp/06-AIP-Improvement-Proposal-Process.md) |

---

## Pricing For Agent Actions

| Tier | Starts From | Intended Workload |
|---|---:|---|
| `standard` | `$0.0005` | Simple read, single record, lightweight API request |
| `complex` | `$0.002` | Search, aggregation, multi-source queries, higher compute |
| `premium` | `$0.005` | AI inference, GPU workloads, deep analytics, premium data |

For the current AIFP-1 merchant-monetization profile, AiFinPay charges exactly **1% (`100` bps)** on successful monetized transactions, with **no creator/referral fee (`0` bps)**. The merchant receives **99% before applicable network or settlement costs**. AIFP-2/x402 agent-payment routes are a separate profile and use **0% AiFinPay protocol fee (`0/0`)**.

Learn more in [Protocol Economics](docs/economics.md).

---

## Architecture

```mermaid
flowchart TB
    subgraph AgentLayer["Agent Layer"]
        AgentSDK["Agent SDK"]
        Passport["Agent Passport"]
        Budget["Budget Policy"]
    end
    subgraph MerchantPlane["Merchant Data Plane"]
        Middleware["Merchant Middleware"]
        Pricing["Pricing Engine"]
        Verifier["Local Receipt Verifier"]
        Resource["Protected API / Data / Compute"]
    end
    subgraph ControlPlane["AiFinPay Control Plane"]
        Quote["Quote Service"]
        Pay["Payment Orchestrator"]
        Receipt["Receipt Authority"]
        Ledger["Ledger + Webhooks"]
        JWKS["JWKS + Key Rotation"]
    end
    subgraph Settlement["Settlement Layer"]
        Assets["USDC / USDT / PYUSD"]
        Networks["Supported Networks"]
        Fiat["Fiat + Hybrid Rails"]
    end
    AgentSDK --> Passport
    AgentSDK --> Budget
    AgentSDK --> Middleware
    Middleware --> Pricing
    Pricing --> AgentSDK
    AgentSDK --> Quote
    Quote --> Pay
    Pay --> Assets
    Pay --> Fiat
    Assets --> Networks
    Pay --> Receipt
    Receipt --> AgentSDK
    AgentSDK --> Verifier
    Verifier --> JWKS
    Verifier --> Resource
    Receipt --> Ledger
    Ledger --> MerchantPlane
```

AiFinPay separates the control plane from the merchant data plane. Merchants verify receipt tokens locally, so access checks remain fast and resilient. The control plane handles quotes, wallet authorization, settlement, receipts, key rotation, and webhooks.

---

## HTTP 402 Sequence

```mermaid
sequenceDiagram
    autonumber
    participant A as AI Agent
    participant M as Merchant API
    participant P as AiFinPay
    participant W as Wallet
    A->>M: GET /premium-data<br/>Accept-Payment: aifp/1.0
    M-->>A: 402 Payment Required<br/>Payment Challenge
    A->>P: POST /v1/quote
    P-->>A: quote_id, amount, currency, nonce, expiry
    A->>P: POST /v1/pay<br/>Idempotency-Key
    P->>W: Check policy + debit approved wallet
    W-->>P: Settlement reference
    P-->>A: Ed25519 receipt token
    A->>M: Retry request<br/>Payment-Receipt: JWT
    M->>M: Verify signature, audience, resource, amount, expiry, nonce
    M-->>A: 200 OK + protected response
```

### Payment Challenge Example

```json
{
  "payment_challenge": {
    "version": "1.0",
    "scheme": "aifp",
    "merchant_id": "mrch_9f3a1c2b",
    "resource": "/api/data",
    "pricing_tier": "standard",
    "estimated_amount": "0.0005",
    "currency": "USD",
    "accepted_assets": ["USDC", "USDT", "PYUSD"],
    "accepted_chains": ["polygon", "base", "solana"],
    "quote_endpoint": "https://api.aifinpay.io/v1/quote",
    "nonce": "b7e2c91a",
    "expires_at": "2026-07-01T12:34:56Z"
  }
}
```

---

## Five Minute Start

### Merchant

```bash
npm install @aifinpay/merchant
```

```ts
import { aifpPaywall } from "@aifinpay/merchant";

app.use(aifpPaywall({
  merchantId: "mrch_...",
  pricing: {
    "/api/data": { tier: "standard" },
    "/api/search": { tier: "complex" },
    "/api/inference": { tier: "premium" }
  }
}));
```

### Agent

```bash
npm install @aifinpay/agent
```

```ts
import { AIFPAgent } from "@aifinpay/agent";

const agent = new AIFPAgent({
  apiKey: process.env.AIFP_AGENT_KEY,
  walletId: "wlt_...",
  budget: { dailyUsd: 5 }
});

const response = await agent.fetch("https://merchant.example.com/api/data");
```

### Raw API

```bash
curl https://api.aifinpay.io/v1/quote \
  -H "Authorization: Bearer $AIFP_AGENT_KEY" \
  -H "Content-Type: application/json" \
  -d '{"merchant_id":"mrch_9f3a1c2b","resource":"/api/data","pricing_tier":"standard"}'
```

---

## Documentation Map

| Start Here | Build | Verify | Govern |
|---|---|---|---|
| [Docs Portal](docs/index.md) | [Merchant Guide](docs/merchant.md) | [Security Model](docs/security-model.md) | [AIP Process](docs/aifp/06-AIP-Improvement-Proposal-Process.md) |
| [Quick Start](docs/quickstart/index.md) | [Agent Guide](docs/agent.md) | [Conformance](docs/conformance.md) | [Ecosystem](docs/aifp/14-Ecosystem-and-Governance.md) |
| [Architecture](docs/architecture.md) | [SDKs](sdk/README.md) | [OpenAPI](docs/aifp/08-OpenAPI-3.1-Specification.yaml) | [Roadmap](ROADMAP.md) |
| [Protocol Economics](docs/economics.md) | [Examples](examples/README.md) | [JSON Schemas](docs/aifp/10-JSON-Schemas.md) | [Contributing](CONTRIBUTING.md) |

Every canonical source document lives in [docs/aifp](docs/aifp/README.md). Every important document is reachable within two clicks from this README.

---

## Trust, Security, And Compliance Posture

| Area | Posture |
|---|---|
| Receipt signing | Ed25519 JWT receipts with JWKS key discovery and rotation |
| Replay protection | Nonce, resource binding, receipt expiry, idempotency keys |
| Merchant availability | Local verification; no control-plane call required for every retry |
| Agent safety | Wallet budgets, merchant policy, trust levels, passport metadata |
| Settlement | Stablecoin, fiat, and hybrid settlement model |
| Governance | Public AIP flow for protocol changes |
| Security reporting | Private disclosure through [SECURITY.md](SECURITY.md) |

---

## Release Quality

This repository is organized as a public protocol foundation project:

- Canonical RFC/specification set in `docs/aifp/`.
- Human-readable documentation portal in `docs/`.
- Machine-readable OpenAPI and JSON Schema contracts.
- Postman collection for API exploration.
- SDK design surface for TypeScript, Python, and Go.
- Examples for merchant, agent, wallet, webhook, and raw HTTP flows.
- GitHub issue forms, PR template, workflows, code ownership, roadmap, security, and support policy.

---

## License

Code, examples, schemas, scripts, tests, GitHub workflows, and machine-readable artifacts are licensed under Apache-2.0. Documentation, prose specifications, diagrams, and governance documents are licensed under CC BY 4.0 unless a file states otherwise. See [LICENSE](LICENSE).

---

## Vision

AiFinPay is designed to become a foundational standard for the AI web: a neutral payment layer where autonomous software can discover priced resources, reason about budgets, pay safely, carry reputation, and access the machine-readable economy without subscriptions or human checkout.

