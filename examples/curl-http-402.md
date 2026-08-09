# Raw HTTP 402 Flow

This example shows the protocol without an SDK.

## 1. Request Protected Resource

```bash
curl -i https://merchant.example.com/api/data \
  -H "Accept-Payment: aifp/1.0"
```

Expected response:

```http
HTTP/1.1 402 Payment Required
Content-Type: application/json
```

```json
{
  "payment_challenge": {
    "version": "1.0",
    "scheme": "aifp",
    "merchant_id": "mrch_9f3a1c2b",
    "resource": "/api/data",
    "pricing_tier": "standard",
    "estimated_amount": "0.0005",
    "currency": "USD",
    "quote_endpoint": "https://api.aifinpay.io/v1/quote"
  }
}
```

## 2. Create Quote

```bash
curl https://api.aifinpay.io/v1/quote \
  -H "Authorization: Bearer $AIFP_AGENT_KEY" \
  -H "Content-Type: application/json" \
  -d '{"merchant_id":"mrch_9f3a1c2b","resource":"/api/data","pricing_tier":"standard"}'
```

## 3. Pay

```bash
curl https://api.aifinpay.io/v1/pay \
  -H "Authorization: Bearer $AIFP_AGENT_KEY" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: <unique-request-id>" \
  -d '{"quote_id":"qt_...","wallet_id":"wlt_...","asset":"USDC","chain":"polygon"}'
```

## 4. Retry With Receipt

```bash
curl https://merchant.example.com/api/data \
  -H "Payment-Receipt: $AIFP_RECEIPT"
```

