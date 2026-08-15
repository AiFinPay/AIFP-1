# Developer Experience

AIFP-1 developer documentation should be predictable, machine-readable, and explicit about the difference between protocol design and verified implementation availability.

## Developer Surfaces

| Surface | Purpose |
|---|---|
| Root README | Protocol overview, economics, security invariants, canonical links |
| Docs portal | Role-based navigation and conceptual guidance |
| Canonical docs | RFC, economics, security, AIP governance |
| OpenAPI | Machine-readable AIFP-1 API contract |
| JSON Schemas | Machine-readable object/economics contract |
| Postman | Reference requests aligned to the OpenAPI contract |
| SDK docs | Protocol-facing behavior; actual package availability is verified externally |
| Examples | Copyable protocol recipes without embedded secrets |
| Sandbox directory | Local/configured test-flow guidance; no invented hosted sandbox |
| Tests / CI | Documentation, schema, OpenAPI, secret and conformance quality gates |

## Quality Bar

- Every active surface uses `$0.0005 / $0.002 / $0.005` and AIFP-1 `100/0`.
- AIFP-2/x402 `0/0` is explicit and separate.
- AIFP-3 identity is not embedded as a normative AIFP-1 payment API.
- Examples use local payer signing and `tx_ref` verification rather than sending private keys.
- A payable quote is never described as valid when the route verifier is unavailable.
- Package names, versions, public sandbox URLs, network status, benchmarks, and certifications are only stated when verified.
- `deployed`, `verifier-ready`, `E2E verified`, and `payment-live` remain distinct statuses.
- Security-sensitive flows link to the canonical security model.

## Implementation Discovery

Use the actual AiFinPay implementation repositories and package registries to discover current SDK/MCP releases and route support. This protocol repository is the source of truth for AIFP-1 semantics, not for the current deployment status of every implementation.
