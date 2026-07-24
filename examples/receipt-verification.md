# Receipt Verification

Merchants verify receipts locally before serving a protected resource.

## Required Checks

| Check | Reject When |
| --- | --- |
| Signature | Signature cannot be verified with current JWKS key |
| Issuer | Issuer is not trusted |
| Audience | Merchant id does not match |
| Resource | Receipt resource does not match requested resource |
| Amount | Amount is below required resource price |
| Pricing tier | Tier is not the merchant-selected tier |
| Expiry | Receipt is expired |
| Nonce | Nonce was already used |

## Pseudocode

```ts
import { compareDecimalUsd } from "@aifinpay/merchant";

const claims = await verifyReceipt(receipt, { jwks });

assert(claims.aud === merchantId);
assert(claims.resource === request.path);
assert(compareDecimalUsd(claims.amount, requiredAmount) >= 0);
assert(claims.pricing_tier === requiredTier);
assert(claims.exp > now());
assert(await nonceStore.consume(claims.nonce));
```

`nonceStore.consume` must be atomic and linearizable, for example Redis
`SET key value NX EX ttl` with the consistency guarantees required by AIFP-1.
Do not implement receipt replay checks as separate `exists` then `set` operations.
