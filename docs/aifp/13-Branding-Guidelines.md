# AIFP-1 Branding & Editorial Guidelines

**Document:** AIFP-DOC-13  
**Status:** Active repository style guidance

These guidelines govern naming and editorial consistency for the AIFP-1 protocol repository. They do not define visual identity for every AiFinPay product.

## 1. Naming

| Subject | Preferred form |
|---|---|
| Company | **AiFinPay** |
| Protocol | **AIFP-1** |
| Description | **merchant AI-traffic/resource monetization protocol** |
| Related agent-payment protocol | **AIFP-2/x402** |
| Identity protocol | **AIFP-3 / Agent Passport** |
| Improvement proposal | **AIP** |

Rules:

- write `AIFP-1`, not `AIFP1`;
- do not call every HTTP `402` interaction x402;
- do not describe AIFP-1 and AIFP-2 as one fee profile;
- do not describe a draft specification as production-ready merely because it is documented;
- avoid implying that a network is payment-live merely because a contract was deployed.

## 2. Current Economic Terminology

Current AIFP-1 reference values:

| Item | Current value |
|---|---:|
| Standard | `$0.0005` |
| Complex | `$0.002` |
| Premium | `$0.005` |
| AiFinPay protocol fee | `1%` / `100` bps |
| Creator/referral fee | `0` bps |
| Merchant amount | `99%` before external network/settlement costs |

AIFP-2/x402 uses `0/0` AiFinPay fees.

Old microcent prices and `100/1` belong only in clearly marked historical/superseded sections.

## 3. Money Formatting

- Use decimal strings in API/JSON examples: `"0.0005"`, not floating-point literals when exactness matters.
- For on-chain amounts, document token base units and decimals explicitly.
- Never round away a fee/profile mismatch in security-sensitive examples.
- Distinguish merchant amount, AiFinPay fee, creator/referral amount, total payer amount, and network gas where applicable.

## 4. Protocol Terminology

Use these terms consistently:

- **AIFP-1 challenge** — merchant payment-required message using HTTP `402`;
- **binding quote** — authoritative pre-payment merchant/resource/route/amount statement;
- **settlement reference / `tx_ref`** — evidence submitted after payer execution;
- **settlement verifier** — component that checks the actual chain/rail evidence;
- **receipt** — signed paid-access authorization issued after verified settlement;
- **route class** — AIFP-1 or AIFP-2/x402;
- **payment-live** — route with approved current implementation/evidence, not merely deployed.

Do not use "x402 challenge" as a synonym for AIFP-1 challenge.

## 5. Status Language

Preferred status labels:

- `Draft specification`
- `Experimental`
- `Reference implementation`
- `Verified deployment`
- `Verifier-ready`
- `E2E verified`
- `Payment-live`
- `Legacy / historical / superseded`

Use `production-ready` only when the relevant implementation has explicitly passed the release gate for that claim.

## 6. Documentation Voice

- precise and technical;
- active voice;
- claims should be evidence-backed;
- distinguish target architecture from deployed implementation;
- avoid exaggerated scale/latency/security claims without measured evidence;
- avoid invented partnerships, approvals, benchmarks, package availability, or chain support.

Normative `MUST / SHOULD / MAY` language should be reserved for normative or clearly designated specification/security/governance sections.

## 7. Code And Example Style

- JSON/YAML/JS/TS: 2-space indentation where compatible with the existing file/tooling.
- Python: 4 spaces.
- Use obvious placeholders for IDs, addresses, keys, hashes, and secrets.
- Never include real private keys, mnemonics, API secrets, merchant origin secrets, or production signing material.
- Examples should match the OpenAPI and JSON schema surfaces where they represent protocol objects.

Example AIFP-1 quote fragment:

```json
{
  "route_class": "AIFP-1",
  "pricing_tier": "standard",
  "merchant_amount": "0.0005",
  "treasury_bps": 100,
  "creator_bps": 0
}
```

## 8. Cross-Protocol Links

When AIFP-1 documentation needs identity or x402 functionality, link to the separate protocol rather than copying its normative wire format into AIFP-1.

Examples:

- "For x402 agent-payment support, see AIFP-2/x402."
- "For portable agent identity, see AIFP-3 / Agent Passport."

## 9. Package And Repository Naming

Only name a package as available when verified against its actual repository/package registry. Do not maintain speculative language matrices in AIFP-1 as if they were published products.

Repository links should use the current AiFinPay organization/repository names rather than deprecated naming.

## 10. Visual Style

For documentation visuals:

- favor clear system diagrams over decorative crypto imagery;
- use accessible contrast;
- keep diagrams readable in light and dark environments;
- avoid status colors that imply `live`/`verified` unless that status is true;
- keep protocol diagrams focused on data/payment flow and trust boundaries.

## 11. Synchronization Rule

When economics or route semantics change, update together:

1. AIFP-1 RFC;
2. economics document;
3. OpenAPI;
4. JSON schemas;
5. Postman/examples;
6. SDK reference/guides;
7. README/portal pages;
8. changelog/migration note.

Contradictory active examples are treated as defects, not harmless documentation drift.
