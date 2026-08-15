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
| `scripts/` | `validate-openapi`, `validate-schemas`, `check-links`, `lint-markdown`, `build-docs`, `generate-pdfs`, `run-conformance` (planned). |
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
| Conformance check | `tests/...` |
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
| AIFP-1 protocol fee | `0.01` (1%, `100` bps) |
| AIFP-1 creator/referral fee | `0` (0 bps) |
| AIFP-1 merchant settlement rate | `0.99` (99%, before network/settlement costs) |
| AIFP-2/x402 AiFinPay protocol fee | `0` (0%, separate route profile) |
| Tier `standard` | from `$0.0005` |
| Tier `complex` | from `$0.002` |
| Tier `premium` | from `$0.005` |
| Receipt default TTL | 600 seconds |
| Idempotency dedupe window | 24 hours |
| Receipt signature | Ed25519 |
| Webhook signature | HMAC-SHA256 |
| Control-plane transport | TLS 1.3 |

`docs.yml` must reject superseded current-product markers such as
`$0.00001`, `$0.00006`, `$0.00010`, current-looking `100/1`, and a non-zero
creator/referral fee. Historical material may retain superseded values only when
it is explicitly labeled legacy or superseded.

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
- Receipt, JWKS, and webhook changes are security-sensitive and
  require security review.
- Do not weaken audience, resource, amount, expiry, or nonce
  validation in docs, OpenAPI, JSON Schemas, or SDKs.

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
- [ ] `gitleaks` (local or CI) is clean.
- [ ] PR template is filled out, including compatibility level.
- [ ] Affected canonical documents and cross-links are updated.
- [ ] No secrets, real `kid` values, or production material included.
- [ ] No PDF hand-edits, no `bun.lock` hand-edits, no legacy pricing
      markers reintroduced.
