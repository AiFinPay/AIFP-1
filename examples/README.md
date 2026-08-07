# Examples

Examples show the canonical AIFP flow from multiple perspectives. They are written as copyable implementation recipes and must remain aligned with OpenAPI, JSON Schemas, and AIFP-1.

## Example Catalog

| Example | Purpose |
|---|---|
| [Merchant Basic](merchant-basic.md) | Protect a resource with AIFP middleware |
| [Agent Autopay](agent-autopay.md) | Agent detects `402`, pays, and retries |
| [Wallet Funding](wallet-funding.md) | Wallet setup and budget policy |
| [Webhook Verification](webhook-verification.md) | Merchant verifies signed webhooks |
| [Raw HTTP 402](curl-http-402.md) | End-to-end cURL flow for quote, pay, retry |
| [Receipt Verification](receipt-verification.md) | Local receipt validation checklist and pseudocode |

## End-to-End Flow

```mermaid
sequenceDiagram
    participant Merchant
    participant Agent
    participant AiFinPay
    participant Wallet
    Agent->>Merchant: Request paid resource
    Merchant-->>Agent: 402 challenge with pricing_tier
    Agent->>AiFinPay: Quote + Pay
    AiFinPay->>Wallet: Settle payment under policy
    AiFinPay-->>Agent: Receipt token
    Agent->>Merchant: Retry with receipt
    Merchant-->>Agent: Protected data
```

## Pricing Contract

All examples use:

| Tier | From |
|---|---:|
| `standard` | `$0.0005` |
| `complex` | `$0.002` |
| `premium` | `$0.005` |

Protocol fee is 1%; merchant settlement is 99% before external costs.

