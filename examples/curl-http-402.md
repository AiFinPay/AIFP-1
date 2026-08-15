# Raw AIFP-1 HTTP 402 Flow

This example shows the AIFP-1 merchant-monetization protocol without assuming a specific SDK.

Current AIFP-1 economics are `treasuryBps=100`, `creatorBps=0`. The standard reference action price is `$0.0005`. AIFP-2/x402 is a separate `0/0` route profile.

## 1. Request Protected Resource

```bash
curl -i https://merchant.example.com/api/data \
  -H "Accept-Payment: aifp/1.0"
```

Illustrative response:

```http
HTTP/1.1 402 Payment Required
Content-Type: application/json
```

```json
{
  "error": "AIFP-402",
  "protocol": "AIFP-1",
  "merchant_id": "mrch_example",
  "resource": "/api/data",
  "pricing_tier": "standard",
  "reference_price_usd": "0.0005",
  "quote_endpoint": "https://api.aifinpay.io/v1/quote"
}
```

## 2. Create Binding Quote

```bash
curl https://api.aifinpay.io/v1/quote \
  -H "Authorization: Bearer $AIFP_AGENT_KEY" \
  -H "Content-Type: application/json" \
  -d '{"merchant_id":"mrch_example","resource":"/api/data","pricing_tier":"standard","units":1}'
```

Before signing a payment, the client should verify that the returned quote is AIFP-1 and uses `treasury_bps=100`, `creator_bps=0` with the expected merchant/resource/asset/chain.

If the service cannot verify the selected settlement route, quote creation should fail before the payer is instructed to send funds.

## 3. Sign And Broadcast Settlement

The payer wallet constructs/signs/broadcasts the transaction for the canonical verified settlement target. This step is chain/wallet specific and is intentionally not represented as a `curl` call that uploads the payer's private key.

Result:

```text
TX_REF=<transaction-or-settlement-reference>
```

Never send a private key, mnemonic, or recovery phrase to `/v1/pay`.

## 4. Submit Settlement For Verification

```bash
curl https://api.aifinpay.io/v1/pay \
  -H "Authorization: Bearer $AIFP_AGENT_KEY" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: <unique-request-id>" \
  -d '{"quote_id":"qt_...","asset":"USDC","chain":"polygon","tx_ref":"'"$TX_REF"'"}'
```

A receipt should only be returned after the service verifies that the settlement matches the binding quote. `202` means settlement/finality is still pending; reconcile before attempting another payment.

## 5. Retry With Receipt

```bash
curl https://merchant.example.com/api/data \
  -H "Payment-Receipt: $AIFP_RECEIPT"
```

The merchant verifies the receipt's signature and required merchant/resource/scope/amount/expiry/replay properties before granting access.
