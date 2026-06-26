#!/usr/bin/env python3
"""Sanity checks for scripts/digit_stride_experiment.py."""
from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "digit_stride_experiment.py"

spec = importlib.util.spec_from_file_location("digit_stride_experiment", SCRIPT)
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
assert spec.loader is not None
spec.loader.exec_module(module)


class DigitStrideExperimentTests(unittest.TestCase):
    def test_self_check(self) -> None:
        result = module.self_check()
        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["bridge_rows_checked"], [13, 89, 233])

    def test_w13_positions_are_base_agnostic_bridge_positions(self) -> None:
        self.assertEqual(module.row_positions(13), [13 * k for k in range(1, 14)])
        self.assertEqual(module.row_positions(13)[-1], 169)

    def test_fibonacci_prime_bridge_membership(self) -> None:
        fibs = set(module.fibonacci_up_to(300))
        primes = set(module.primes_up_to(300))
        bridges = sorted(n for n in fibs & primes if n > 5)
        self.assertEqual(bridges[:3], [13, 89, 233])
        self.assertEqual(module.classify_n(13, fibs, primes), "bridge")
        self.assertEqual(module.classify_n(8, fibs, primes), "fib_only")
        self.assertEqual(module.classify_n(7, fibs, primes), "prime_only")

    def test_distinct_prime_rows_are_disjoint_in_the_test_range(self) -> None:
        prime_rows = [7, 11, 13, 17, 19]
        for i, p in enumerate(prime_rows):
            for q in prime_rows[i + 1 :]:
                self.assertTrue(set(module.row_positions(p)).isdisjoint(module.row_positions(q)))

    def test_known_w13_words_in_base10(self) -> None:
        pi_digits = module.digits_for_source("pi", 10, 169, 40)
        phi_digits = module.digits_for_source("phi", 10, 169, 40)
        self.assertEqual(module.encode_word(module.word_digits_from_stream(pi_digits, 13)), "7878083465579")
        self.assertEqual(module.encode_word(module.word_digits_from_stream(phi_digits, 13)), "8308021512849")


if __name__ == "__main__":
    unittest.main()
