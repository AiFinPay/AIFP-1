# AIFP JSON Schemas

**Document:** AIFP-DOC-10 · **Status:** Conforming Artifact · **Governed by:** AIFP-1 (Doc 01)  
**Spec dialect:** JSON Schema 2020-12 · **Base `$id`:** `https://schemas.aifinpay.io/v1/`

> These schemas are the canonical machine-readable definitions of every AIFP protocol object. They MUST stay byte-consistent with the OpenAPI 3.1 components, the AIFP-1 normative spec, and the current protocol pricing model. Where documents differ, **AIFP-1 governs**.

Each schema below is independently publishable as a `.json` file under the `$id` base. A consolidated bundle is provided in [`/schemas/aifp.bundle.json`](#bundle).

---

## Index

| Object | `$id` | Source of truth |
|---|---|---|
| Payment Challenge | `payment-challenge.json` | AIFP-1 §6 |
| Quote | `quote.json` | AIFP-1 §16.1 |
| Receipt Token (claims) | `receipt-token.json` | AIFP-1 §7.3 |
| Receipt (envelope) | `receipt.json` | AIFP-1 §16.2 |
| Merchant | `merchant.json` | AIFP-1 §11 |
| Wallet | `wallet.json` | AIFP-1 §13 |
| Passport | `passport.json` | AIFP-1 §24, §10.2; Doc 03 §9 |
| Payment | `payment.json` | AIFP-1 §16.2 |
| Settlement | `settlement.json` | AIFP-1 §19 |
| Webhook | `webhook.json` | AIFP-1 §9.4 |
| Error | `error.json` | AIFP-1 §17.2 |

---

## Pricing Contract

| Tier | Minimum amount | Intended use |
|---|---:|---|
| `standard` | `$0.0005` | Simple read, single record, lightweight API request. |
| `complex` | `$0.002` | Search, aggregation, multi-source queries, higher compute. |
| `premium` | `$0.005` | AI inference, GPU workloads, deep analytics, premium data. |

The AiFinPay Protocol Fee is `1%` of every successful transaction. The remaining `99%` is settled to the merchant, excluding any applicable payment-network or settlement costs.

---

## Shared definitions (`$defs`)

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://schemas.aifinpay.io/v1/common.json",
  "title": "AIFP Common Definitions",
  "$defs": {
    "pricingTier": {
      "type": "string",
      "enum": ["standard", "complex", "premium"],
      "description": "Protocol pricing tier for the requested action."
    },
    "tierMinimumAmount": {
      "type": "string",
      "enum": ["0.0005", "0.002", "0.005"],
      "description": "Minimum USD amount for the selected pricing tier."
    },
    "protocolFeeRate": {
      "type": "number",
      "const": 0.01,
      "description": "AiFinPay Protocol Fee: 1% of each successful transaction."
    },
    "merchantSettlementRate": {
      "type": "number",
      "const": 0.99,
      "description": "Merchant settlement share before external network or settlement costs."
    },
    "asset": { "type": "string", "enum": ["USDC", "USDT", "PYUSD"] },
    "chain": {
      "type": "string",
      "enum": ["solana", "polygon", "avalanche", "bnb", "optimism", "arbitrum", "base", "unichain", "bot_chain", "xrpl_evm", "near", "aptos"]
    },
    "decimalUsd": { "type": "string", "pattern": "^[0-9]+\\.[0-9]{2,8}$", "examples": ["0.0005", "0.002", "0.005"], "description": "Per-request micropayment amount (2-8 fractional digits, no whole-dollar form)." },
    "monetaryUsd": { "type": "string", "pattern": "^[0-9]+(\\.[0-9]{1,8})?$", "examples": ["0.0005", "50.00", "100", "5"], "description": "Larger monetary value (settlement, payout, budget cap). Allows whole-dollar amounts; fractional part optional, 1-8 digits." },
    "merchantId": { "type": "string", "pattern": "^mrch_[A-Za-z0-9]+$" },
    "agentId": { "type": "string", "pattern": "^agt_[A-Za-z0-9]+$" },
    "walletId": { "type": "string", "pattern": "^wlt_[A-Za-z0-9]+$" },
    "quoteId": { "type": "string", "pattern": "^qt_[A-Za-z0-9]+$" },
    "receiptId": { "type": "string", "pattern": "^rcpt_[A-Za-z0-9]+$" },
    "passportId": { "type": "string", "pattern": "^pp_[A-Za-z0-9]+$" },
    "nonce": {
      "type": "string",
      "minLength": 22,
      "maxLength": 128,
      "pattern": "^[A-Za-z0-9_-]+$",
      "description": "Single-use anti-replay value, >=128 bits entropy from a CSPRNG (AIFP-1 §6.4, §18.3). Minimum 22 chars (base64url of 128 bits) or 32 chars (hex of 128 bits). The nonce MUST be identical across the challenge, quote, and receipt."
    }
  }
}
```

---

## Payment Challenge

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://schemas.aifinpay.io/v1/payment-challenge.json",
  "title": "AIFP Payment Challenge",
  "description": "Body returned with HTTP 402 (AIFP-1 §6).",
  "type": "object",
  "required": ["version", "scheme", "merchant_id", "resource", "pricing_tier", "currency", "nonce", "expires_at", "quote_endpoint"],
  "properties": {
    "version": { "type": "string", "const": "1.0" },
    "scheme": { "type": "string", "const": "aifp" },
    "merchant_id": { "$ref": "common.json#/$defs/merchantId" },
    "resource": { "type": "string" },
    "pricing_tier": { "$ref": "common.json#/$defs/pricingTier" },
    "estimated_amount": { "$ref": "common.json#/$defs/decimalUsd", "description": "Decimal USD estimate (SHOULD; not binding — use /quote for a binding amount)." },
    "currency": { "type": "string", "const": "USD" },
    "accepted_assets": { "type": "array", "items": { "$ref": "common.json#/$defs/asset" } },
    "accepted_chains": { "type": "array", "items": { "$ref": "common.json#/$defs/chain" } },
    "nonce": { "$ref": "common.json#/$defs/nonce" },
    "expires_at": { "type": "string", "format": "date-time" },
    "quote_endpoint": { "type": "string", "format": "uri", "description": "Where the agent requests a binding quote (AIFP-1 §6)." },
    "onboarding": { "type": "boolean", "default": false, "description": "true -> AIFP-402-ONBOARDING" }
  },
  "additionalProperties": false
}
```

