# MCP + AIFP-1 Quick Start

AiFinPay's MCP tooling can expose payment operations to an AI-agent host. This page describes the AIFP-1 route semantics an MCP integration must preserve; verify the current published MCP package/version and exact tool names in the SDK repository/package registry.

## Current AIFP-1 Economics

| Tier | Gross price paid by agent | Merchant 99% | AiFinPay 1% |
|---|---:|---:|---:|
| `standard` | `$0.0005` | `$0.000495` | `$0.000005` |
| `complex` | `$0.002` | `$0.00198` | `$0.00002` |
| `premium` | `$0.005` | `$0.00495` | `$0.00005` |

AIFP-1 uses gross-inclusive `treasuryBps=100`, `creatorBps=0`. The agent settles the gross quoted amount; the protocol fee is deducted from gross and is not added on top. AIFP-2/x402 is separate and uses `0/0`.

## Required MCP Routing Behavior

An MCP payment tool that accepts an arbitrary URL should not treat every `402` as the same payment protocol.

Safe high-level routing:

```text
request
  ↓
AIFP-1 challenge? ── yes → AIFP-1 gross quote → local payer settlement → verifier → receipt → retry
  │
  no
  ↓
x402 challenge? ──── yes → AIFP-2/x402 route/version handling
  │
  no
  ↓
return unsupported/non-payment response
```

An explicit/forced x402 facilitator selection means x402 intent and should bypass AIFP-1 detection. Conversely, an AIFP-1 budget rejection must not be retried through x402 to bypass the caller's spend cap.

## Conceptual AIFP-1 Tool Input

```json
{
  "merchant_id": "mrch_example",
  "resource": "/api/data",
  "pricing_tier": "standard",
  "max_amount_usd": "0.0005"
}
```

`max_amount_usd` is compared to the gross commercial amount the payer will settle, not the 99% merchant share.

The returned binding quote must be validated before any signing action:

```json
{
  "route_class": "AIFP-1",
  "gross_amount": "0.0005",
  "payer_total_amount": "0.0005",
  "merchant_amount": "0.000495",
  "protocol_fee_amount": "0.000005",
  "creator_amount": "0",
  "treasury_bps": 100,
  "creator_bps": 0,
  "asset": "USDC",
  "chain": "polygon"
}
```

The exact chain/asset above is illustrative. A tool should only offer a route that is current in the SDK/backend registry, independently verifiable, and able to prove the gross-inclusive 99/1/0 split.

## Non-Custodial Settlement

MCP tooling may orchestrate transaction construction but must not require the user/agent to send a private key or recovery phrase to the receipt service.

Expected flow:

1. obtain verifier-ready AIFP-1 quote;
2. validate `payer_total_amount = gross_amount` and the 99/1/0 amount conservation rule;
3. enforce MCP/agent budget policy against the gross payer amount;
4. construct transaction for the canonical route;
5. sign locally in the agent wallet;
6. broadcast exactly the quoted gross settlement amount;
7. submit `tx_ref` for verification;
8. receive receipt only after verification;
9. retry the protected request.

## Budget Handling

MCP tools must treat budget limits as hard policy.

- `max_amount_usd` should be checked against gross before signing;
- daily/window caps should be concurrency-safe;
- a budget skip must not be "laundered" into a different payment protocol/facilitator;
- ambiguous broadcast errors need reconciliation before a new payment attempt;
- an implementation must not budget against merchant net while settling gross.

## Protocol Classification

### AIFP-1

Recognize explicit AIFP-1 protocol/challenge structure and apply the gross-inclusive `100/0` merchant-monetization route: payer gross = merchant 99% + AiFinPay 1%, creator 0%.

### AIFP-2/x402

Recognize the actual supported x402 wire version/scheme. Unsupported x402 versions should return an explicit unsupported-version error rather than being mislabeled as AIFP-1 or as a generic facilitator failure.

## Going Live

Before an MCP integration enables real spend on an AIFP-1 route, confirm:

- canonical deployment target;
- current gross-inclusive `100/0` economics;
- payer total equals gross and no 1% fee is added on top;
- correct token decimals;
- SDK transaction construction;
- backend settlement verifier;
- replay/idempotency behavior;
- durable spend-cap behavior where promised;
- end-to-end evidence for the selected chain/asset.

Do not assume that installing the MCP package proves all documented chains/routes are payment-live.

See [AIFP-1 HTTP 402 Flow](../core-concepts/x402-flow.md) and [Agent SDK Specification](../aifp/03-AI-Agent-SDK-Specification.md).
