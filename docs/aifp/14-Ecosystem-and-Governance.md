# AIFP-1 Ecosystem & Governance

**Document:** AIFP-DOC-14  
**Status:** Draft ecosystem/governance guidance  
**Companion to:** [AIP Process](./06-AIP-Improvement-Proposal-Process.md)

AIFP-1 is maintained as an open protocol specification for merchant AI-traffic/resource monetization. This document describes governance principles and evidence expectations; it does not claim that a formal standards body, certification authority, Security Council, conformance registry, or multi-stakeholder foundation already exists unless separately evidenced.

## 1. Open Protocol Principle

The protocol should remain implementable from public technical artifacts:

- normative RFC;
- current economics;
- OpenAPI;
- JSON schemas;
- examples/test vectors;
- AIP history;
- implementation/deployment evidence where published.

AiFinPay may operate commercial implementations and settlement services, but product operation and protocol specification are distinct concerns.

## 2. Current Protocol Scope

| Protocol | Scope | Current AiFinPay fee profile |
|---|---|---:|
| **AIFP-1** | Merchant AI-traffic/resource monetization | gross-inclusive `100/0` |
| **AIFP-2/x402** | Separate x402-style agent payment route | `0/0` |
| **AIFP-3** | Agent Passport / identity | Separate identity surface |

Using HTTP `402` does not automatically make an AIFP-1 flow x402.

Current AIFP-1 reference action prices are gross payer prices `$0.0005 / $0.002 / $0.005`. The 1% AiFinPay fee is deducted from gross; it is not added on top. Merchant receives 99% of gross before external network/settlement costs.

## 3. Governance Mechanism

Material AIFP-1 changes should use the repository's AIP process.

At minimum, review should answer:

- what problem is being solved;
- which protocol/route is affected;
- whether wire/API behavior changes;
- whether economics or gross-vs-net semantics change;
- compatibility/migration impact;
- security impact;
- implementation/test impact;
- deployment/registry impact;
- what evidence is required before a live claim.

The actual repository maintainers/owners are responsible for merging changes. This document does not invent a standing review board whose members have not been formally designated.

## 4. Economic Governance

Economic changes are high-impact protocol changes because stale examples or ambiguous gross/net semantics can cause incorrect payments.

Current AIFP-1 baseline:

```text
standard gross: $0.0005/action
complex gross:  $0.002/action
premium gross:  $0.005/action
payer_total_amount = gross_amount
treasuryBps: 100
creatorBps:  0
protocol_fee_amount = 1% of gross
merchant_amount = 99% of gross
creator_amount = 0
merchant_amount + protocol_fee_amount + creator_amount = gross_amount
fee-on-top: not permitted
```

A proposal changing any of those values or semantics should update the entire dependency chain: RFC, economics, OpenAPI, schemas, examples, SDK/backend route policy, contract/deployment profile, discovery metadata, CI/conformance evidence, and migration notes.

## 5. Network Governance

Do not ratify "network support" as a single boolean.

Useful states are:

- protocol can represent the network;
- source/deployment provenance known;
- canonical target identified;
- supported asset/decimals known;
- gross-vs-net settlement semantics verified;
- verifier ready;
- SDK/backend ready;
- E2E verified;
- payment-live;
- legacy/superseded.

An AIP that adds a network identifier is not, by itself, a production/payment-live approval.

## 6. Conformance

There is a difference between a **conformance model** and a currently deployed certification program.

AIFP-1 conformance should test, at minimum:

### Merchant role

- returns an AIFP-1 `402` for paid access;
- advertises the current gross payer price rather than merchant net;
- does not mislabel AIFP-1 as x402;
- verifies receipt signature/claims;
- enforces scope/gross-amount/quota/replay rules;
- fails closed.

### Agent/SDK role

- detects AIFP-1 separately from AIFP-2/x402;
- validates current gross-inclusive `100/0` quote economics;
- checks `payer_total_amount = gross_amount` and exact 99/1/0 conservation;
- rejects fee-on-top routes before signing;
- enforces budget against gross before signing;
- uses the canonical route;
- submits settlement reference for verification;
- does not duplicate payment on retries.

### Settlement/verifier role

- validates actual chain/rail evidence;
- validates merchant/asset/gross amount/payment binding;
- validates current 99/1/0 economic profile and conservation;
- does not issue receipt before successful verification;
- refuses unsupported or fee-on-top routes before payment.

### Financial/reconciliation role

- records gross/merchant/treasury/creator amounts distinctly;
- detects creator amount above zero on current AIFP-1;
- detects payer total different from gross, fee-on-top, or conservation mismatch;
- detects route/profile mismatch;
- handles duplicate/finality/reorg corrections as appropriate.

## 7. Conformance Claims

Until a formal public certification program exists, prefer evidence-based statements such as:

- "passes repository conformance tests for AIFP-1 gross quote/receipt flow";
- "Polygon AIFP-1 route E2E verified at commit/deployment X";
- "SDK supports gross-inclusive AIFP-1 `100/0` on the listed verified routes".

Avoid an official-looking "AIFP Certified" badge/registry unless a real certification process has been created and is operating.

## 8. Reference Implementations

A protocol document may point to real AiFinPay implementation repositories. It must verify the actual repository/package before describing it as published or current.

A documentation stub or aspirational language matrix is not a reference implementation.

Reference implementations are useful for interoperability but are not the only allowed implementation of an open protocol.

## 9. Security Review Governance

Risk-based review should apply:

| Change | Typical review level |
|---|---|
| Editorial docs | ordinary maintainer review |
| Machine-readable schema/API | compatibility + tests |
| SDK payment construction | technical/security review + tests |
| Backend verifier/financial ledger | independent review + integration evidence |
| Smart contracts/payment programs | strongest independent review + exact deployment evidence |

The author or AI agent that produced a financial smart-contract/payment-path change should not be its only production approver.

## 10. Transparency

Important decisions should be traceable through public artifacts where appropriate:

- AIP / issue / requirement;
- pull request;
- exact commit;
- tests/review;
- release/deployment;
- conformance/E2E evidence.

Historical mistakes or superseded deployments should be preserved when they are useful audit evidence, but clearly labeled so they are not selected as current routes.

## 11. Interoperability

AIFP-1 should interoperate with the broader agent/payment ecosystem without erasing protocol boundaries.

AIFP-2 can handle x402 compatibility separately. AIFP-1 should not copy an unsupported x402 wire format and call it compatible. Compatibility claims should identify the actual x402 version/scheme/network tested.

## 12. Long-Term Direction

The goal is an open, implementation-neutral protocol for monetizing machine access. Broader community governance or formal standardization may be pursued as adoption and independent implementations mature, but future governance aspirations should be labeled as roadmap rather than current institutional fact.

## References

- [AIFP-1 RFC](./01-AIFP-1-RFC-Payment-Protocol-Specification.md)
- [AIP Process](./06-AIP-Improvement-Proposal-Process.md)
- [Security Specification](./04-Security-and-Cryptography-Specification.md)
- [Repository Architecture](./15-Repository-Architecture.md)
- [Protocol Economics](../economics.md)
