#!/usr/bin/env python3
"""Build Target A/B/C datasets for EML prime experiments.

Outputs CSV files with columns: x,y,split plus target-specific fields.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
from typing import Iterable


def primes_up_to(n: int) -> list[int]:
    if n < 2:
        return []
    sieve = bytearray(b"\x01") * (n + 1)
    sieve[0:2] = b"\x00\x00"
    for p in range(2, int(n**0.5) + 1):
        if sieve[p]:
            step = p
            start = p * p
            sieve[start : n + 1 : step] = b"\x00" * (((n - start) // step) + 1)
    return [i for i, is_p in enumerate(sieve) if is_p]


def split_label(i: int, n: int) -> str:
    frac = i / max(1, n - 1)
    if frac < 0.7:
        return "train"
    if frac < 0.85:
        return "val"
    return "test"


def log_grid(max_x: int, points: int) -> list[int]:
    vals = sorted(
        {
            max(2, int(round(10 ** (math.log10(2) + t * (math.log10(max_x) - math.log10(2))))))
            for t in [i / max(1, points - 1) for i in range(points)]
        }
    )
    return [v for v in vals if v <= max_x]


def write_csv(path: Path, rows: Iterable[dict], fieldnames: list[str]) -> None:
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow(r)


def target_a_rows(primes: list[int], x_samples: list[int]) -> list[dict]:
    rows = []
    count = 0
    j = 0
    for i, x in enumerate(x_samples):
        while j < len(primes) and primes[j] <= x:
            count += 1
            j += 1
        approx = x / math.log(x)
        y = count / approx if approx > 0 else 0.0
        rows.append({"x": x, "pi_x": count, "y": y, "split": split_label(i, len(x_samples))})
    return rows


def target_b_rows(primes: list[int], window: int) -> list[dict]:
    gaps = [primes[i + 1] - primes[i] for i in range(len(primes) - 1)]
    rows = []
    half = max(1, window // 2)
    for i in range(half, len(gaps) - half):
        x = primes[i]
        loc = gaps[i - half : i + half + 1]
        gbar = sum(loc) / len(loc)
        y = gbar / max(1e-9, math.log(x))
        rows.append({"x": x, "gap_ma": gbar, "y": y})
    n = len(rows)
    for i, r in enumerate(rows):
        r["split"] = split_label(i, n)
    return rows


def entropy(counts: list[int]) -> float:
    total = sum(counts)
    if total <= 0:
        return 0.0
    h = 0.0
    for c in counts:
        if c <= 0:
            continue
        p = c / total
        h -= p * math.log(p)
    return h


def residue_slot(residue: int, prime: int, modulus: int, surface_mode: str) -> int:
    """Map a residue class to a surface slot.

    unit:   standard residue ring [0, modulus)
    mobius: doubled surface ring [0, 2*modulus) with parity twist
    """
    if surface_mode == "mobius":
        return residue + (modulus if (prime % 2) else 0)
    return residue


def target_c_rows(primes: list[int], x_samples: list[int], modulus: int, surface_mode: str = "unit") -> list[dict]:
    ring_size = modulus * 2 if surface_mode == "mobius" else modulus
    occ = [0] * ring_size
    twin_hits = [0] * ring_size
    rows = []
    j = 0
    prev = None
    for i, x in enumerate(x_samples):
        while j < len(primes) and primes[j] <= x:
            p = primes[j]
            d = residue_slot(p % modulus, p, modulus, surface_mode)
            occ[d] += 1
            if prev is not None and p - prev == 2:
                twin_hits[residue_slot(prev % modulus, prev, modulus, surface_mode)] += 1
                twin_hits[d] += 1
            prev = p
            j += 1

        active = [occ[k] for k in range(ring_size) if math.gcd(k % modulus, modulus) == 1]
        if not active:
            continue
        mean = sum(active) / len(active)
        anis = max(active) - mean
        h = entropy(active)
        tw = sum(twin_hits)
        rows.append(
            {
                "x": x,
                "entropy": h,
                "anisotropy": anis,
                "twin_cohit": tw,
                "y": anis,
                "split": split_label(i, len(x_samples)),
            }
        )
    return rows


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--x-max", type=int, default=1_000_000)
    ap.add_argument("--modulus", type=int, default=360)
    ap.add_argument("--log-grid-points", type=int, default=256)
    ap.add_argument("--window", type=int, default=31)
    ap.add_argument("--surface-mode", choices=["unit", "mobius"], default="unit")
    ap.add_argument("--out-dir", default="data")
    args = ap.parse_args()

    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)

    ps = primes_up_to(args.x_max)
    xs = log_grid(args.x_max, args.log_grid_points)

    a_rows = target_a_rows(ps, xs)
    b_rows = target_b_rows(ps, args.window)
    c_rows = target_c_rows(ps, xs, args.modulus, args.surface_mode)

    write_csv(out / "target_a.csv", a_rows, ["x", "pi_x", "y", "split"])
    write_csv(out / "target_b.csv", b_rows, ["x", "gap_ma", "y", "split"])
    write_csv(out / "target_c.csv", c_rows, ["x", "entropy", "anisotropy", "twin_cohit", "y", "split"])

    manifest = {
        "x_max": args.x_max,
        "modulus": args.modulus,
        "log_grid_points": args.log_grid_points,
        "window": args.window,
        "surface_mode": args.surface_mode,
        "n_primes": len(ps),
        "rows": {"target_a": len(a_rows), "target_b": len(b_rows), "target_c": len(c_rows)},
    }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2))
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
