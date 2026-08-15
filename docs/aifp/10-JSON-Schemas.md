# AIFP-1 JSON Schema Contract

**Document:** AIFP-DOC-10  
**Status:** Draft conforming artifact  
**Schema dialect:** JSON Schema 2020-12  
**Governed by:** [AIFP-1 RFC](./01-AIFP-1-RFC-Payment-Protocol-Specification.md)

This document defines the current machine-readable object shapes required by the AIFP-1 merchant-monetization profile. It intentionally excludes AIFP-2/x402 and AIFP-3 Agent Passport objects; those are separate protocol surfaces.

## Current Economics

| Field | AIFP-1 value |
|---|---:|
| `standard` reference action | `$0.0005` |
| `complex` reference action | `$0.002` |
| `premium` reference action | `$0.005` |
| `protocolFeeRate` | `0.01` |
| `merchantSettlementRate` | `0.99` |
| `creatorFeeRate` | `0` |
| `treasury_bps` | `100` |
| `creator_bps` | `0` |

AIFP-2/x402 uses a separate `0/0` fee profile and MUST NOT be inferred from these schemas.

---

## Common Definitions

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://schemas.aifinpay.io/aifp-1/common.json",
  "title": "AIFP-1 Common Definitions",
  "$defs": {
    "routeClass": {
      "type": "string",
      "const": "AIFP-1"
    },
    "pricingTier": {
      "type": "string",
      "enum": ["standard", "complex", "premium"]
    },
    "referenceActionPrice": {
      "type": "string",
      "enum": ["0.0005", "0.002", "0.005"]
    },
    "decimalAmount": {
      "type": "string",
      "pattern": "^[0-9]+(?:\\.[0-9]+)?$",
      "examples": ["0.0005", "0.002", "0.005", "1", "10.25"]
    },
    "protocolFeeRate": {
      "type": "string",
      "const": "0.01"
    },
    "merchantSettlementRate": {
      "type": "string",
      "const": "0.99"
    },
    "creatorFeeRate": {
      "type": "string",
      "const": "0"
    },
    "treasuryBps": {
      "type": "integer",
      "const": 100
    },
    "creatorBps": {
      "type": "integer",
      "const": 0
    },
    "merchantId": {
      "type": "string",
      "minLength": 1
    },
    "quoteId": {
      "type": "string",
      "minLength": 1
    },
    "receiptId": {
      "type": "string",
      "minLength": 1
    }
  }
}
```

---

## AIFP-1 Payment Challenge

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://schemas.aifinpay.io/aifp-1/payment-challenge.json",
  "title": "AIFP-1 Payment Challenge",
  "type": "object",
  "required": ["protocol", "merchant_id", "resource", "pricing_tier", "quote_endpoint"],
  "properties": {
    "protocol": { "type": "string", "const": "AIFP-1" },
    "merchant_id": { "type": "string", "minLength": 1 },
    "resource": { "type": "string", "minLength": 1 },
    "scope": { "type": "string" },
    "pricing_tier": { "type": "string", "enum": ["standard", "complex", "premium"] },
    "reference_price_usd": { "type": "string", "enum": ["0.0005", "0.002", "0.005"] },
    "quote_endpoint": { "type": "string", "format": "uri" },
    "expires_at": { "type": "string", "format": "date-time" }
  },
  "additionalProperties": true
}
```

The challenge is informational. The **binding Quote** controls the actual settlement amount and route.

---

## Quote Request

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://schemas.aifinpay.io/aifp-1/quote-request.json",
  "title": "AIFP-1 Quote Request",
  "type": "object",
  "required": ["merchant_id", "resource", "pricing_tier"],
  "properties": {
    "merchant_id": { "type": "string", "minLength": 1 },
    "resource": { "type": "string", "minLength": 1 },
    "scope": { "type": "string" },
    "pricing_tier": { "type": "string", "enum": ["standard", "complex", "premium"] },
    "units": { "type": "integer", "minimum": 1, "default": 1 },
    "preferred_asset": { "type": "string" },
    "preferred_chain": { "type": "string" }
  },
  "additionalProperties": false
}
```

---

## Binding Quote

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://schemas.aifinpay.io/aifp-1/quote.json",
  "title": "AIFP-1 Binding Quote",
  "type": "object",
  "required": [
    "quote_id",
    "protocol",
    "route_class",
    "merchant_id",
    "resource",
    "merchant_amount",
    "treasury_bps",
    "creator_bps",
    "asset",
    "chain",
    "expires_at"
  ],
  "properties": {
    "quote_id": { "type": "string", "minLength": 1 },
    "protocol": { "type": "string", "const": "AIFP-1" },
    "route_class": { "type": "string", "const": "AIFP-1" },
    "merchant_id": { "type": "string", "minLength": 1 },
    "resource": { "type": "string", "minLength": 1 },
    "scope": { "type": "string" },
    "pricing_tier": { "type": "string", "enum": ["standard", "complex", "premium"] },
    "merchant_amount": { "type": "string", "pattern": "^[0-9]+(?:\\.[0-9]+)?$" },
    "total_amount": { "type": "string", "pattern": "^[0-9]+(?:\\.[0-9]+)?$" },
    "currency": { "type": "string", "default": "USD" },
    "treasury_bps": { "type": "integer", "const": 100 },
    "creator_bps": { "type": "integer", "const": 0 },
    "asset": { "type": "string", "minLength": 1 },
    "chain": { "type": "string", "minLength": 1 },
    "settlement_target": { "type": "string" },
    "payment_id": { "type": "string" },
    "order_id": { "type": "string" },
    "verifier_profile": { "type": "string" },
    "expires_at": { "type": "string", "format": "date-time" }
  },
  "additionalProperties": true
}
```

