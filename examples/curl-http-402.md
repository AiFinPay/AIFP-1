# Raw AIFP-1 HTTP 402 Flow

This example shows the AIFP-1 merchant-monetization protocol without assuming a specific SDK.

Current AIFP-1 economics are gross-inclusive `treasuryBps=100`, `creatorBps=0`. The Standard reference action price `$0.0005` is the **gross amount paid by the agent**: `$0.000495` goes to the merchant and `$0.000005` to AiFinPay. The 1% fee is not added on top. AIFP-2/x402 is a separate `0/0` route profile.

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

`reference_price_usd` is gross payer pricing, not the merchant's 99% net amount.

## 2. Create Binding Quote

```bash
curl https://api.aifinpay.io/v1/quote \
  -H "Authorization: Bearer $AIFP_AGENT_KEY" \
  -H "Content-Type: application/json" \
  -d '{"merchant_id":"mrch_example","resource":"/api/data","pricing_tier":"standard","units":1}'
```

Illustrative Standard quote breakdown:

```json
{
  "quote_id": "qt_example",
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

Before signing a payment, the client should verify:

```text
payer_total_amount = gross_amount
merchant_amount + protocol_fee_amount + creator_amount = gross_amount
creator_amount = 0
```

and that the returned quote is AIFP-1, uses `treasury_bps=100`, `creator_bps=0`, and matches the expected merchant/resource/asset/chain.

If the service cannot verify the selected settlement route, or the route implements fee-on-top rather than this gross split, quote creation should fail before the payer is instructed to send funds.

## 3. Sign And Broadcast Settlement

The payer wallet constructs/signs/broadcasts the transaction for the canonical verified settlement target. It settles **exactly the quoted `gross_amount`**, excluding separately disclosed network/gas cost. This step is chain/wallet specific and is intentionally not represented as a `curl` call that uploads the payer's private key.

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

A receipt should only be returned after the service verifies that the settlement matches the binding quote, including payer total = gross and the 99/1/0 split. `202` means settlement/finality is still pending; reconcile before attempting another payment.

## 5. Retry With Receipt

```bash
curl https://merchant.example.com/api/data \
  -H "Payment-Receipt: $AIFP_RECEIPT"
```

The merchant verifies the receipt's signature and required merchant/resource/scope/gross-amount/expiry/replay properties before granting access.
