#!/usr/bin/env python3
"""Digit-stride parser experiments for constants, bases, and selector sets.

For a source number x, base b, and stride n, the row W_{n,b}(x) is
formed by landing on digit positions n, 2n, ..., n^2 after the radix point.
The same code treats Fibonacci-only rows, prime-only rows, and bridge rows
(n that are both Fibonacci and prime) as separate experimental regions.

This module intentionally uses only Python's standard library.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from collections import Counter, defaultdict
from dataclasses import dataclass
from decimal import Decimal, localcontext
from pathlib import Path
from typing import Iterable, Sequence

DIGIT_ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
DEFAULT_SOURCES = ("pi", "phi")
DEFAULT_BASES = (2, 3, 5, 7, 10, 11, 13, 16)
DEFAULT_MODULI = (360, 2880, 359)


@dataclass(frozen=True)
class ExperimentRow:
    source: str
    base: int
    n: int
    membership: str
    word: str
    word_sha256: str
    length: int
    final_position: int
    digit_entropy_norm: float
    digit_phase_R: float
    transition_coherence: float
    residues: dict[int, int]


def parse_int_list(raw: str | None, default: Sequence[int]) -> list[int]:
    if raw is None or raw.strip() == "":
        return list(default)
    return [int(x.strip()) for x in raw.split(",") if x.strip()]


def parse_str_list(raw: str | None, default: Sequence[str]) -> list[str]:
    if raw is None or raw.strip() == "":
        return list(default)
    return [x.strip().lower() for x in raw.split(",") if x.strip()]


def primes_up_to(n: int) -> list[int]:
    if n < 2:
        return []
    sieve = bytearray(b"\x01") * (n + 1)
    sieve[0:2] = b"\x00\x00"
    for p in range(2, int(n**0.5) + 1):
        if sieve[p]:
            start = p * p
            sieve[start : n + 1 : p] = b"\x00" * (((n - start) // p) + 1)
    return [i for i, flag in enumerate(sieve) if flag]


def fibonacci_up_to(n: int) -> list[int]:
    vals: list[int] = []
    a, b = 1, 1
    while a <= n:
        if not vals or vals[-1] != a:
            vals.append(a)
        a, b = b, a + b
    return vals


def classify_n(n: int, fibs: set[int], primes: set[int]) -> str:
    in_fib = n in fibs
    in_prime = n in primes
    if in_fib and in_prime:
        return "bridge"
    if in_fib:
        return "fib_only"
    if in_prime:
        return "prime_only"
    return "neither"


def row_positions(n: int) -> list[int]:
    """One-indexed fractional digit positions for W_n."""
    if n <= 0:
        raise ValueError("n must be positive")
    return [k * n for k in range(1, n + 1)]


def pi_chudnovsky(precision: int) -> Decimal:
    """Return pi to roughly `precision` decimal digits using Chudnovsky."""
    with localcontext() as ctx:
        ctx.prec = precision + 20
        C = Decimal(426880) * Decimal(10005).sqrt()
        M = 1
        L = 13591409
        X = 1
        K = 6
        S = Decimal(L)
        terms = precision // 14 + 3
        for i in range(1, terms):
            M = (M * (K**3 - 16 * K)) // (i**3)
            L += 545140134
            X *= -262537412640768000
            S += Decimal(M * L) / Decimal(X)
            K += 12
        return +C / S


def constant_decimal(name: str, precision: int) -> Decimal:
    name = name.lower()
    with localcontext() as ctx:
        ctx.prec = precision + 20
        if name == "pi":
            return +pi_chudnovsky(precision + 10)
        if name == "phi":
            return +(Decimal(1) + Decimal(5).sqrt()) / Decimal(2)
        if name == "e":
            return +Decimal(1).exp()
        if name in ("sqrt2", "sqrt_2"):
            return +Decimal(2).sqrt()
    raise ValueError(f"Unsupported source constant: {name!r}")


def required_decimal_precision(max_position: int, base: int, guard_digits: int) -> int:
    if base < 2 or base > len(DIGIT_ALPHABET):
        raise ValueError(f"base must be in [2,{len(DIGIT_ALPHABET)}]")
    return int(math.ceil((max_position + guard_digits) * math.log10(base))) + guard_digits


def fractional_digits(value: Decimal, base: int, count: int, precision: int | None = None) -> list[int]:
    if count < 0:
        raise ValueError("count must be non-negative")
    if base < 2 or base > len(DIGIT_ALPHABET):
        raise ValueError(f"base must be in [2,{len(DIGIT_ALPHABET)}]")

    def _extract() -> list[int]:
        whole = int(value)
        frac = value - Decimal(whole)
        out: list[int] = []
        b = Decimal(base)
        for _ in range(count):
            frac *= b
            digit = int(frac)
            # Decimal guard against rare rounding spillover.
            if digit >= base:
                digit = base - 1
            out.append(digit)
            frac -= Decimal(digit)
        return out

    if precision is None:
        return _extract()
    with localcontext() as ctx:
        ctx.prec = precision
        return _extract()


def digits_for_source(source: str, base: int, max_position: int, guard_digits: int) -> list[int]:
    precision = required_decimal_precision(max_position, base, guard_digits)
    value = constant_decimal(source, precision)
    return fractional_digits(value, base, max_position, precision + guard_digits + 20)


def word_digits_from_stream(digits: Sequence[int], n: int) -> list[int]:
    positions = row_positions(n)
    if positions[-1] > len(digits):
        raise ValueError(f"need at least {positions[-1]} digits, got {len(digits)}")
    return [digits[pos - 1] for pos in positions]


def encode_word(word_digits: Sequence[int]) -> str:
    return "".join(DIGIT_ALPHABET[d] for d in word_digits)


def residues_for_word(word_digits: Sequence[int], base: int, moduli: Sequence[int]) -> dict[int, int]:
    residues = {m: 0 for m in moduli}
    for d in word_digits:
        for m in moduli:
            residues[m] = (base * residues[m] + d) % m
    return residues


def normalized_entropy(word_digits: Sequence[int], base: int) -> float:
    if not word_digits:
        return 0.0
    counts = Counter(word_digits)
    h = 0.0
    n = len(word_digits)
    for c in counts.values():
        p = c / n
        h -= p * math.log(p)
    return h / math.log(base) if base > 1 else 0.0


def digit_phase_R(word_digits: Sequence[int], base: int) -> float:
    if not word_digits:
        return 0.0
    sx = 0.0
    sy = 0.0
    for d in word_digits:
        angle = 2.0 * math.pi * d / base
        sx += math.cos(angle)
        sy += math.sin(angle)
    return math.hypot(sx, sy) / len(word_digits)


def transition_coherence(word_digits: Sequence[int], base: int) -> float:
    if len(word_digits) < 2:
        return 0.0
    sx = 0.0
    sy = 0.0
    for a, b in zip(word_digits, word_digits[1:]):
        angle = 2.0 * math.pi * ((b - a) % base) / base
        sx += math.cos(angle)
        sy += math.sin(angle)
    return math.hypot(sx, sy) / (len(word_digits) - 1)


def make_row(
    source: str,
    base: int,
    n: int,
    membership: str,
    digits: Sequence[int],
    moduli: Sequence[int],
) -> ExperimentRow:
    wdigits = word_digits_from_stream(digits, n)
    word = encode_word(wdigits)
    return ExperimentRow(
        source=source,
        base=base,
        n=n,
        membership=membership,
        word=word,
        word_sha256=hashlib.sha256(word.encode("utf-8")).hexdigest(),
        length=n,
        final_position=n * n,
        digit_entropy_norm=normalized_entropy(wdigits, base),
        digit_phase_R=digit_phase_R(wdigits, base),
        transition_coherence=transition_coherence(wdigits, base),
        residues=residues_for_word(wdigits, base, moduli),
    )


def row_to_dict(row: ExperimentRow, moduli: Sequence[int], word_limit: int) -> dict[str, str | int | float]:
    d: dict[str, str | int | float] = {
        "source": row.source,
        "base": row.base,
        "n": row.n,
        "membership": row.membership,
        "length": row.length,
        "final_position": row.final_position,
        "digit_entropy_norm": round(row.digit_entropy_norm, 12),
        "digit_phase_R": round(row.digit_phase_R, 12),
        "transition_coherence": round(row.transition_coherence, 12),
        "word_sha256": row.word_sha256,
    }
    if word_limit < 0 or len(row.word) <= word_limit:
        d["word"] = row.word
    else:
        d["word"] = row.word[:word_limit] + "..."
    for m in moduli:
        d[f"residue_mod_{m}"] = row.residues[m]
    return d


def compare_rows(rows: Sequence[ExperimentRow]) -> list[dict[str, str | int | float]]:
    """Compare source pairs within the same base and n."""
    by_key: dict[tuple[int, int], list[ExperimentRow]] = defaultdict(list)
    for row in rows:
        by_key[(row.base, row.n)].append(row)

    comparisons: list[dict[str, str | int | float]] = []
    for (base, n), group in sorted(by_key.items()):
        group = sorted(group, key=lambda r: r.source)
        for i in range(len(group)):
            for j in range(i + 1, len(group)):
                a = group[i]
                b = group[j]
                if len(a.word) != len(b.word):
                    continue
                matches = sum(1 for x, y in zip(a.word, b.word) if x == y)
                comparisons.append(
                    {
                        "base": base,
                        "n": n,
                        "membership": a.membership,
                        "source_a": a.source,
                        "source_b": b.source,
                        "length": len(a.word),
                        "exact_matches": matches,
                        "match_rate": round(matches / len(a.word), 12) if a.word else 0.0,
                    }
                )
    return comparisons


def summarize(rows: Sequence[ExperimentRow], moduli: Sequence[int]) -> dict:
    by_membership: dict[str, list[ExperimentRow]] = defaultdict(list)
    for r in rows:
        by_membership[r.membership].append(r)
    summary = {
        "row_count": len(rows),
        "memberships": {},
        "moduli": list(moduli),
    }
    for membership, group in sorted(by_membership.items()):
        summary["memberships"][membership] = {
            "rows": len(group),
            "n_values": sorted({r.n for r in group}),
            "mean_entropy_norm": sum(r.digit_entropy_norm for r in group) / len(group),
            "mean_digit_phase_R": sum(r.digit_phase_R for r in group) / len(group),
            "mean_transition_coherence": sum(r.transition_coherence for r in group) / len(group),
        }
    return summary


def run_experiment(
    sources: Sequence[str],
    bases: Sequence[int],
    max_n: int,
    min_n: int,
    moduli: Sequence[int],
    guard_digits: int,
) -> list[ExperimentRow]:
    fibs = {x for x in fibonacci_up_to(max_n) if x > min_n}
    primes = {x for x in primes_up_to(max_n) if x > min_n}
    n_values = sorted(fibs | primes)
    if not n_values:
        return []
    max_position = max(n * n for n in n_values)

    rows: list[ExperimentRow] = []
    for source in sources:
        for base in bases:
            digits = digits_for_source(source, base, max_position, guard_digits)
            for n in n_values:
                membership = classify_n(n, fibs, primes)
                rows.append(make_row(source, base, n, membership, digits, moduli))
    return rows


def write_csv(path: Path, rows: Iterable[dict]) -> None:
    rows = list(rows)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("")
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def self_check() -> dict:
    fibs = set(fibonacci_up_to(300))
    primes = set(primes_up_to(300))
    bridges = sorted(n for n in fibs & primes if n > 5)
    assert bridges[:3] == [13, 89, 233]
    assert row_positions(13) == [13 * k for k in range(1, 14)]
    assert row_positions(13)[-1] == 169

    for p in [7, 11, 13, 17, 19]:
        for q in [7, 11, 13, 17, 19]:
            if p < q:
                assert set(row_positions(p)).isdisjoint(row_positions(q))

    pi_digits = digits_for_source("pi", 10, 169, 40)
    phi_digits = digits_for_source("phi", 10, 169, 40)
    assert encode_word(word_digits_from_stream(pi_digits, 13)) == "7878083465579"
    assert encode_word(word_digits_from_stream(phi_digits, 13)) == "8308021512849"

    # Base changes the observed word, not the bridge membership or positions.
    pi_base2 = encode_word(word_digits_from_stream(digits_for_source("pi", 2, 169, 80), 13))
    assert pi_base2 == "1000001100001"

    return {
        "status": "ok",
        "bridge_rows_checked": bridges[:3],
        "w13_pi_base10": "7878083465579",
        "w13_phi_base10": "8308021512849",
        "w13_pi_base2": pi_base2,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run digit-stride parser experiments.")
    parser.add_argument("--sources", default=",".join(DEFAULT_SOURCES), help="comma list: pi,phi,e,sqrt2")
    parser.add_argument("--bases", default=",".join(str(x) for x in DEFAULT_BASES), help="comma list of bases 2..36")
    parser.add_argument("--max-n", type=int, default=89, help="largest n from Fibonacci/prime selectors")
    parser.add_argument("--min-n", type=int, default=5, help="exclude selector values <= this")
    parser.add_argument("--moduli", default=",".join(str(x) for x in DEFAULT_MODULI), help="comma list of projection moduli")
    parser.add_argument("--guard-digits", type=int, default=80, help="extra decimal precision guard")
    parser.add_argument("--out-dir", default="data/digit_stride", help="output directory")
    parser.add_argument("--word-limit", type=int, default=512, help="truncate word in CSV; -1 writes full words")
    parser.add_argument("--self-check", action="store_true", help="run deterministic sanity checks and exit")
    args = parser.parse_args()

    if args.self_check:
        print(json.dumps(self_check(), indent=2))
        return

    sources = parse_str_list(args.sources, DEFAULT_SOURCES)
    bases = parse_int_list(args.bases, DEFAULT_BASES)
    moduli = parse_int_list(args.moduli, DEFAULT_MODULI)

    rows = run_experiment(
        sources=sources,
        bases=bases,
        max_n=args.max_n,
        min_n=args.min_n,
        moduli=moduli,
        guard_digits=args.guard_digits,
    )

    out_dir = Path(args.out_dir)
    write_csv(out_dir / "rows.csv", [row_to_dict(r, moduli, args.word_limit) for r in rows])
    write_csv(out_dir / "source_comparisons.csv", compare_rows(rows))

    metadata = {
        "definition": "W_{n,b}(x) = digits at one-indexed fractional positions n,2n,...,n^2 in base b",
        "sources": sources,
        "bases": bases,
        "max_n": args.max_n,
        "min_n": args.min_n,
        "moduli": moduli,
        "guard_digits": args.guard_digits,
        "summary": summarize(rows, moduli),
        "self_check": self_check(),
    }
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "manifest.json").write_text(json.dumps(metadata, indent=2))
    print(json.dumps({"out_dir": str(out_dir), "row_count": len(rows)}, indent=2))


if __name__ == "__main__":
    main()
