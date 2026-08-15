#!/usr/bin/env python3
"""Fail CI when AIFP-1 lifecycle drifts into payer-loss semantics."""

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]

RFC = ROOT / "docs/aifp/01-AIFP-1-RFC-Payment-Protocol-Specification.md"
OPENAPI = ROOT / "docs/aifp/08-OpenAPI-3.1-Specification.yaml"
AIP19 = ROOT / "aips/aip-0019.md"
SECURITY = ROOT / "SECURITY.md"
ERRORS = ROOT / "docs/reference/error-codes.md"

required = {
    RFC: [
        "Pre-payment policy cannot become a post-payment receipt veto",
        "Budget, policy, and quote expiry",
        "MUST NOT by itself be used to deny receipt",
        "reconcile/retry verification of the **same** settlement reference",
    ],
    AIP19: [
        "before an AIFP-1 payment is signed or broadcast",
        "MUST NOT be used by `POST /v1/pay`",
        "budget comparisons are against the **gross payer amount**",
    ],
    SECURITY: [
        "Pre-payment budget/policy checks",
        "must not be denied a receipt solely because a budget threshold is discovered after payment",
        "there is no universal 600-second protocol constant",
        "there is no universal 24-hour protocol constant",
    ],
    ERRORS: [
        "Budget Lifecycle Rule",
        "Quote Expiry Rule",
        "do not use wall-clock expiry alone to reject an already-valid in-window settlement",
    ],
}

errors: list[str] = []

for path, snippets in required.items():
    if not path.is_file():
        errors.append(f"missing lifecycle source: {path.relative_to(ROOT)}")
        continue
    text = path.read_text(encoding="utf-8-sig")
    for snippet in snippets:
        if snippet not in text:
            errors.append(f"{path.relative_to(ROOT)} missing lifecycle marker: {snippet!r}")

if OPENAPI.is_file():
    api = OPENAPI.read_text(encoding="utf-8-sig")
    quote_match = re.search(r"(?ms)^  /v1/quote:\n(.*?)(?=^  /v1/pay:)", api)
    pay_match = re.search(r"(?ms)^  /v1/pay:\n(.*?)(?=^  /v1/receipt/)", api)
    if not quote_match:
        errors.append("OpenAPI missing /v1/quote section")
    else:
        quote = quote_match.group(1)
        if "'403':" not in quote:
            errors.append("OpenAPI /v1/quote must expose pre-payment 403 budget/policy rejection")
        if "before\n        the payer signs or broadcasts" not in quote and "before\n        signing" not in quote:
            errors.append("OpenAPI /v1/quote must describe budget/policy rejection before signing/broadcast")
    if not pay_match:
        errors.append("OpenAPI missing /v1/pay section")
    else:
        pay = pay_match.group(1)
        if "'403':" in pay:
            errors.append("OpenAPI /v1/pay must not expose a generic budget/policy 403 post-payment veto")
        if "post-payment verification endpoint" not in pay:
            errors.append("OpenAPI /v1/pay must identify itself as post-payment verification")
        if "MUST NOT deny the corresponding receipt solely because a budget" not in pay:
            errors.append("OpenAPI /v1/pay missing post-payment budget safety rule")
        if "MUST NOT be evaluated solely from the later /v1/pay request" not in pay:
            errors.append("OpenAPI /v1/pay missing quote-expiry timing safety rule")
else:
    errors.append("missing OpenAPI lifecycle source")

# Prevent reintroduction of previously audited universal constants in agent/security policy.
for rel in ["AGENTS.md", "SECURITY.md"]:
    path = ROOT / rel
    if not path.is_file():
        continue
    text = path.read_text(encoding="utf-8-sig")
    forbidden = [
        r"Receipt default TTL\s*\|\s*600 seconds",
        r"Idempotency dedupe window\s*\|\s*24 hours",
        r"Control-plane transport\s*\|\s*TLS 1\.3",
    ]
    for pattern in forbidden:
        if re.search(pattern, text, flags=re.IGNORECASE):
            errors.append(f"{rel} reintroduced an unevidenced universal constant: {pattern}")

if errors:
    print("AIFP-1 lifecycle conformance FAILED:")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)

print("AIFP-1 lifecycle conformance OK: policy/expiry pre-payment, settlement verification post-payment")
