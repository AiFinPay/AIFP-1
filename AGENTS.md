# AGENTS.md

Primary instructions are located at:

- node_modules/@daochild/agents-config/AGENTS.md

Follow all instructions from that file unless overridden below.

Operating instructions for AI coding agents working in the
`@aifinpay/protocol-aifp-1` repository (the AiFinPay Paywall Protocol, AIFP-1).

This file applies to the entire repository. Follow it alongside
`CONTRIBUTING.md`, `SECURITY.md`, `SUPPORT.md`, and `CODE_OF_CONDUCT.md`.

## What This Repository Is

- A payment protocol foundation, not a typical application codebase.
- Canonical protocol specification lives in `docs/aifp/` (Docs 01-15).
- Public developer portal lives in `docs/`.
- Machine-readable contracts: `docs/aifp/08-OpenAPI-3.1-Specification.yaml`
  and `docs/aifp/10-JSON-Schemas.md`.
- SDK design surface lives in `sdk/` (TypeScript, Python, Go).
- Examples live in `examples/`, sandbox flow in `sandbox/`, validation
  helpers in `scripts/`, and conformance work in `tests/`.

The README hero image and other branded assets live in `assets/`.
PDFs next to canonical Markdown files are generated artifacts; do not
hand-edit them.

## Package Layout

| Path | Purpose |
|---|---|
| `package.json` | Declares the npm package name `@aifinpay/protocol-aifp-1` and the `@daochild/agents-config` dev dependency. There is no application source in this root package; it is a meta-package. |
| `docs/aifp/01-...15-...` | Source of truth for protocol behavior. Treat as normative. |
| `docs/aifp/08-OpenAPI-3.1-Specification.yaml` | API contract, must match protocol docs. |
| `docs/aifp/10-JSON-Schemas.md` | Object shape contract, must match OpenAPI and protocol docs. |
| `docs/` | Human-readable portal, navigation, quick starts, role-based guides. |
| `sdk/typescript\|python\|go/` | SDK design surfaces. Reference implementations land under `sdk/`. |
| `examples/` | Runnable merchant, agent, wallet, webhook, receipt, and curl flows. |
| `sandbox/` | Local challenge, quote, pay, receipt, and webhook playground. |
| `schemas/` | Schema entry points. |
| `scripts/` | Validation and conformance helpers, including `check-economics.py`. |
| `tests/` | Conformance, schema, security, and documentation link tests. |
| `assets/` | Brand and diagram assets. |
| `.github/` | Issue templates, PR template, workflows, CODEOWNERS. |
| `.githooks/pre-push` | Local `gitleaks` secret scan before pushing. |

## Repository Map For Agents

If you are not sure where a change belongs:

| Change | Edit |
|---|---|
| Protocol meaning, error codes, receipt claims, quote/pay flow | `docs/aifp/01-AIFP-1-RFC-Payment-Protocol-Specification.md` (and matching `02-`/`03-`/`04-` documents) |
| API shape, endpoints, request/response schemas | `docs/aifp/08-OpenAPI-3.1-Specification.yaml` |
| Object shape contract | `docs/aifp/10-JSON-Schemas.md` |
| Portal copy, navigation, role guides | `docs/*.md` |
| SDK reference | `sdk/typescript\|python\|go/...` and `docs/aifp/11-SDK-Reference.md` |
| Runnable example | `examples/...` |
| Conformance check | `tests/...` and `scripts/check-economics.py` |
| Automation | `scripts/...` and `.github/workflows/...` |

When two surfaces disagree, the canonical spec (`docs/aifp/01-`) wins.
Open an AIP before changing normative protocol behavior.

## Build, Lint, Test

There is no compile step for the protocol documents themselves. Use
these local checks before opening a pull request:

| Check | Command |
|---|---|
| Markdown lint | `npx --yes markdownlint-cli2 "**/*.md" "!node_modules"` |
| OpenAPI lint | `npx --yes @redocly/cli lint docs/aifp/08-OpenAPI-3.1-Specification.yaml` |
| Economics conformance | `python scripts/check-economics.py` |
| Local Markdown link check | `python .github/workflows/link-check.yml` (run the embedded Python block from the workflow) |
| Secret scan (local) | `gitleaks protect --staged --verbose --redact --no-git` (requires `gitleaks`; the `.githooks/pre-push` hook wraps this) |
| Conformance | See `tests/README.md` (planned runner) |

CI runs the same checks via `.github/workflows/`:
`docs.yml`, `link-check.yml`, `markdown-lint.yml`, `openapi.yml`,
`schemas.yml`, `secret-scan.yml`, `release.yml`.

## Coding Conventions

- Match the existing voice: clear, precise, evidence-based, cross-linked.
- Prefer examples over abstract descriptions in documentation.
- Keep heading text stable; other documents and AIPs link to them.
- Do not add code comments unless the surrounding files already use
  comments as documentation.
- Match the style of neighboring files (Markdown, YAML, JSON, source).
- For TypeScript, Python, and Go SDKs, follow the language-specific
  README under `sdk/<language>/` once present.
- Do not introduce a native token, do not change pricing tiers or fee
  rates, and do not replace HTTP auth. See `ROADMAP.md` "Non-Goals".

## Pricing And Protocol Constants

Do not change these without an accepted AIP and a migration plan:

