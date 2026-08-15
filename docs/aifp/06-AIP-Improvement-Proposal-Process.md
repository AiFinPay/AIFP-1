# AIFP Improvement Proposal (AIP) Process

**Document:** AIFP-DOC-06  
**Status:** Active governance process  
**Applies to:** AIFP-1 protocol evolution and repository governance

An **AIP** (AiFinPay Improvement Proposal) is the repository mechanism for proposing, reviewing, and recording material protocol changes. It is intended to prevent undocumented drift between the normative specification, machine-readable contracts, SDK/backend behavior, contracts, and deployment profiles.

## 1. AIP Types

| Type | Scope |
|---|---|
| **Standards Track** | Protocol semantics, interfaces, receipt/quote objects, settlement rules, security rules, network/profile support |
| **Meta** | Governance and process changes |
| **Informational** | Non-binding guidance, design notes, operational recommendations |

Standards Track proposals may use categories such as `Core`, `Interface`, `Networks`, `Security`, or `Economics`.

## 2. Lifecycle

```text
Idea → Draft → Review → Last Call → Accepted → Final
         └──────────────→ Rejected / Withdrawn / Stagnant
Final ──────────────────→ Superseded
```

| Status | Meaning |
|---|---|
| `Draft` | Proposal exists and is open to change |
| `Review` | Active technical/security review |
| `Last Call` | Final objection window |
| `Accepted` | Direction approved; implementation/evidence may still be required |
| `Final` | Normative for the stated protocol/version/profile |
| `Rejected` | Declined with rationale |
| `Withdrawn` | Author withdrew the proposal |
| `Stagnant` | Inactive and not current guidance |
| `Superseded` | Replaced by newer normative guidance |

A Standards Track AIP must not be marked `Final` solely because documentation was merged. Where the proposal changes payment behavior, `Final` should require implementation/conformance evidence appropriate to the risk.

## 3. Review Principles

A proposal should state:

- the problem;
- exact protocol change;
- affected route/protocol (`AIFP-1`, `AIFP-2`, etc.);
- compatibility impact;
- security impact;
- migration plan;
- implementation/test plan;
- machine-readable surfaces affected;
- deployment/rollout implications where relevant.

Financial/smart-contract changes need stronger independent review than editorial documentation changes.

## 4. Compatibility

Classify changes by actual impact rather than by marketing/release preference:

- **PATCH:** editorial clarification with no change to machine behavior;
- **MINOR:** backward-compatible optional capability;
- **MAJOR:** breaking wire/behavior/security/economic change requiring migration.

Changes to required request fields, payment semantics, receipt validation, fee routing, or transaction construction are generally not editorial changes.

## 5. Economics Changes

Economic changes require explicit coordination because stale examples can cause real payment errors.

An economics proposal must update, as applicable:

1. AIFP-1 RFC;
2. `docs/economics.md`;
3. OpenAPI;
4. JSON schemas/examples;
5. Postman examples;
6. SDK route policy;
7. backend quote/verifier policy;
8. contract/deployment profile;
9. tests/conformance evidence;
10. public developer documentation.

### Current economics baseline

As of the August 14, 2026 founder-approved model:

| Route | Treasury | Creator/referral | Reference prices |
|---|---:|---:|---|
| AIFP-1 | `100` bps | `0` bps | `$0.0005 / $0.002 / $0.005` |
| AIFP-2/x402 | `0` bps | `0` bps | provider-defined x402 payment amount |

Earlier AIFP-1 microcent prices and `100/1` examples are superseded current-product economics.

## 6. Network / Deployment Proposals

Adding a network to a repository or deploying a contract does not automatically make the network payment-live.

A network/payment-profile AIP should distinguish:

- source repository and canonical source commit;
- deployed contract/program/address;
- runtime/source provenance;
- supported assets and decimals;
- ABI/IDL/entrypoint;
- active economic profile;
- settlement verifier availability;
- SDK/backend registry support;
- end-to-end evidence.

A proposal must not use a raw chain count as proof that all chains satisfy the current payment profile.

## 7. Protocol Boundaries

AIPs must preserve protocol separation unless they explicitly propose a cross-protocol change.

Current boundaries relevant to this repository:

- **AIFP-1:** merchant AI-traffic/resource monetization, current `100/0` profile;
- **AIFP-2/x402:** separate agent-payment route, current `0/0` AiFinPay profile;
- **AIFP-3:** Agent Passport / identity surface.

Using HTTP `402` does not make an AIFP-1 message x402.

## 8. AIP Template

```markdown
---
aip: <number>
title: <concise title>
author: <name/handle>
type: Standards Track | Meta | Informational
category: Core | Interface | Networks | Security | Economics
status: Draft
created: YYYY-MM-DD
updated: YYYY-MM-DD
requires: <optional>
supersedes: <optional>
---

## Abstract
## Motivation
## Specification
## Protocol / Route Scope
## Backward Compatibility
## Migration Plan
## Security Considerations
## Reference Implementation
## Test / Conformance Evidence
## Deployment Considerations
## Copyright
```

## 9. Current Repository Examples

### AIP-2 — Core Payment Protocol

AIP-2 records the current AIFP-1 merchant-monetization baseline. Its active economics must agree with the canonical AIFP-1 RFC and economics document: `$0.0005 / $0.002 / $0.005`, `100/0`, settlement verification before receipt issuance.

### AIP-31 — Dynamic Pricing Reputation Discount Cap

AIP-31 is now marked **Superseded**. Its prior dynamic ranges/reputation-discount assumptions are not current AIFP-1 pricing guidance. A future dynamic-pricing design requires a new or reactivated proposal with current economics and deterministic quote semantics.

## 10. Definition Of Done For A Standards Change

Before a payment-affecting AIP is considered complete:

- normative text and machine-readable contracts agree;
- stale contradictory examples are removed or explicitly marked historical;
- implementation is linked to exact commits/versions;
- relevant tests pass;
- security review is complete at the appropriate risk level;
- deployment/profile changes are traceable;
- end-to-end evidence exists for any new payment-live claim;
- rollback/migration behavior is documented.

## 11. Copyright

Unless a file states otherwise, AIP code artifacts use the repository code license and documentation uses the repository documentation license.
