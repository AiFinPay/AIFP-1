# AiFinPay Protocol Documentation

The official documentation ecosystem for the **AiFinPay Paywall Protocol (AIFP)** — an application-layer payment protocol on top of HTTP that lets autonomous AI agents pay for content, data, and APIs automatically, with no human in the loop.

## Documents

| # | Document | Audience | Read it for |
|---|---|---|---|
| 01 | [AIFP-1 — Payment Protocol Specification](./01-AIFP-1-RFC-Payment-Protocol-Specification.md) | Implementers, standards bodies | Normative standard: 402, challenge, receipt, flows, errors, security, settlement |
| 02 | [Merchant Integration Guide](./02-Merchant-Integration-Guide.md) | Backend engineers | Integrate AIFP in production frameworks |
| 03 | [AI Agent SDK Specification](./03-AI-Agent-SDK-Specification.md) | Agent developers | Auto-pay flow, wallets, budgets, multi-chain, Passport |
| 04 | [Security & Cryptography Specification](./04-Security-and-Cryptography-Specification.md) | Security engineers | Threat model, signatures, replay, key rotation, compliance |
| 05 | [Whitepaper](./05-Whitepaper.md) | Investors, enterprises, partners | Protocol vision, market, model, roadmap |
| 06 | [AIP — Improvement Proposal Process](./06-AIP-Improvement-Proposal-Process.md) | Contributors, maintainers | Governance, lifecycle, versioning, compatibility |
| 07 | [Quick Start Guide](./07-Quick-Start-Guide.md) | New developers | Merchant, agent, wallet quick starts |
| 08 | [OpenAPI 3.1 Specification](./08-OpenAPI-3.1-Specification.yaml) | API consumers, tooling | Machine-readable API source of truth |
| 09 | [Postman Collection](./09-Postman-Collection.json) | API testers | Quote, Pay, Receipt, Merchant, Wallet, Verify requests |
| 10 | [JSON Schemas](./10-JSON-Schemas.md) | Tooling, validation | Schema definitions for protocol objects |
| 11 | [SDK Reference](./11-SDK-Reference.md) | Developers | Classes, methods, events for SDKs |
| 12 | [Developer Portal Structure](./12-Developer-Portal-Structure.md) | DevRel, docs team | Portal IA, navigation, search, sandbox |
| 13 | [Branding Guidelines](./13-Branding-Guidelines.md) | Everyone | Naming, color, typography, code and doc style |
| 14 | [Ecosystem & Governance](./14-Ecosystem-and-Governance.md) | Partners, foundations | Open-standard strategy, governance, certification |
| 15 | [Repository Architecture](./15-Repository-Architecture.md) | Maintainers | GitHub org layout, CI/CD, templates, contribution flow |
| 16 | [Agent Communication Protocol](./16-Agent-Communication-Protocol-Specification.md) | Agent developers | Agent-to-agent messaging, discovery, cross-agent payments |

## Pricing Summary

| Agent Action Tier | Starts From | Typical Action |
|---|---:|---|
| Standard | `$0.0005` | Simple read, single record, lightweight API request |
| Complex | `$0.002` | Search, aggregation, multi-source queries, higher compute |
| Premium | `$0.005` | AI inference, GPU workloads, deep analytics, premium data |

AiFinPay charges a **1% protocol fee** on every successful transaction. The remaining **99%** is settled to the merchant, excluding any applicable payment network or settlement costs.

## How They Fit Together

- **Document 01 governs.** It is the normative spec. All other documents are conforming guidance; on any conflict, AIFP-1 wins.
- **Single sources of truth.** API → Doc 08. Object shapes → Doc 10. SDKs mirror Docs 08/10. Postman mirrors Doc 08.
- **Repository architecture.** Doc 15 describes the official GitHub organization layout and repository standards.

## Status

Version 1.0.0 · Draft Standard · June 28, 2026 · © 2026 AiFinPay, Inc.
