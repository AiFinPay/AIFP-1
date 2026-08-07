# AIFP Branding & Style Guidelines

**Document:** AIFP-DOC-13 · **Version:** 1.0.0 · **Governed by:** AIFP-1 (Doc 01)

> These guidelines govern the visual and editorial identity of **AiFinPay** and the
> **AiFinPay Paywall Protocol (AIFP)** across docs, code, packages, and the developer
> portal. The aesthetic is **enterprise-grade, infrastructure-first, technical but
> clean** — Stripe / Ramp / Anthropic vibe, not crypto manifesto.

---

## 1. Naming Convention (normative)

| Use | Correct | Incorrect |
|---|---|---|
| Company | **AiFinPay** | AIFinPay, Aifinpay, AI FinPay |
| Protocol (full) | **AiFinPay Paywall Protocol** | AI Paywall Protocol |
| Protocol (abbr) | **AIFP** | aifp (in prose), AiFP |
| Spec | **AIFP-1** | AIFP1, AIFP 1.0 (use "AIFP-1 v1.0.0") |
| Proposal | **AIP** (AiFinPay Improvement Proposal) | EIP, AIFP-IP |

**Rules:** "AIFP" is always uppercase in prose. The first mention in any document SHOULD
expand to "AiFinPay Paywall Protocol (AIFP)". Never refer to AIFP as a token or coin —
**AIFP is tokenless**.

---

## 2. Logo Usage

- **Primary mark:** the AiFinPay globe/network glyph + "AiFinPay" wordmark.
- **Clear space:** ≥ the height of the "A" in the wordmark on all sides.
- **Minimum size:** 24px height (digital), 12mm (print).
- **Variants:** full-color on light, full-color on dark, monochrome (black), reverse
  (white). Use the highest-contrast variant for the background.
- **Don'ts:** don't recolor, stretch, rotate, add effects/shadows, place on busy imagery,
  or recreate the wordmark in a different typeface.

---

## 3. Color Palette

| Token | Hex | Use |
|---|---|---|
| **Primary Blue** | `#2F5FD6` | Brand accent, links, primary buttons, code highlights |
| Royal Blue (alt) | `#2563EB` | Diagrams, gradients, secondary accent |
| Ink (near-black) | `#0B1020` | Headlines, body on light |
| Slate | `#475569` | Secondary text |
| Mist | `#F4F6FB` | Surfaces / cards on light |
| Border | `#E2E8F0` | Hairlines, dividers, card borders |
| Surface Dark | `#0E1424` | Dark-mode background |
| Success | `#16A34A` | "Live / Done" states |
| Warning | `#D97706` | Caution, deprecations |
| Danger | `#DC2626` | Errors (`AIFP-4xx/5xx`) |

**Usage rule:** one dominant accent (Primary Blue). Avoid rainbow palettes. Status colors
only for status.

---

## 4. Typography

| Role | Family | Notes |
|---|---|---|
| Headlines | Inter / Helvetica Neue | Tight tracking; uppercase for section labels |
| Body | Inter / system-ui | 16px base, 1.6 line-height |
| Mono / code | JetBrains Mono / SF Mono | Code, IDs (`rcpt_*`), endpoints |

**Hierarchy:** H1 bold ink; H2 with a left **Primary Blue** bar; uppercase blue labels for
eyebrows; generous whitespace; no center-justified body text.

---

## 5. Iconography

- Line icons, 1.5–2px stroke, rounded joins, `currentColor` (Lucide / Heroicons style).
- **No emoji in normative docs, decks, or diagrams** — use inline SVG icons instead
  (lesson from the Casper deck: emoji render as tofu in headless rendering).
- Icon sizing relative to text (`width: 1em`) so they inherit color and scale.

---

## 6. Code Style (across SDKs & samples)

- **Indent:** 2 spaces (JS/TS/JSON/YAML), 4 spaces (Python), gofmt (Go), rustfmt (Rust).
- **Quotes:** double in JSON; language-idiomatic elsewhere.
- **IDs in examples:** always the canonical prefixes — `mrch_`, `agt_`, `wlt_`, `qt_`,
  `rcpt_`, `pp_` — and the same sample values across docs (`mrch_9f3a1c2b`, `wlt_3a1b`,
  `qt_8d21f0`, `rcpt_7b3e9f21`, `agt_4f9a2c7e`).
- **Amounts:** decimal **strings** in USD (`"0.0005"`), never floats.
- **Lint:** every code sample must pass CI checks against OpenAPI (Doc 08) + JSON Schemas
  (Doc 10).

---

## 7. Documentation Style

- **Voice:** precise, calm, infrastructure-grade. Active voice. Short sentences.
- **Normative language:** RFC 2119 keywords (MUST / SHOULD / MAY) only in normative docs
  (01, 04, 06).
- **Terminology:** use the canonical glossary (AIFP-1 Appendix A); never invent synonyms
  (it's a "receipt", not a "token receipt" or "payment proof token").
- **Numbers/invariants:** pricing, fees, TTLs, and network counts must match the canonical
  values everywhere (see Synchronization, Doc README).
- **No marketing fluff in reference docs.** Sell in the Whitepaper (05); explain in the rest.

---

## 8. Repository Naming

- Org: `github.com/aifinpay`.
- Pattern: `aifp-<area>` for protocol artifacts, `<lang>` clarity for SDKs.
- Examples: `aifp` (RFC/spec), `aifp-go`, `aifinpay-python`, `merchant-js`, `agent-js`,
  `docs`, `examples`, `openapi`, `schemas`, `conformance`. Full map in Doc 15.

---

## 9. Package Naming

| Ecosystem | Pattern | Example |
|---|---|---|
| npm | `@aifinpay/<pkg>` | `@aifinpay/agent`, `@aifinpay/merchant` |
| PyPI | `aifinpay-<pkg>` | `aifinpay-agent` |
| Go | `github.com/aifinpay/aifp-go` | module path |
| crates.io | `aifinpay` | crate |
| Maven | `io.aifinpay:aifp` | group:artifact |
| Packagist | `aifinpay/aifp` | vendor/package |
| NuGet | `AiFinPay` | package id |

---

## 10. Versioning Rules

- **SemVer** `MAJOR.MINOR.PATCH` for the protocol, SDKs, and schemas (see Doc 06 §5).
- Docs are versioned with the protocol MAJOR.MINOR; the portal exposes a version selector.
- Receipt `kid` is date-stamped (`aifp-2026-06`) and rotated; old `kid`s remain
  resolvable for receipt TTL windows.
- Breaking changes require an AIP, a deprecation window, and ≥12 months of previous-MAJOR
  support.
