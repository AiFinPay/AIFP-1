# Agent Guide

This page is the human-facing overview for an AIFP-1 payer/agent integration. Runnable protocol-oriented examples are in [Quick Start](quickstart/index.md) and [Core Concepts](core-concepts/index.md).

## Responsibilities

| Responsibility | Required behavior |
|---|---|
| Classify `402` | Distinguish an AIFP-1 challenge from AIFP-2/x402 or unsupported payment protocols |
| Request quote | Obtain a binding AIFP-1 quote only from a verifier-ready route |
| Validate economics | Require AIFP-1 `treasuryBps=100`, `creatorBps=0` |
| Enforce budget | Reserve/check spend before any signing or broadcast |
| Sign locally | Keep payer private keys/recovery material in the payer wallet/environment |
| Broadcast settlement | Send the quoted transaction to the selected settlement rail |
| Reconcile | Submit `tx_ref` for independent verification and avoid duplicate payment on ambiguous failures |
| Retry resource | Attach the verified receipt and replay the protected request |

AIFP-3 Agent Passport is a separate identity protocol. An AIFP-1 client may consume authenticated identity, but Passport is not part of the AIFP-1 payment wire format.

## Read Next

- [Node / TypeScript Quick Start](quickstart/node-typescript.md)
- [Python Quick Start](quickstart/python.md)
- [MCP Server Quick Start](quickstart/mcp-server.md)
- [AIFP-1 HTTP 402 Flow](core-concepts/x402-flow.md)
- [Protocol Economics](economics.md)
- [Error Codes](reference/error-codes.md)
