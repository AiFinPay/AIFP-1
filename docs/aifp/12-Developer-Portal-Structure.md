# AIFP Developer Portal Structure

**Document:** AIFP-DOC-12 · **Version:** 1.0.0 · **Governed by:** AIFP-1 (Doc 01)
**Reference quality bar:** Stripe Docs · Cloudflare Developers · Google Cloud · Kubernetes.

> This document specifies the information architecture, navigation, and feature set of
> the official AIFP developer portal at **`https://docs.aifinpay.io`**. All content maps
> to the canonical documents (01–15); the portal renders them — it is not a new source of
> truth.

---

## 1. Information Architecture

```text
docs.aifinpay.io
├── Home (value prop · "4-step loop" hero · quick links)
├── Get Started
│   ├── Quick Start (Doc 07)            ← 5-minute path
│   ├── Merchant Quick Start
│   ├── Agent Quick Start
│   └── Wallet Quick Start
├── Concepts
│   ├── HTTP 402 & the Payment Challenge (AIFP-1 §5–6)
│   ├── Receipts & Stateless Verification (AIFP-1 §7)
│   ├── Action Pricing & Fees (Standard · Complex · Premium · 1% protocol fee)
│   ├── Agent Passport, Reputation & Trust (AIFP-1 §24, §10.2; Doc 03 §9)
│   ├── Budgets & Idempotency
│   └── Settlement & Multi-chain (12 networks)
├── Guides
│   ├── Merchant Integration (Doc 02 · 15 frameworks)
│   ├── Building an Agent (Doc 03)
│   ├── x402 Migration
│   ├── Hybrid Fiat Settlement
│   └── Webhooks
├── API Reference
│   ├── API Explorer (live, OpenAPI 3.1 · Doc 08)
│   ├── Quote · Pay · Receipt · Verify
│   ├── Merchant · Wallet · Passport · Migration
│   ├── Errors (registry · AIFP-1 App. C)
│   └── JSON Schemas (Doc 10)
├── SDKs
│   ├── SDK Reference (Doc 11)
│   ├── TypeScript · Python · Go · Rust · Java · PHP · C#
│   └── Downloads & Versions
├── Tools
│   ├── Sandbox (test keys · faucet)
│   ├── Postman Collection (Doc 09)
│   ├── Receipt Inspector (paste a JWT → decoded claims + validity)
│   └── Code Samples / Recipes
├── Protocol
│   ├── AIFP-1 RFC (Doc 01)
│   ├── Whitepaper (Doc 05)
│   ├── AIP Process & Index (Doc 06)
│   ├── Security & Cryptography (Doc 04)
│   └── Ecosystem & Governance (Doc 14)
├── Resources
│   ├── Changelog
│   ├── Status / Uptime
│   ├── FAQ
│   ├── Branding (Doc 13)
│   └── GitHub / Repos (Doc 15)
└── Footer (Version Selector · Search · Language · Support)
```

---

## 2. Navigation

- **Primary nav (top):** Get Started · Guides · API Reference · SDKs · Protocol.
- **Persistent left sidebar:** section tree (collapsible, deep-linkable anchors).
- **Right "on this page" rail:** in-page heading outline for long docs.
- **Breadcrumbs:** `Docs / Section / Page`.
- **Role switcher (top-right):** *I am a…* **Merchant / Agent Developer / Wallet** — re-orders
  Get Started and surfaces the relevant Quick Start.

---

## 3. Search

- Full-text, typo-tolerant, instant (`/` to focus). Indexes all docs + API + SDK + AIPs.
- **Scoped facets:** Concepts · Guides · API · SDK · Errors. Searching an error code
  (e.g. `AIFP-422-SIGNATURE`) jumps straight to its registry entry.
- **AI answer box** (optional) grounded **only** in the canonical docs; every answer cites
  the source doc/section.

---

## 4. API Explorer

- Rendered from **`08-OpenAPI-3.1-Specification.yaml`** (single source).
- Try-it-out with a **sandbox** key prefilled (`sk_test_*`), never production by default.
- Per-operation: request schema, response schemas, examples, error table, and
  copy-paste snippets in all 7 SDK languages + cURL.
- "Run in Postman" button (links Doc 09 collection).

---

## 5. Code Samples & Recipes

Each recipe is runnable and language-tabbed (TS/Py/Go/Rust/Java/PHP/C#/cURL):
- Paywall an endpoint · Pay through a 402 · Verify a receipt · Set a budget ·
  Create an Agent Passport · Migrate from x402 · Handle async (`202`) settlement ·
  Webhook signature verification.

Samples are **lint-checked in CI against the OpenAPI + JSON Schemas** so they cannot drift.

---

## 6. Authentication (portal-side)

- **Dashboard sign-in** (separate from docs) at `dashboard.aifinpay.io` for keys.
- Docs show keys via a **placeholder** (`sk_test_REPLACE_ME`); signed-in users may inject
  their **sandbox** key into the API Explorer for that session only (never persisted in
  shareable URLs).
- Two key planes documented everywhere: **API key** (`Authorization: Bearer`) +
  **Agent Passport** signature (AIFP-1 §10).

---

## 7. SDK Downloads

| Language | Package | Badge |
|---|---|---|
| TypeScript | `@aifinpay/agent`, `@aifinpay/merchant` | npm version |
| Python | `aifinpay-agent`, `aifinpay-merchant` | PyPI |
| Go | `github.com/aifinpay/aifp-go` | pkg.go.dev |
| Rust | `aifinpay` | crates.io |
| Java | `io.aifinpay:aifp` | Maven Central |
| PHP | `aifinpay/aifp` | Packagist |
| C# | `AiFinPay` | NuGet |

Each card links source repo (Doc 15), changelog, and the SDK Reference (Doc 11) section.

---

## 8. Sandbox

- Base URL `https://sandbox.api.aifinpay.io`, test keys, and hosted sandbox test-token tooling.
- Simulated settlement; test `kid` JWKS. One-click "reset sandbox" and "seed merchant +
  agent + wallet" fixtures.

---

## 9. Changelog & Versioning

- **Version selector** (top-right) switches the whole portal between protocol MAJOR/MINOR
  versions; deep links preserve the version.
- Changelog entries link the **AIP** (Doc 06) that introduced the change and tag
  `breaking | feature | fix` per SemVer (Doc 06 §5).

---

## 10. FAQ (seed set)

- *Does AIFP have a token?* No — tokenless by design (Whitepaper §14).
- *Do I call AiFinPay to verify a receipt?* No — verification is local/stateless (§7.4).
- *Which chains/assets?* 12 networks; USDC/USDT/PYUSD (Doc 01 App. B).
- *How do micropayments work?* Agent actions are priced by tier: Standard from $0.00001, Complex from $0.00006, Premium from $0.00010.
- *What is the protocol fee?* AiFinPay charges 1% on successful transactions; 99% settles to the merchant, excluding applicable network or settlement costs.
- *Is it x402-compatible?* Yes. Migration incentives, if any, are published through the official developer portal.

---

## 11. Portal Tech & Quality Bar

- Static-site generator (docs-as-code; Markdown in the repo → portal). Content lives in
  `aifinpay/docs` (Doc 15); PRs preview-deploy.
- A11y AA, dark/light, mobile-first, sub-1s search, copy buttons on every code block,
  permalink anchors, and "Edit this page on GitHub" on every doc.
- **Single source of truth:** the portal builds from Docs 01–15 + the OpenAPI/Schema/
  Postman artifacts. No content is authored only in the portal.
