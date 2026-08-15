# Quick Start

Choose the guide that matches your integration context.

| Path | Best for |
|---|---|
| [Node / TypeScript](node-typescript.md) | Protocol-oriented TypeScript examples |
| [Python](python.md) | Protocol-oriented Python examples |
| [MCP Server](mcp-server.md) | MCP integrations that must distinguish AIFP-1 from AIFP-2/x402 |

## Before Real Spend

The protocol repository does not define a universal public sandbox, faucet, test key, or package release channel. Use only environments and package versions explicitly documented by the active implementation repository or package registry.

Before enabling real spend, read:

- [AIFP-1 HTTP 402 Flow](../core-concepts/x402-flow.md)
- [Protocol Economics](../economics.md)
- [Security Model](../security-model.md)
- [Error Codes](../reference/error-codes.md)

A route should only move from test to real spend after its canonical target, asset decimals, SDK transaction semantics, settlement verifier, current `100/0` economics, replay/idempotency behavior, and end-to-end evidence have been verified.

## Package Status

The language quickstarts are protocol-facing examples. Actual package names, versions, installation commands, and supported routes must be checked against the current AiFinPay implementation repositories/package registries; this documentation does not invent `alpha` package versions.
