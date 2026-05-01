#!/usr/bin/env python3
"""Construct a gonal-Möbius-epicyclic embedding with prime basin anchoring.

Layer order (explicit):
1) Gonal address space on n-th roots of unity.
2) Möbius face lift to 2n spinor states.
3) Epicyclic radial modulation.
4) Prime-basin projection for embedding coordinates.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Epicycle:
    rho: float
    chi: int


@dataclass(frozen=True)
class State:
    j: int
    k: int
    face: int
    radius: float
    z: complex


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


def root_of_unity(n: int, k: int) -> complex:
    return complex(math.cos(2 * math.pi * k / n), math.sin(2 * math.pi * k / n))


def mobius_path(n: int, chi: int) -> list[tuple[int, int]]:
    """Return (k_j, f_j) for j in [0, 2n)."""
    path: list[tuple[int, int]] = []
    for j in range(2 * n):
        k = (chi * j) % n
        f = (j // n) % 2
        path.append((k, f))
    return path


def epicyclic_radius(j: int, n: int, cycles: list[Epicycle]) -> float:
    total = 0j
    for l, cyc in enumerate(cycles, start=1):
        angle = cyc.chi * 2 * math.pi * l * j / (2 * n)
        total += cyc.rho * complex(math.cos(angle), math.sin(angle))
    return abs(total)


def build_states(n: int, chi: int, cycles: list[Epicycle]) -> list[State]:
    states: list[State] = []
    for j, (k, f) in enumerate(mobius_path(n, chi)):
        r = epicyclic_radius(j, n, cycles)
        omega = root_of_unity(n, k)
        # Face sign is a lightweight spinor lift into C.
        z = ((-1) ** f) * r * omega
        states.append(State(j=j, k=k, face=f, radius=r, z=z))
    return states


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True


def prime_basins(value: int, anchors: list[int], tau: float) -> list[float]:
    """Soft assignment of an integer into prime basins via log-distance kernel."""
    if value <= 1:
        return [0.0 for _ in anchors]
    log_v = math.log(value)
    raw = [math.exp(-abs(log_v - math.log(p)) / max(1e-9, tau)) for p in anchors]
    s = sum(raw)
    return [v / s if s > 0 else 0.0 for v in raw]


def compose_embedding(value: int, states: list[State], anchors: list[int], tau: float) -> dict[str, float]:
    basin = prime_basins(value, anchors, tau)
    # Use phase index from value to select a state deterministically.
    st = states[value % len(states)]
    out = {
        "value": float(value),
        "prime": float(1 if is_prime(value) else 0),
        "x": st.z.real,
        "y": st.z.imag,
        "face": float(st.face),
        "radius": st.radius,
    }
    for p, w in zip(anchors, basin):
        out[f"basin_p{p}"] = w
    return out


def parse_epicycles(raw: str) -> list[Epicycle]:
    """Parse 'rho:chi,rho:chi,...' into Epicycle records."""
    cycles: list[Epicycle] = []
    for chunk in raw.split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        rho_s, chi_s = chunk.split(":")
        chi = int(chi_s)
        if chi not in (-1, 1):
            raise ValueError(f"Epicycle chirality must be -1 or +1, got {chi}")
        cycles.append(Epicycle(rho=float(rho_s), chi=chi))
    if not cycles:
        raise ValueError("At least one epicycle is required")
    return cycles


def write_csv(path: Path, rows: list[dict[str, float]]) -> None:
    if not rows:
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow(r)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=29, help="gonal size")
    ap.add_argument("--chi", type=int, choices=[-1, 1], default=1, help="global traversal chirality")
    ap.add_argument("--epicycles", default="1.0:1,0.5:-1", help="comma list rho:chi")
    ap.add_argument("--basin-primes", default="3,5,7,13,29,53", help="prime anchors")
    ap.add_argument("--tau", type=float, default=0.35, help="prime basin sharpness")
    ap.add_argument("--max-value", type=int, default=500)
    ap.add_argument("--out", default="data/gonal_mobius_embedding.csv")
    args = ap.parse_args()

    cycles = parse_epicycles(args.epicycles)
    anchors = [int(x.strip()) for x in args.basin_primes.split(",") if x.strip()]
    if any(not is_prime(p) for p in anchors):
        raise ValueError("All basin anchors must be prime numbers")

    states = build_states(args.n, args.chi, cycles)
    rows = [compose_embedding(v, states, anchors, args.tau) for v in range(2, args.max_value + 1)]

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    write_csv(out_path, rows)

    manifest = {
        "n": args.n,
        "chi": args.chi,
        "num_states": len(states),
        "epicycles": [{"rho": c.rho, "chi": c.chi} for c in cycles],
        "basin_primes": anchors,
        "tau": args.tau,
        "max_value": args.max_value,
        "out": str(out_path),
    }
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
