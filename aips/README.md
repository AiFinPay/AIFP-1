# AiFinPay Improvement Proposals (AIPs)

AIPs are the formal mechanism for proposing, debating, and ratifying changes to the AiFinPay Paywall Protocol (AIFP) and its ecosystem.

## Process

See [AIP-0001](aip-0001.md) for the full proposal process.

## Current AIPs

| AIP | Title | Type | Category | Status |
|---|---|---|---|---|
| [1](aip-0001.md) | AIFP Improvement Proposal Process | Meta | N/A | Final |
| [2](aip-0002.md) | Core Payment Protocol | Standards Track | Core | Draft |
| [7](aip-0007.md) | Add Unichain to Full Core Networks | Standards Track | Networks | Final |
| [12](aip-0012.md) | Agent Passport & Reputation Network | Standards Track | Core | Draft |
| [19](aip-0019.md) | AIFP-403-BUDGET-EXCEEDED Error | Standards Track | Interface | Draft |
| [23](aip-0023.md) | Streaming Payments via mSECCO Channels | Standards Track | Core | Withdrawn |
| [31](aip-0031.md) | Dynamic Pricing Reputation Discount Cap | Informational | N/A | Draft |

## AIP Types

| Type | Scope |
|---|---|
| **Standards Track** | Changes to the protocol itself |
| **Meta** | Changes to processes or governance |
| **Informational** | Guidelines and best practices (non-binding) |

> **2026-08-07.** Five AIPs were moved off `Final`/`Accepted` after a
> line-by-line check against the implementation. Each carries a "Status note"
> saying exactly what disagrees, with file references. `Final` is what an
> outside integrator trusts, so a Final AIP that contradicts the server is
> worse than no AIP: it produces a client that is wrong in a way its author
> can defend.
>
> Nothing shipped in the last week is specified here — receipt scope, the
> prepaid-batch floor, fee-on-top. That gap is the more useful half of this
> finding.

## AIP Status Flow

```
Idea ──► Draft ──► Review ──► Last Call ──► Accepted ──► Final
```

## Contributing

1. Open a Discussion describing your idea
2. Submit a PR with a new AIP using the template from AIP-0001
3. An Editor will assign a number and begin review
