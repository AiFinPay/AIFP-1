# Wallet Guide

This page explains the payer-wallet boundary in AIFP-1. It does not define or promise a particular custodial, MPC, fiat, or chain integration unless that capability is verified in the active implementation.

## AIFP-1 Wallet Requirement

For the preferred crypto settlement flow, the payer wallet/environment keeps signing local:

```text
binding quote
→ client validates AIFP-1 route/economics
→ wallet builds/approves/signs
→ payer broadcasts settlement
→ client submits tx_ref
→ settlement verifier checks actual payment
→ receipt issued only after verifier success
```

The AIFP-1 receipt service must not require the payer's private key, mnemonic, recovery phrase, or raw signing secret.

## Wallet Policy

A wallet/client integration should be able to enforce, before signing:

- maximum amount per payment;
- daily/rolling spend cap where promised;
- allowed merchants;
- allowed assets/chains;
- allowed route class;
- explicit approval thresholds where configured.

A durable spend cap must be concurrency-safe and must not silently reset on process restart.

## Settlement Support

Actual supported chains/assets are implementation facts. A route is only suitable for real AIFP-1 spend when its canonical target, asset decimals, transaction construction, `100/0` economics, settlement verifier, and end-to-end evidence are current.

## Related Protocols

AIFP-2/x402 may use the same wallet but follows a separate `0/0` route profile. AIFP-3 may provide identity/wallet binding, but it is not part of the AIFP-1 payment wire format.

## Read Next

- [Core Concepts](core-concepts/index.md)
- [Security Model](security-model.md)
- [Agent Guide](agent.md)
- [Protocol Economics](economics.md)