| Constant | Value |
|---|---|
| AIFP-1 reference-price semantics | **gross payer amount**; protocol fee is deducted from gross, never added on top |
| AIFP-1 protocol fee | `0.01` (1% of gross, `100` bps) |
| AIFP-1 creator/referral fee | `0` (0 bps) |
| AIFP-1 merchant settlement rate | `0.99` (99% of gross, before network/settlement costs) |
| AIFP-1 payer settlement amount | `1.00` of gross (`payer_total_amount = gross_amount`) |
| AIFP-2/x402 AiFinPay protocol fee | `0` (0%, separate route profile) |
| Tier `standard` gross price | from `$0.0005` |
| Tier `complex` gross price | from `$0.002` |
| Tier `premium` gross price | from `$0.005` |
| Receipt signature profile | Ed25519 / EdDSA under the current receipt design |
| Webhook signature profile | HMAC-SHA256 where the documented webhook profile is used |

The following are **profile/deployment parameters, not universal hard-coded protocol constants**:

| Parameter | Rule |
|---|---|
| Receipt TTL / expiry | Defined by the active receipt/profile; expiry validation is mandatory |
| Idempotency retention window | Must be sufficient for the implementation's retry/reconciliation model; no universal 24-hour constant is defined here |
| Control-plane TLS version/configuration | Use authenticated, confidential modern TLS appropriate to the active deployment/security policy; do not invent an unevidenced fixed version claim |

Current AIFP-1 amount conservation is normative:

```text
payer_total_amount = gross_amount
merchant_amount + protocol_fee_amount + creator_amount = gross_amount
protocol_fee_amount = 1% of gross under exact settlement base-unit arithmetic
creator_amount = 0
```

Never use the gross tier value as `merchant_amount`. Never implement or document the current AIFP-1 1% fee as an additional surcharge above the displayed/quoted action price.

Budget/policy rejection belongs **before signing/broadcasting**. A `/v1/pay` settlement-verification path must not deny the receipt for an otherwise valid settlement matching an already-issued payable quote solely because a budget threshold is discovered after payment.

`docs.yml` and `scripts/check-economics.py` must reject active economics drift, including gross-as-merchant examples. Historical material may retain superseded values only when it is explicitly labeled legacy or superseded.

## Pull Request Workflow

1. Read `CONTRIBUTING.md` and the relevant section of `docs/aifp/`.
2. Decide whether the change is documentation, example, SDK, schema,
   protocol behavior, or security-sensitive. Use the PR template.
3. Keep public protocol meaning stable unless the change is gated by
   an accepted AIP.
4. Update affected canonical documents in the same PR. Cross-link.
5. Run the local checks listed above.
6. Fill out `.github/PULL_REQUEST_TEMPLATE.md` completely. Mark the
   compatibility level: PATCH, MINOR, or MAJOR.
7. Do not commit secrets, API keys, real `kid` values, or production
   JWKS material. Use the `sandbox/` flow for test fixtures.
8. Do not force-push, skip hooks, or amend published commits unless
   the user explicitly asks for it.

## Security

- Vulnerabilities are reported privately to `security@aifinpay.io`
  per `SECURITY.md`. Never post them in issues, PRs, or chat.
- The `.githooks/pre-push` script runs `gitleaks` locally if
  installed; CI runs the same scan via `secret-scan.yml`.
- Receipt, JWKS, webhook, quote-economics, settlement-semantics, and
  post-payment lifecycle changes are security-sensitive and require review.
- Do not weaken audience, resource, gross amount, split, expiry, or replay/idempotency
  validation in docs, OpenAPI, JSON Schemas, or SDKs.
- Do not put AIFP-3 Agent Passport security semantics into AIFP-1 unless a cross-protocol integration explicitly requires them and cites the AIFP-3 source.

## Governance

- Protocol changes go through the AIP process
  (`docs/aifp/06-AIP-Improvement-Proposal-Process.md`).
- Code ownership is defined in `.github/CODEOWNERS`. Routing:
  - `/docs/aifp/` -> `@AiFinPay/protocol`
  - OpenAPI and JSON Schemas -> `@AiFinPay/api`
  - `/.github/` and `/SECURITY.md` -> `@AiFinPay/security` (for `SECURITY.md`) / `@AiFinPay/maintainers` (for `.github/`)
  - Everything else -> `@AiFinPay/maintainers`

## What Not To Do

- Do not edit generated PDFs in `docs/aifp/*.pdf`. Regenerate from
  Markdown via `docs/aifp/md2pdf.py`.
- Do not edit `bun.lock` by hand.
- Do not introduce a new top-level package manager, build tool, or
  framework without an AIP.
- Do not move normative spec text out of `docs/aifp/`.
- Do not remove or rename files under `docs/aifp/` without updating
  every cross-link in `README.md`, `docs/index.md`, and the portal
  navigation.
- Do not add emojis, marketing language, or unrelated "drive-by"
  formatting changes to canonical documents.

## Quick Sanity Check Before Committing

- [ ] Markdown renders and links resolve locally.
- [ ] `markdownlint-cli2` passes.
- [ ] `redocly lint` passes for the OpenAPI contract.
- [ ] `python scripts/check-economics.py` passes.
- [ ] `gitleaks` (local or CI) is clean.
- [ ] PR template is filled out, including compatibility level.
- [ ] Affected canonical documents and cross-links are updated.
- [ ] No secrets, real `kid` values, or production material included.
- [ ] No PDF hand-edits, no `bun.lock` hand-edits, no legacy pricing or fee-on-top semantics reintroduced.
