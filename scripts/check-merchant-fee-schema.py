#!/usr/bin/env python3
"""Validate the draft envelope; this is not quote authorization or settlement proof."""
import copy
import json
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / "schemas/merchant-fee-profile-v1.schema.json").read_text())
VECTORS = json.loads((ROOT / "tests/merchant-fee-profile-v1-vectors.json").read_text())
VALIDATOR = Draft202012Validator(SCHEMA)


def envelope(case):
    return {
        "profile": "AIFP1-MERCHANT-FEE-V1",
        "merchant_id": "fixture-merchant",
        "fee_profile_id": "fixture-profile",
        "fee_profile_revision": 1,
        "treasury_bps": case["bps"],
        "creator_bps": 0,
        "gross_atomic": case["gross"],
        "merchant_atomic": case["merchant"],
        "protocol_fee_atomic": case["fee"],
        "creator_atomic": "0",
        "payer_total_atomic": case["gross"],
        "chain": "eip155:84532",
        "asset": "fixture-usdc",
        "asset_decimals": 6,
        "treasury_destination": "fixture-corporate-treasury",
    }


class MerchantFeeSchemaTests(unittest.TestCase):
    def assert_rejected(self, instance):
        self.assertTrue(list(VALIDATOR.iter_errors(instance)), repr(instance))

    def changed(self, field, value):
        instance = envelope(VECTORS["valid"][0])
        instance[field] = value
        return instance

    def test_schema_is_valid_draft_2020_12(self):
        self.assertEqual(SCHEMA["$schema"], "https://json-schema.org/draft/2020-12/schema")
        Draft202012Validator.check_schema(SCHEMA)

    def test_every_published_valid_arithmetic_vector_has_a_valid_envelope(self):
        self.assertGreater(len(VECTORS["valid"]), 0)
        for case in VECTORS["valid"]:
            with self.subTest(case=case):
                VALIDATOR.validate(envelope(case))

    def test_each_required_binding_is_required(self):
        required = {
            "profile", "merchant_id", "fee_profile_id", "fee_profile_revision",
            "treasury_bps", "creator_bps", "gross_atomic", "merchant_atomic",
            "protocol_fee_atomic", "creator_atomic", "payer_total_atomic",
            "chain", "asset", "asset_decimals", "treasury_destination",
        }
        self.assertEqual(set(SCHEMA["required"]), required)
        for field in required:
            with self.subTest(field=field):
                instance = envelope(VECTORS["valid"][0])
                del instance[field]
                self.assert_rejected(instance)

    def test_unknown_profiles_and_properties_are_rejected(self):
        for profile in ["AIFP-2", "AIFP1-MERCHANT-FEE-V2", "", None]:
            with self.subTest(profile=profile):
                self.assert_rejected(self.changed("profile", profile))
        self.assert_rejected(self.changed("caller_fee_override", 500))

    def test_rate_revision_and_decimals_bounds(self):
        invalid = {
            "treasury_bps": [99, 501, 250.5, "100", True, None],
            "fee_profile_revision": [0, -1, 1.5, "1", True, None],
            "asset_decimals": [-1, 37, 6.5, "6", True, None],
            "creator_bps": [1, -1, "0", None],
        }
        for field, values in invalid.items():
            for value in values:
                with self.subTest(field=field, value=value):
                    self.assert_rejected(self.changed(field, value))

    def test_atomic_amount_strings_are_canonical(self):
        fields = ["gross_atomic", "merchant_atomic", "protocol_fee_atomic",
                  "creator_atomic", "payer_total_atomic"]
        for field in fields:
            for value in ["-1", "+1", "1.0", "1e3", "01", "", " 1", 1, True, None]:
                with self.subTest(field=field, value=value):
                    self.assert_rejected(self.changed(field, value))
        self.assert_rejected(self.changed("gross_atomic", "0"))
        self.assert_rejected(self.changed("creator_atomic", "1"))

    def test_binding_references_are_nonempty_strings(self):
        for field in ["merchant_id", "fee_profile_id", "chain", "asset",
                      "treasury_destination"]:
            for value in ["", None, 1, [], {}]:
                with self.subTest(field=field, value=value):
                    self.assert_rejected(self.changed(field, value))

    def test_schema_does_not_claim_cross_field_authorization(self):
        instance = copy.deepcopy(envelope(VECTORS["valid"][0]))
        instance["merchant_atomic"] = "1"
        VALIDATOR.validate(instance)
        self.assertNotEqual(
            int(instance["gross_atomic"]),
            int(instance["merchant_atomic"]) + int(instance["protocol_fee_atomic"]),
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
