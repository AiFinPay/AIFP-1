# AiFinPay Protocol Documentation

The official documentation ecosystem for **AiFinPay AIFP-1** — an application-layer merchant-monetization protocol on top of HTTP that lets autonomous AI agents pay for protected content, data, APIs, and digital actions without a human checkout flow.

## Documents

| # | Document | Audience | Read it for |
|---|---|---|---|
| 01 | [AIFP-1 — Payment Protocol Specification](./01-AIFP-1-RFC-Payment-Protocol-Specification.md) | Implementers, standards bodies | Normative standard: HTTP 402, challenge, receipt, flows, errors, security, settlement |
| 02 | [Merchant Integration Guide](./02-Merchant-Integration-Guide.md) | Backend engineers | Integrate AIFP-1 in server frameworks |
| 03 | [AI Agent SDK Specification](./03-AI-Agent-SDK-Specification.md) | Agent developers | Auto-pay flow, wallets, budgets, settlement profiles |
| 04 | [Security & Cryptography Specification](./04-Security-and-Cryptography-Specification.md) | Security engineers | Threat model, signatures, replay, key rotation |
| 05 | [Whitepaper](./05-Whitepaper.md) | Investors, enterprises, partners | Protocol vision, market, model, roadmap |
| 06 | [AIP — Improvement Proposal Process](./06-AIP-Improvement-Proposal-Process.md) | Contributors, maintainers | Governance, lifecycle, versioning, compatibility |
| 07 | [Quick Start Guide](./07-Quick-Start-Guide.md) | New developers | Merchant, agent, wallet quick starts |
| 08 | [OpenAPI 3.1 Specification](./08-OpenAPI-3.1-Specification.yaml) | API consumers, tooling | Machine-readable API contract |
| 09 | [Postman Collection](./09-Postman-Collection.json) | API testers | Quote, Pay, Receipt, Merchant, Wallet, Verify requests |
| 10 | [JSON Schemas](./10-JSON-Schemas.md) | Tooling, validation | Schema definitions for protocol objects |
| 11 | [SDK Reference](./11-SDK-Reference.md) | Developers | Classes, methods, events for SDKs |
| 12 | [Developer Portal Structure](./12-Developer-Portal-Structure.md) | DevRel, docs team | Portal IA, navigation, search, sandbox |
| 13 | [Branding Guidelines](./13-Branding-Guidelines.md) | Everyone | Naming, color, typography, code and doc style |
| 14 | [Ecosystem & Governance](./14-Ecosystem-and-Governance.md) | Partners, foundations | Open-standard strategy, governance, certification |
| 15 | [Repository Architecture](./15-Repository-Architecture.md) | Maintainers | GitHub org layout, CI/CD, templates, contribution flow |
| 16 | [Agent Communication Protocol](./16-Agent-Communication-Protocol-Specification.md) | Agent developers | Agent-to-agent messaging, discovery, cross-agent payment metadata |

## Pricing Summary

| Agent Action Tier | Starts From | Typical Action |
|---|---:|---|
| Standard | `$0.0005` | Simple read, single record, lightweight API request |
| Complex | `$0.002` | Search, aggregation, multi-source queries, higher compute |
| Premium | `$0.005` | AI inference, GPU workloads, deep analytics, premium data |

The current **AIFP-1 merchant-monetization profile** charges exactly **1% (`100` bps)** to AiFinPay, with **0 bps creator/referral fee**. The merchant receives **99% before external network or settlement costs**. **AIFP-2/x402 is a separate agent-payment profile with `0/0` AiFinPay fees.**

## How They Fit Together

- **Document 01 governs AIFP-1.** It is the normative spec. All other AIFP-1 documents are conforming guidance; conflicts must be reconciled explicitly.
- **Economics source of truth.** [`../economics.md`](../economics.md) records the current founder-approved AIFP-1 `100/0` and AIFP-2 `0/0` separation.
- **Machine-readable sources.** API → Doc 08. Object shapes → Doc 10. SDK guidance mirrors Docs 08/10. Postman mirrors Doc 08.
- **Repository architecture.** Doc 15 describes the intended GitHub organization layout and repository standards.
- **Status discipline.** Draft/specification material must not be described as production-ready merely because it is documented here.

## Status

Version 1.0.0 · Draft Standard · updated economics August 14, 2026 · © 2026 AiFinPay