A quote MUST NOT be returned as payable if the selected route cannot be verified by the active settlement verifier.

---

## Pay Request

The payer executes settlement outside the receipt service and submits the resulting reference for verification.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://schemas.aifinpay.io/aifp-1/pay-request.json",
  "title": "AIFP-1 Pay Request",
  "type": "object",
  "required": ["quote_id", "chain", "asset", "tx_ref"],
  "properties": {
    "quote_id": { "type": "string", "minLength": 1 },
    "chain": { "type": "string", "minLength": 1 },
    "asset": { "type": "string", "minLength": 1 },
    "tx_ref": { "type": "string", "minLength": 1 }
  },
  "additionalProperties": false
}
```

A private key, recovery phrase, or raw signing secret MUST NOT be part of this request schema.

---

## Receipt Envelope

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://schemas.aifinpay.io/aifp-1/receipt.json",
  "title": "AIFP-1 Receipt Envelope",
  "type": "object",
  "required": [
    "receipt_id",
    "protocol",
    "route_class",
    "merchant_id",
    "status",
    "receipt",
    "issued_at",
    "expires_at"
  ],
  "properties": {
    "receipt_id": { "type": "string", "minLength": 1 },
    "protocol": { "type": "string", "const": "AIFP-1" },
    "route_class": { "type": "string", "const": "AIFP-1" },
    "merchant_id": { "type": "string", "minLength": 1 },
    "resource": { "type": "string" },
    "scope": { "type": "string" },
    "quote_id": { "type": "string" },
    "tx_ref": { "type": "string" },
    "merchant_amount": { "type": "string", "pattern": "^[0-9]+(?:\\.[0-9]+)?$" },
    "treasury_bps": { "type": "integer", "const": 100 },
    "creator_bps": { "type": "integer", "const": 0 },
    "status": { "type": "string", "enum": ["settled", "final"] },
    "receipt": { "type": "string", "minLength": 1 },
    "issued_at": { "type": "string", "format": "date-time" },
    "expires_at": { "type": "string", "format": "date-time" }
  },
  "additionalProperties": true
}
```

A receipt may only be created after the settlement verifier confirms the binding quote.

---

## Pending Settlement

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://schemas.aifinpay.io/aifp-1/pending-settlement.json",
  "title": "AIFP-1 Pending Settlement",
  "type": "object",
  "required": ["status"],
  "properties": {
    "status": { "type": "string", "const": "pending" },
    "receipt_id": { "type": "string" },
    "retry_after_seconds": { "type": "integer", "minimum": 1 }
  },
  "additionalProperties": false
}
```

Pending is not equivalent to verified or paid. Protected access MUST NOT be granted unless the active receipt/finality policy permits it.

---

## Assisted Verify Request

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://schemas.aifinpay.io/aifp-1/verify-request.json",
  "title": "AIFP-1 Assisted Verify Request",
  "type": "object",
  "required": ["receipt", "merchant_id", "resource"],
  "properties": {
    "receipt": { "type": "string", "minLength": 1 },
    "merchant_id": { "type": "string", "minLength": 1 },
    "resource": { "type": "string", "minLength": 1 },
    "required_amount": { "type": "string", "pattern": "^[0-9]+(?:\\.[0-9]+)?$" }
  },
  "additionalProperties": false
}
```

Merchant implementations SHOULD verify receipts locally where supported. Assisted verification is an optional compatibility surface, not a substitute for pre-receipt settlement verification.

---

## Error Object

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://schemas.aifinpay.io/aifp-1/error.json",
  "title": "AIFP-1 Error",
  "type": "object",
  "required": ["error"],
  "properties": {
    "error": { "type": "string" },
    "detail": { "type": "string" },
    "request_id": { "type": "string" }
  },
  "additionalProperties": true
}
```

---

## Conformance Rules

Machine-readable AIFP-1 artifacts are conformant only if they agree on all of the following:

1. protocol/route class is `AIFP-1`;
2. standard preset prices are `$0.0005 / $0.002 / $0.005`;
3. `protocolFeeRate = 0.01` and `treasury_bps = 100`;
4. `creatorFeeRate = 0` and `creator_bps = 0`;
5. `merchantSettlementRate = 0.99` before external network/settlement costs;
6. payer settlement reference is verified before receipt issuance;
7. no private signing key is sent to the receipt service;
8. unsupported or unverifiable settlement routes fail before payment;
9. AIFP-2/x402 `0/0` is not silently represented as AIFP-1.

Legacy schema examples using `$0.00001 / $0.00006 / $0.00010` or `100/1` are superseded and must not be used for current integration generation.