---

## Quote

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://schemas.aifinpay.io/v1/quote.json",
  "title": "AIFP Quote",
  "type": "object",
  "required": ["quote_id", "merchant_id", "resource", "pricing_tier", "amount", "currency", "nonce", "expires_at"],
  "properties": {
    "quote_id": { "$ref": "common.json#/$defs/quoteId" },
    "merchant_id": { "$ref": "common.json#/$defs/merchantId" },
    "resource": { "type": "string" },
    "pricing_tier": { "$ref": "common.json#/$defs/pricingTier" },
    "amount": { "$ref": "common.json#/$defs/decimalUsd" },
    "currency": { "type": "string", "const": "USD" },
    "accepted_assets": { "type": "array", "items": { "$ref": "common.json#/$defs/asset" } },
    "accepted_chains": { "type": "array", "items": { "$ref": "common.json#/$defs/chain" } },
    "pay_to": { "type": "object", "additionalProperties": { "type": "string" } },
    "nonce": { "$ref": "common.json#/$defs/nonce" },
    "expires_at": { "type": "string", "format": "date-time" }
  },
  "additionalProperties": false
}
```

---

## Receipt Token (JWT claims)

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://schemas.aifinpay.io/v1/receipt-token.json",
  "title": "AIFP Receipt Token Claims",
  "description": "Decoded Ed25519 JWT claim set (AIFP-1 §7.3). Header alg MUST be EdDSA.",
  "type": "object",
  "required": ["iss", "sub", "aud", "resource", "amount", "nonce", "iat", "exp", "kid"],
  "properties": {
    "iss": { "type": "string", "const": "https://api.aifinpay.io" },
    "sub": { "$ref": "common.json#/$defs/agentId" },
    "aud": { "$ref": "common.json#/$defs/merchantId" },
    "resource": { "type": "string" },
    "pricing_tier": { "$ref": "common.json#/$defs/pricingTier" },
    "amount": { "$ref": "common.json#/$defs/decimalUsd" },
    "currency": { "type": "string", "const": "USD" },
    "asset": { "$ref": "common.json#/$defs/asset" },
    "chain": { "$ref": "common.json#/$defs/chain" },
    "tx_ref": { "type": "string" },
    "receipt_id": { "$ref": "common.json#/$defs/receiptId" },
    "nonce": { "$ref": "common.json#/$defs/nonce" },
    "iat": { "type": "integer" },
    "exp": { "type": "integer", "description": "Default TTL 600s after iat." },
    "kid": { "type": "string", "examples": ["aifp-2026-06"] },
    "quota": { "type": "integer", "minimum": 1, "description": "Optional multi-use claim (AIFP-1 §7.5). When present, the receipt grants `quota` redemptions for the same resource within its TTL; the nonce is consumed on the final use. Absent = single-use (default)." }
  },
  "additionalProperties": false
}
```

