# AiFinPay Improvement Proposals (AIPs)

AIPs record proposed and accepted changes around AIFP-1. An AIP's historical status does not, by itself, prove that a referenced implementation or deployment is currently production/payment-live.

## Process

See [AIP-0001](aip-0001.md) and the [AIP Process](../docs/aifp/06-AIP-Improvement-Proposal-Process.md).

## Current Index

| AIP | Title | Type | Category | Current status / note |
|---|---|---|---|---|
| [1](aip-0001.md) | AIFP Improvement Proposal Process | Meta | N/A | Final; process record |
| [2](aip-0002.md) | Core Payment Protocol | Standards Track | Core | Final; updated current AIFP-1 baseline |
| [7](aip-0007.md) | Add Unichain To The Network Registry | Standards Track | Networks | Final; does not itself imply payment-live status |
| [12](aip-0012.md) | Agent Passport & Reputation Network | Standards Track | Core | **Superseded** in AIFP-1; identity scope moved to AIFP-3 |
| [19](aip-0019.md) | Budget-Exceeded Error | Standards Track | Interface | Historical interface proposal; validate against current API before use |
| [23](aip-0023.md) | Streaming Payments via mSECCO Channels | Standards Track | Core | **Withdrawn** from current AIFP-1 scope |
| [31](aip-0031.md) | Dynamic Pricing Reputation Discount Cap | Informational | N/A | **Superseded** current pricing guidance |

## Current AIFP-1 Baseline

```text
standard: $0.0005/action
complex:  $0.002/action
premium:  $0.005/action
treasuryBps: 100
creatorBps:  0
```

AIFP-2/x402 is a separate `0/0` AiFinPay fee profile. AIFP-3 is the separate Agent Passport/identity surface.

## AIP Types

| Type | Scope |
|---|---|
| **Standards Track** | Protocol/interface/network/security/economic changes |
| **Meta** | Governance/process changes |
| **Informational** | Non-binding guidance/design notes |

## Status Flow

```text
Idea → Draft → Review → Last Call → Accepted → Final
         └──────────────→ Rejected / Withdrawn / Stagnant
Final ──────────────────→ Superseded
```

## Release Discipline

Payment-affecting proposals should not be considered complete from documentation alone. Current implementation claims require matching code, tests, route registry/deployment evidence, and the appropriate review/conformance gate.

## Contributing

1. Define the problem and protocol/route affected.
2. Open a proposal/PR using the AIP template.
3. Describe compatibility, security, migration, implementation, and conformance impact.
4. Keep the RFC, economics, OpenAPI, schemas, SDK/backend policy, contracts/deployment profiles, and examples synchronized when the proposal changes them.
