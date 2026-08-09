# Python Quick Start

## What You Need

- Python 3.11 or newer.
- An AiFinPay sandbox merchant endpoint.
- A test wallet funded with sandbox tokens.
- A sandbox API key that starts with `sk_test_`.
- A test token source for sandbox funds. The public faucet URL is published with the hosted sandbox.

## Install

```bash
pip install --pre aifinpay-agent aifinpay-merchant
```

`alpha` means the API may change while the SDK surface is still being settled.

## Sandbox Example

```python
import asyncio
import os

from aifinpay_agent import Agent

async def main():
    agent = Agent(
        api_key=os.environ["AIFP_AGENT_KEY"],
        wallet_id=os.environ["AIFP_WALLET_ID"],
        base_url="https://sandbox.api.aifinpay.io",
    )

    response = await agent.call(
        "https://sandbox.merchant.example/api/data",
        headers={"Accept-Payment": "aifp/1.0"},
    )

    print(response.model_dump_json(indent=2))


if __name__ == "__main__":
    asyncio.run(main())
```

Example sandbox response:

```json
{
  "ok": true,
  "resource": "/api/data",
  "pricing_tier": "standard",
  "quote_id": "qt_sbx_01",
  "receipt_id": "rcpt_sbx_01",
  "receipt_status": "settled",
  "charged_amount": "0.0005",
  "protocol_fee": "0.0000001",
  "merchant_settlement": "0.0000099"
}
```

## What Happened Under The Hood

The SDK detected the `402` challenge, asked for a quote, paid the sandbox amount, received a
receipt token, and retried the request with that receipt attached. The token is a short-lived,
signed proof that binds the merchant, resource, amount, and nonce. The protocol flow is explained
in [x402 Flow](../core-concepts/x402-flow.md). Verification stays local to the merchant.

## Going To Production

- Audit the merchant contract and receipt verification path.
- Set explicit spend limits on the wallet.
- Switch the base URL from sandbox to production only after approval.
- Replace sandbox keys with production keys.
- Add monitoring for 402, 409, 410, 422, and 429 responses.
- Confirm the payout account and settlement rail before enabling live spend.

## Common Mistakes

- Forgetting to `await` the async client call.
- Mixing `sk_test_` and `sk_live_` keys.
- Reusing an expired quote.
- Reusing a nonce.
- Missing an async event loop when running the example in notebooks.
