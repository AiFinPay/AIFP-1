#!/usr/bin/env python3
"""Candidate fee profile vectors; does not activate or validate live settlement."""
import json
import re
from pathlib import Path

def split(gross, bps):
    if type(bps) is not int or not 100 <= bps <= 500:
        raise ValueError("RATE")
    if not isinstance(gross, str) or not re.fullmatch(r"[1-9][0-9]*", gross):
        raise ValueError("AMOUNT")
    total = int(gross)
    fee = total * bps // 10_000
    if fee == 0:
        raise ValueError("ZERO_FEE")
    return str(fee), str(total - fee)

vectors = json.loads((Path(__file__).resolve().parents[1] / "tests/merchant-fee-profile-v1-vectors.json").read_text())
for case in vectors["valid"]:
    fee, merchant = split(case["gross"], case["bps"])
    assert (fee, merchant) == (case["fee"], case["merchant"]), case
    assert int(fee) + int(merchant) == int(case["gross"])
for case in vectors["invalid"]:
    try:
        split(case["gross"], case["bps"])
    except ValueError as exc:
        assert str(exc) == case["error"], case
    else:
        raise AssertionError(case)
print("Candidate merchant fee vectors passed:", len(vectors["valid"]) + len(vectors["invalid"]))