---

## Receipt (API envelope)

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://schemas.aifinpay.io/v1/receipt.json",
  "title": "AIFP Receipt Envelope",
  "type": "object",
  "required": ["receipt_id", "status"],
  "properties": {
    "receipt_id": { "$ref": "common.json#/$defs/receiptId" },
    "receipt": { "type": "string", "description": "Compact EdDSA JWT." },
    "status": { "type": "string", "enum": ["settled", "settling", "expired", "revoked"] },
    "tx_ref": { "type": "string" },
    "amount": { "$ref": "common.json#/$defs/decimalUsd" },
    "protocol_fee_rate": { "$ref": "common.json#/$defs/protocolFeeRate" },
    "merchant_settlement_rate": { "$ref": "common.json#/$defs/merchantSettlementRate" },
    "protocol_fee_amount": { "$ref": "common.json#/$defs/monetaryUsd" },
    "merchant_settlement_amount": { "$ref": "common.json#/$defs/monetaryUsd" },
    "expires_at": { "type": "string", "format": "date-time" },
    "poll": { "type": "string", "description": "Present on 202 async settlement." }
  },
  "additionalProperties": false
}
```

---

## Merchant

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://schemas.aifinpay.io/v1/merchant.json",
  "title": "AIFP Merchant",
  "type": "object",
  "required": ["merchant_id", "name", "created_at"],
  "properties": {
    "merchant_id": { "$ref": "common.json#/$defs/merchantId" },
    "name": { "type": "string" },
    "settlement_mode": { "type": "string", "enum": ["stablecoin", "fiat", "hybrid"] },
    "protocol_fee_rate": { "$ref": "common.json#/$defs/protocolFeeRate" },
    "merchant_settlement_rate": { "$ref": "common.json#/$defs/merchantSettlementRate" },
    "resources": { "type": "object", "additionalProperties": { "$ref": "common.json#/$defs/pricingTier" } },
    "created_at": { "type": "string", "format": "date-time" }
  },
  "additionalProperties": false
}
```

---

## Wallet

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://schemas.aifinpay.io/v1/wallet.json",
  "title": "AIFP Wallet",
  "type": "object",
  "required": ["wallet_id", "agent_id", "type"],
  "properties": {
    "wallet_id": { "$ref": "common.json#/$defs/walletId" },
    "agent_id": { "$ref": "common.json#/$defs/agentId" },
    "type": { "type": "string", "enum": ["custodial", "non_custodial"] },
    "balances": { "type": "object", "additionalProperties": { "type": "string" } },
    "budget": {
      "type": "object",
      "properties": {
        "window": { "type": "string", "enum": ["hour", "day", "week", "month"] },
        "cap_usd": { "$ref": "common.json#/$defs/monetaryUsd" }
      }
    }
  },
  "additionalProperties": false
}
```

---

## Passport

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://schemas.aifinpay.io/v1/passport.json",
  "title": "AIFP Agent Passport",
  "type": "object",
  "required": ["passport_id", "agent_id", "reputation", "risk", "trust_level"],
  "properties": {
    "passport_id": { "$ref": "common.json#/$defs/passportId" },
    "agent_id": { "$ref": "common.json#/$defs/agentId" },
    "public_key": { "type": "string", "description": "Ed25519 public key (base64url)." },
    "reputation": { "type": "integer", "minimum": 0, "maximum": 1000, "default": 500 },
    "risk": { "type": "integer", "minimum": 0, "maximum": 100 },
    "trust_level": { "type": "string", "enum": ["untrusted", "basic", "verified", "enterprise"] },
    "created_at": { "type": "string", "format": "date-time" }
  },
  "additionalProperties": false
}
```

