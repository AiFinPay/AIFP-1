# AGENTS.md — Protocol-AIFP-1

This repository is the **public protocol foundation** for AiFinPay AIFP-1, not a runnable service. It contains the canonical RFC/specification set, OpenAPI contract, JSON schemas, SDK design surface, AIPs, and documentation portal. Keep expectations aligned: there are no application entrypoints, no tests to run, and no CI pipelines defined inside this repo.

## What this repo actually holds

- `docs/aifp/` — canonical AIFP-1 documents (01–16). The **normative source of truth** is `docs/aifp/01-AIFP-1-RFC-Payment-Protocol-Specification.md`.
- `docs/aifp/08-OpenAPI-3.1-Specification.yaml` — machine-readable API contract.
- `docs/aifp/09-Postman-Collection.json` — API exploration collection.
- `docs/aifp/10-JSON-Schemas.md` — JSON Schema definitions.
- `docs/` — human-readable documentation portal (entry point: `docs/index.md`).
- `aips/` — AiFinPay Improvement Proposals; governed by `docs/aifp/06-AIP-Improvement-Proposal-Process.md`.
- `README.md`, `LICENSE`, `SECURITY.md`, `SUPPORT.md`, `CODE_OF_CONDUCT.md` — project health files.
- `package.json` — meta-package only. The single dependency (`@daochild/agents-config`) is for agent tooling configuration, not runtime code.

## What is intentionally elsewhere

The actual implementations live in **separate repositories under `github.com/aifinpay`**:

- `server` — reference control plane (quote, pay, receipt authority, settlement).
- `merchant-js`, `agent-js`, `aifinpay-python`, `aifp-go`, `aifinpay-rust`, `aifinpay-java`, `aifinpay-php`, `aifinpay-dotnet` — per-language SDKs.
- `openapi`, `schemas`, `conformance`, `examples`, `portal`, `postman`, `brand` — dedicated artifact repos.
- `.github` — org-level reusable workflows and issue/PR templates.

Do not add implementation code, SDKs, examples, or test suites here unless the project explicitly restructures this repo.

## Editing rules

1. **Prefer executable sources of truth over prose.** If documentation conflicts with `08-OpenAPI-3.1-Specification.yaml` or `10-JSON-Schemas.md`, trust the machine-readable contract and update the prose.
2. **Keep canonical documents consistent.** Any change to protocol behavior (pricing tiers, fee, networks, error codes, receipt TTL, headers, endpoints) must propagate through:
   - `docs/aifp/01-AIFP-1-RFC-Payment-Protocol-Specification.md`
   - `docs/aifp/08-OpenAPI-3.1-Specification.yaml`
   - `docs/aifp/10-JSON-Schemas.md`
   - `docs/aifp/09-Postman-Collection.json`
   - relevant AIPs in `aips/`
   - overview pages in `docs/` (architecture, quickstart, merchant, agent, wallet, security-model, conformance)
3. **Use the AIP process for protocol changes.** For any change to wire format, APIs, schemas, or governance, open or reference an AIP per `docs/aifp/06-AIP-Improvement-Proposal-Process.md`. Small docs fixes or typo corrections do not need an AIP.
4. **Maintain the navigation contract.** Every important document should be reachable within two clicks from `README.md`. Update `docs/navigation.md` and `docs/SUMMARY.md` when adding or moving pages.
5. **Markdown style.** Long lines and compact tables are allowed because RFC-style specifications require them. The repo-level config is `.markdownlint-cli2.yaml`:
   - `MD013` (line length) disabled
   - `MD060` (table column style) disabled

## Invariants likely to drift

When editing any of the following, check every canonical artifact for consistency:

- Pricing tiers: `standard` ($0.00001), `complex` ($0.00006), `premium` ($0.00010).
- Protocol fee: 1% of successful transactions.
- Default free quota: 100 requests per agent.
- Receipt TTL: 600 seconds.
- Quote TTL: 300 seconds.
- Idempotency window: 24 hours.
- Supported networks: 12 total (see AIFP-1 Appendix B / Doc 08 / Doc 10).
- Supported assets: USDC, USDT, PYUSD.
- Base URLs: `https://api.aifinpay.io/v1` (prod), `https://sandbox.api.aifinpay.io/v1` (sandbox).

## AIP workflow in this repo

- AIP index: `aips/README.md`.
- Process: `docs/aifp/06-AIP-Improvement-Proposal-Process.md`.
- Template headers: `aip`, `title`, `author`, `type`, `category` (Standards Track only), `status`, `created`, `requires`, `supersedes`.
- Status flow: `Idea → Draft → Review → Last Call → Accepted → Final`.
- A Standards Track AIP cannot reach `Final` without a reference implementation and passing conformance tests.

## Contribution guardrails

- Security issues: follow `SECURITY.md`; do not open public issues for vulnerabilities.
- License: code and machine-readable artifacts are Apache-2.0; documentation and specifications are CC BY 4.0. See `LICENSE`.
- DCO sign-off is required for contributions (per Doc 15 §6).
- PRs changing protocol/API/schema must include: linked AIP, backward-compatibility impact (PATCH/MINOR/MAJOR), which docs were updated, and confirmation that OpenAPI/JSON Schemas match.

## What not to expect

- No `npm run build`, `npm test`, or `npm run lint` scripts are defined; this repo has no runnable application code.
- No CI workflows live in this repo; the org-level `.github` repository supplies reusable workflows for other repos.
- No `schemas/`, `sdk/`, `examples/`, `sandbox/`, `scripts/`, or `tests/` directories exist at the root today; they are declared in `package.json` `files` as part of the intended future layout.

## When in doubt

- Start with `README.md` and `docs/index.md`.
- Treat `docs/aifp/01-AIFP-1-RFC-Payment-Protocol-Specification.md` as the authoritative standard.
- For repository organization questions, read `docs/aifp/15-Repository-Architecture.md`.
