#!/usr/bin/env python3
"""Fail CI when active AIFP-1 surfaces drift from canonical gross economics."""

from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]

CANONICAL_FILES = {
    "rfc": ROOT / "docs/aifp/01-AIFP-1-RFC-Payment-Protocol-Specification.md",
    "economics": ROOT / "docs/economics.md",
    "openapi": ROOT / "docs/aifp/08-OpenAPI-3.1-Specification.yaml",
    "schemas": ROOT / "docs/aifp/10-JSON-Schemas.md",
    "sdk": ROOT / "docs/aifp/11-SDK-Reference.md",
    "discovery": ROOT / ".well-known/aifinpay.json",
}

REQUIRED_SNIPPETS = {
    "rfc": [
        "gross-inclusive",
        "payer_total_amount  = gross_amount",
        "merchant_amount + protocol_fee_amount + creator_amount = gross_amount",
        "Fee-on-top settlement is not conformant",
    ],
    "economics": [
        "gross_amount = amount paid by the agent",
        "payer_settlement_amount = gross_amount",
        "merchant_amount = gross_amount - protocol_fee_amount",
        "Fee-on-top | **Not permitted for current AIFP-1 economics**",
    ],
    "openapi": [
        'gross_amount: "0.0005"',
        'payer_total_amount: "0.0005"',
        'merchant_amount: "0.000495"',
        'protocol_fee_amount: "0.000005"',
        'creator_amount: "0"',
    ],
    "schemas": [
        '"gross_amount": "0.0005"',
        '"payer_total_amount": "0.0005"',
        '"merchant_amount": "0.000495"',
        '"protocol_fee_amount": "0.000005"',
        '"creator_amount": "0"',
    ],
    "sdk": [
        '"grossAmount": "0.0005"',
        '"payerTotalAmount": "0.0005"',
        '"merchantAmount": "0.000495"',
        '"protocolFeeAmount": "0.000005"',
        '"creatorAmount": "0"',
    ],
}

FORBIDDEN_PATTERNS = [
    re.compile(r"[\"']?merchant_amount[\"']?\s*[:=]\s*[\"']0\.0005[\"']", re.IGNORECASE),
    re.compile(r"\bmerchantAmount\s*[:=]\s*[\"']0\.0005[\"']"),
    re.compile(r"reference merchant amount\s+(?:is|=)\s+\$?0\.0005", re.IGNORECASE),
]

SCAN_SUFFIXES = {".md", ".json", ".yaml", ".yml", ".ts", ".js", ".py", ".go"}
SCAN_DIRS = ["docs", "examples", "schemas", "sdk", "sandbox", "scripts", ".well-known"]

errors: list[str] = []

for name, path in CANONICAL_FILES.items():
    if not path.is_file():
        errors.append(f"missing canonical file: {path.relative_to(ROOT)}")
        continue
    text = path.read_text(encoding="utf-8-sig")
    for snippet in REQUIRED_SNIPPETS.get(name, []):
        if snippet not in text:
            errors.append(f"{path.relative_to(ROOT)} missing required economics marker: {snippet!r}")

try:
    discovery = json.loads(CANONICAL_FILES["discovery"].read_text(encoding="utf-8-sig"))
    economics = discovery["economics"]
    expected = {
        "settlement_semantics": "gross-inclusive",
        "reference_price_semantics": "gross-payer-amount",
        "merchant_share": "0.99",
        "protocol_fee_share": "0.01",
        "creator_share": "0",
        "treasury_bps": 100,
        "creator_bps": 0,
        "fee_on_top": False,
    }
    for key, value in expected.items():
        if economics.get(key) != value:
            errors.append(f".well-known/aifinpay.json economics.{key} must be {value!r}")
except Exception as exc:  # fail closed on malformed discovery metadata
    errors.append(f"cannot validate .well-known/aifinpay.json economics: {exc}")

for directory in SCAN_DIRS:
    base = ROOT / directory
    if not base.exists():
        continue
    for path in base.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in SCAN_SUFFIXES:
            continue
        text = path.read_text(encoding="utf-8-sig", errors="replace")
        for pattern in FORBIDDEN_PATTERNS:
            match = pattern.search(text)
            if match:
                errors.append(
                    f"{path.relative_to(ROOT)} contains a forbidden gross-as-merchant example: {match.group(0)!r}"
                )

if errors:
    print("AIFP-1 economics conformance FAILED:")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)

print("AIFP-1 economics conformance OK: gross payer price, 99/1/0 split, fee-on-top=false")
