# Core Concepts

This section explains the protocol at the level a developer needs before wiring an SDK into an app.

## Start Here

| Topic | Why it matters |
|---|---|
| [AIFP-1 HTTP 402 Flow](x402-flow.md) | The request, challenge, quote, settlement, receipt, retry loop for merchant monetization |
| [Pricing](../economics.md) | Current AIFP-1 `$0.0005 / $0.002 / $0.005` tiers and exact `100/0` economics |
| [Security](../security-model.md) | Receipt verification, replay protection, and key rotation |
| [Conformance](../conformance.md) | What a correct implementation must do |

AIFP-1 merchant monetization and AIFP-2/x402 agent payments are separate route profiles. AIFP-1 uses `100/0`; AIFP-2 uses `0/0`.

## Reading Order

1. Read [AIFP-1 HTTP 402 Flow](x402-flow.md).
2. Read [Pricing](../economics.md).
3. Read [Security](../security-model.md).
4. Use [Quick Start](../quickstart/index.md) for your language.