---

## Payment

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://schemas.aifinpay.io/v1/payment.json",
  "title": "AIFP Payment Request",
  "type": "object",
  "required": ["quote_id", "wallet_id", "asset", "chain"],
  "properties": {
    "quote_id": { "$ref": "common.json#/$defs/quoteId" },
    "wallet_id": { "$ref": "common.json#/$defs/walletId" },
    "asset": { "$ref": "common.json#/$defs/asset" },
    "chain": { "$ref": "common.json#/$defs/chain" }
  },
  "additionalProperties": false
}
```

---

## Settlement

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://schemas.aifinpay.io/v1/settlement.json",
  "title": "AIFP Settlement",
  "type": "object",
  "required": ["receipt_id", "status", "rail"],
  "properties": {
    "receipt_id": { "$ref": "common.json#/$defs/receiptId" },
    "status": { "type": "string", "enum": ["pending", "confirmed", "failed"] },
    "rail": { "type": "string", "enum": ["stablecoin", "fiat"] },
    "chain": { "$ref": "common.json#/$defs/chain" },
    "tx_ref": { "type": "string" },
    "confirmations": { "type": "integer", "minimum": 0 }
  },
  "additionalProperties": false
}
```

---

## Webhook

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://schemas.aifinpay.io/v1/webhook.json",
  "title": "AIFP Webhook Event",
  "type": "object",
  "required": ["id", "type", "created", "data"],
  "properties": {
    "id": { "type": "string", "examples": ["evt_2a9f"] },
    "type": {
      "type": "string",
      "enum": ["payment.succeeded", "payment.pending", "payment.failed", "receipt.issued", "receipt.redeemed", "receipt.expired", "receipt.revoked", "settlement.completed", "payout.completed", "dispute.opened", "passport.updated"]
    },
    "created": { "type": "integer" },
    "data": { "type": "object" }
  },
  "additionalProperties": false
}
```

> **Signature:** Webhook deliveries carry `AIFP-Signature: t=<ts>,v1=<hmac>` (**HMAC-SHA256** over the raw body, using a per-merchant shared secret). Verify the HMAC and the timestamp (5-minute replay window) before trusting the payload. This is a symmetric signature — merchants do NOT need to fetch JWKS to verify webhooks (AIFP-1 §9.4, §18.4).

---

## Error

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://schemas.aifinpay.io/v1/error.json",
  "title": "AIFP Error",
  "type": "object",
  "required": ["error"],
  "properties": {
    "error": {
      "type": "object",
      "required": ["type", "code", "message"],
      "properties": {
        "type": { "type": "string" },
        "code": {
          "type": "string",
          "enum": ["AIFP-400", "AIFP-401", "AIFP-402", "AIFP-402-ONBOARDING", "AIFP-403", "AIFP-403-BUDGET-EXCEEDED", "AIFP-404", "AIFP-409", "AIFP-410", "AIFP-422-SIGNATURE", "AIFP-422-AMOUNT", "AIFP-425", "AIFP-429", "AIFP-5xx"]
        },
        "message": { "type": "string" },
        "request_id": { "type": "string" },
        "doc": { "type": "string", "format": "uri" }
      },
      "additionalProperties": false
    }
  },
  "additionalProperties": false
}
```

---

## Bundle

For tooling that prefers a single file, publish `schemas/aifp.bundle.json` with all the above under a top-level `$defs`, each entry retaining its `$id`. Validation tooling (Ajv 2020, `check-jsonschema`, `quicktype`) MUST resolve `$ref`s against the `https://schemas.aifinpay.io/v1/` base.

```bash
# Validate an example receipt envelope against the schema
npx ajv-cli validate -s webhook.json -d examples/settlement.completed.json --spec=draft2020
```
