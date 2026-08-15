# Python AIFP-1 Quick Start

This page demonstrates the AIFP-1 protocol flow in Python-style pseudocode. Verify actual package names, published versions, and current APIs in their source/package registries before using package-specific code.

## Current Economics

```python
AIFP1_PRICES_USD = {
    "standard": "0.0005",
    "complex": "0.002",
    "premium": "0.005",
}
AIFP1_TREASURY_BPS = 100
AIFP1_CREATOR_BPS = 0
```

AIFP-2/x402 is a separate `0/0` route profile.

## Protocol-Oriented Example

```python
import uuid

async def pay_aifp1_resource(url, http, wallet):
    first = await http.get(url)
    if first.status_code != 402:
        return first

    challenge = first.json()
    if challenge.get("protocol") != "AIFP-1":
        raise RuntimeError("not an AIFP-1 challenge")

    quote_res = await http.post(
        challenge["quote_endpoint"],
        json={
            "merchant_id": challenge["merchant_id"],
            "resource": challenge["resource"],
            "pricing_tier": challenge["pricing_tier"],
            "units": 1,
        },
    )
    quote_res.raise_for_status()
    quote = quote_res.json()

    if quote.get("route_class") != "AIFP-1":
        raise RuntimeError("route mismatch")
    if int(quote.get("treasury_bps", -1)) != 100:
        raise RuntimeError("treasury fee mismatch")
    if int(quote.get("creator_bps", -1)) != 0:
        raise RuntimeError("creator fee mismatch")

    await assert_budget_allows(quote)

    # Build against the canonical verified deployment for this route.
    tx = await build_settlement_from_verified_registry(quote)

    # Signing remains local to the payer wallet.
    tx_ref = await wallet.sign_and_broadcast(tx)

    pay_res = await http.post(
        "https://api.aifinpay.io/v1/pay",
        headers={"Idempotency-Key": str(uuid.uuid4())},
        json={
            "quote_id": quote["quote_id"],
            "chain": quote["chain"],
            "asset": quote["asset"],
            "tx_ref": tx_ref,
        },
    )

    if pay_res.status_code == 202:
        raise RuntimeError("settlement pending; reconcile before another payment")
    pay_res.raise_for_status()
    receipt = pay_res.json()

    return await http.get(
        url,
        headers={"Payment-Receipt": receipt["receipt"]},
    )
```

## Safety Requirements

- distinguish AIFP-1 from x402 before payment;
- validate `100/0` economics before signing;
- apply budget/policy before signing;
- use `decimal.Decimal` or integer token units for money, not `float`;
- derive token amounts from actual token decimals;
- sign locally and submit only the settlement reference for verification;
- do not issue/trust a receipt until verification succeeds;
- reconcile a potentially broadcast transaction before retrying;
- reject duplicate/replayed settlement consumption.

## Exact Money Example

```python
from decimal import Decimal

required = Decimal("0.0005")
quoted = Decimal("0.0005")
assert quoted >= required
```

For on-chain values, prefer integer base units once asset decimals are known.

## Going Live

A route should not be enabled for real spend until its chain/asset has a canonical target, correct AIFP-1 economics, SDK transaction construction, settlement verification, token-decimal validation, and completed end-to-end evidence.

Changing a URL or API key alone is not a production-readiness gate.

See [AIFP-1 HTTP 402 Flow](../core-concepts/x402-flow.md) and [Agent SDK Specification](../aifp/03-AI-Agent-SDK-Specification.md).
