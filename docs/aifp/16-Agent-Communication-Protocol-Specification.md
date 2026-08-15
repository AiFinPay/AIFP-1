# Agent Communication Protocol (ACP) — Draft Companion Specification

**Document:** AIFP-DOC-16  
**Status:** Experimental draft  
**Relationship:** Companion messaging design; not part of the normative AIFP-1 payment object model unless explicitly referenced by an accepted AIP

ACP describes a possible structured agent-to-agent messaging layer. It may carry payment metadata, but it must not collapse AIFP-1, AIFP-2/x402, or AIFP-3 identity into one protocol.

## 1. Protocol Boundaries

| Surface | Purpose | Current economics |
|---|---|---:|
| **AIFP-1** | Merchant AI-traffic/resource monetization | `100/0` |
| **AIFP-2/x402** | Separate x402-style agent payment route | `0/0` |
| **AIFP-3** | Agent identity / Passport | N/A |
| **ACP** | Structured agent-to-agent messaging envelope | No independent fee profile |

An ACP message carrying an AIFP-1 payment challenge must identify that payment profile as AIFP-1. An ACP message carrying x402 data must identify AIFP-2/x402 and its supported wire version.

## 2. Current AIFP-1 Reference Prices

When ACP advertises AIFP-1 reference tiers, use:

| Tier | Price/action |
|---|---:|
| `standard` | `$0.0005` |
| `complex` | `$0.002` |
| `premium` | `$0.005` |

Do not use the superseded `$0.00001 / $0.00006 / $0.00010` values as current pricing.

## 3. ACP Envelope

Illustrative envelope:

```json
{
  "acp_version": "0.1-draft",
  "message_id": "msg_example",
  "timestamp": "2026-08-15T12:00:00Z",
  "sender": {
    "agent_id": "agent_a"
  },
  "recipient": {
    "agent_id": "agent_b"
  },
  "type": "request",
  "payload": {}
}
```

Recommended fields:

- `acp_version` — ACP wire version;
- `message_id` — unique message identifier;
- `timestamp` — freshness/replay input;
- `sender` / `recipient` — identifiers appropriate to the active identity profile;
- `type` — request/response/challenge/payment/status or future versioned types;
- `payload` — type-specific data.

ACP itself does not define an authenticated Passport simply by carrying an `agent_id`. If AIFP-3 or another identity scheme is used, its proof must be validated according to that protocol.

## 4. Request Example

```json
{
  "acp_version": "0.1-draft",
  "message_id": "msg_request_1",
  "timestamp": "2026-08-15T12:00:00Z",
  "sender": { "agent_id": "agent_a" },
  "recipient": { "agent_id": "agent_b" },
  "type": "request",
  "payload": {
    "action": "search",
    "resource": "/company?q=Acme",
    "max_price_usd": "0.005",
    "payment_profiles": ["AIFP-1", "AIFP-2/x402"]
  }
}
```

The sender may advertise acceptable payment profiles and a maximum spend policy. The receiver must not assume that the sender supports a payment profile that was not offered.

## 5. AIFP-1 Challenge Over ACP

```json
{
  "acp_version": "0.1-draft",
  "message_id": "msg_challenge_1",
  "timestamp": "2026-08-15T12:00:01Z",
  "sender": { "agent_id": "agent_b" },
  "recipient": { "agent_id": "agent_a" },
  "type": "challenge",
  "payload": {
    "in_response_to": "msg_request_1",
    "payment_profile": "AIFP-1",
    "challenge": {
      "protocol": "AIFP-1",
      "merchant_id": "merchant_b",
      "resource": "/company?q=Acme",
      "pricing_tier": "complex",
      "reference_price_usd": "0.002",
      "quote_endpoint": "https://api.aifinpay.io/v1/quote"
    }
  }
}
```

This is an **AIFP-1** challenge transported inside ACP. It must not be labeled x402 merely because a payment is required.

## 6. AIFP-1 Payment Response

After obtaining an AIFP-1 receipt through the normal quote → payer settlement → settlement verification flow, an agent may carry the receipt back in ACP:

```json
{
  "acp_version": "0.1-draft",
  "message_id": "msg_payment_1",
  "timestamp": "2026-08-15T12:00:05Z",
  "sender": { "agent_id": "agent_a" },
  "recipient": { "agent_id": "agent_b" },
  "type": "payment",
  "payload": {
    "in_response_to": "msg_challenge_1",
    "payment_profile": "AIFP-1",
    "receipt": "<SIGNED_AIFP1_RECEIPT>"
  }
}
```

The receiving agent/merchant must verify the receipt according to AIFP-1. ACP transport does not weaken audience/resource/scope/expiry/replay checks.

## 7. AIFP-2/x402 Over ACP

If a future ACP version carries x402 negotiation/payment data:

- `payment_profile` must identify AIFP-2/x402;
- the x402 wire version/scheme/network must be explicit;
- the client must use the AIFP-2 `0/0` AiFinPay fee policy;
- AIFP-1 `100/0` must not be silently selected as fallback;
- unsupported x402 wire versions must fail explicitly.

This document does not define the x402 wire format.

## 8. Discovery

A future ACP endpoint may expose a `.well-known` capability document. Such a document should clearly separate:

- ACP messaging versions;
- supported payment profiles;
- supported actions/capabilities;
- identity proof mechanisms;
- endpoint/transports.

Illustrative draft:

```json
{
  "acp_versions": ["0.1-draft"],
  "agent_id": "agent_b",
  "capabilities": ["search", "retrieve"],
  "payment_profiles": {
    "AIFP-1": {
      "pricing_tiers": ["standard", "complex"],
      "reference_prices_usd": {
        "standard": "0.0005",
        "complex": "0.002"
      }
    },
    "AIFP-2/x402": {
      "status": "implementation-specific"
    }
  }
}
```

Do not advertise a chain or payment profile as live unless the underlying implementation has current conformance evidence.

## 9. Transport

ACP is intended to be transport-agnostic. Candidate transports include:

- HTTP request/response;
- WebSocket;
- SSE for server-to-client progress;
- other authenticated messaging transports.

P2P/libp2p is an optional future implementation idea, not a guaranteed AIFP-1 feature.

## 10. Security

ACP implementations should address:

- message replay;
- sender authentication where identity matters;
- recipient binding;
- timestamp/freshness policy;
- duplicate message IDs;
- payload size limits;
- SSRF if messages can trigger network fetches;
- payment-profile confusion;
- cross-protocol receipt reuse;
- budget enforcement before payment;
- untrusted metadata.

A caller-controlled `agent_id` must not be treated as cryptographic identity without an authenticated identity proof.

## 11. Payment Safety

When ACP triggers AIFP-1 payment:

1. receiver emits an AIFP-1 challenge;
2. payer obtains a verifier-ready AIFP-1 binding quote;
3. payer signs/broadcasts settlement locally;
4. settlement is independently verified;
5. receipt is issued;
6. ACP carries that receipt back;
7. receiver validates it before returning paid work.

ACP must not create a shortcut that allows a receipt to be issued before settlement verification.

## 12. Status

ACP is experimental and should not be presented as a production standard merely because this document exists. Promotion to a stable protocol should require an accepted governance proposal, interoperable implementations, security review, and conformance tests.

## References

- [AIFP-1 RFC](./01-AIFP-1-RFC-Payment-Protocol-Specification.md)
- [AIFP-1 Economics](../economics.md)
- [Agent SDK Specification](./03-AI-Agent-SDK-Specification.md)
- [AIP Process](./06-AIP-Improvement-Proposal-Process.md)
