# Security Policy

AiFinPay AIFP-1 covers merchant payment challenges, quotes, payer settlement references, settlement verification, receipts, merchant paid-access authorization, and related reconciliation metadata. Please report security issues privately.

## Reporting A Vulnerability

Do not open a public GitHub issue for vulnerabilities.

Email: security@aifinpay.io

Include:

- Affected component or document.
- Reproduction steps.
- Expected and actual behavior.
- Exploitability assessment.
- Suggested remediation if known.

## Scope

In scope for this repository:

- Receipt forgery or verification bypass.
- Settlement spoofing or verifier bypass.
- Gross/net/fee conservation failures, including fee-on-top drift.
- Replay protection failures.
- Idempotency and double-charge issues.
- Post-payment failures that can strand valid payer funds without receipt entitlement.
- JWKS, key identifier, or key-rotation weaknesses in the AIFP-1 receipt profile.
- Webhook signature/replay weaknesses where an AIFP-1 implementation uses webhooks.
- Free-quota or merchant-access controls that incorrectly treat caller-controlled identifiers as authenticated identity.
- OpenAPI or JSON Schema inconsistencies that could cause unsafe AIFP-1 implementations.
- Route/registry/deployment ambiguity that can direct a payer to the wrong economic profile or unverifiable target.

Agent Passport identity, delegation, reputation, and Passport cryptography belong to the separate **AIFP-3** protocol surface. Cross-protocol integration bugs may affect AIFP-1, but this repository does not define AIFP-3 security semantics.

Out of scope:

- Social engineering.
- Denial-of-service without a protocol-specific vulnerability.
- Vulnerabilities in third-party systems not controlled by AiFinPay.
- AIFP-2/x402 or AIFP-3 implementation defects that do not affect an AIFP-1 integration; report those in their relevant security channels/repositories.

## Cryptographic And Protocol Baseline

Current AIFP-1 security requirements include:

- EdDSA / Ed25519 for the current receipt-signature design unless a future approved profile explicitly changes it.
- Authenticated, confidential transport using a modern TLS configuration appropriate to the deployment/security policy; this repository does not hard-code an unevidenced single TLS-version claim as a protocol constant.
- Authenticated and replay-resistant webhooks where webhooks are implemented; the current documented webhook profile uses HMAC-SHA256.
- Merchant/audience, resource/scope, gross amount or quota, expiry, and replay/idempotency validation as required by the active receipt profile.
- Receipt expiry/TTL defined by the active receipt/profile and binding data; there is no universal 600-second protocol constant unless a ratified profile explicitly defines it.
- Idempotency retention/deduplication long enough for the implementation's retry/reconciliation model; there is no universal 24-hour protocol constant unless a ratified profile explicitly defines it.
- Pre-payment budget/policy checks. A valid settlement matching an already-issued payable quote must not be denied a receipt solely because a budget threshold is discovered after payment.
- Current AIFP-1 gross-inclusive economics: `payer_total_amount = gross_amount`, merchant + protocol fee + creator = gross, AiFinPay 1% of gross, creator 0, no fee-on-top.

## Disclosure Process

1. We acknowledge receipt.
2. We investigate and reproduce.
3. We coordinate remediation.
4. We publish an advisory when appropriate.
5. We credit reporters unless anonymity is requested.
