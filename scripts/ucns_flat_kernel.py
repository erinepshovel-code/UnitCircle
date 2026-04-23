#!/usr/bin/env python3
"""Unit Circle Number System (UCNS) — Frozen Flat Spec v0.3 kernel.

Implements paired traversal objects with:
- intrinsic vs declared carriers,
- star operators for angle and face branches,
- normalization and equivalence,
- ordered-concatenation multiplication,
- disk flip,
- finite contiguous factor search.
"""
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from fractions import Fraction
from math import gcd
from typing import Iterable

TWO_TURN = Fraction(2, 1)  # 4π in (2π)-turn units.
ONE_TURN = Fraction(1, 1)  # 2π in (2π)-turn units.


def lcm(a: int, b: int) -> int:
    return abs(a * b) // gcd(a, b)


def lcm_many(values: Iterable[int]) -> int:
    out = 1
    for v in values:
        out = lcm(out, int(v))
    return out


def mod_two_turn(x: Fraction) -> Fraction:
    q = x % TWO_TURN
    return q if q >= 0 else q + TWO_TURN


def mod_one_turn(x: Fraction) -> Fraction:
    q = x % ONE_TURN
    return q if q >= 0 else q + ONE_TURN


def parse_fraction(token: str) -> Fraction:
    token = token.strip()
    if "/" in token:
        a, b = token.split("/", 1)
        return Fraction(int(a), int(b))
    return Fraction(token)


def parse_angle_list(raw: str) -> tuple[Fraction, ...]:
    if not raw.strip():
        return tuple()
    return tuple(parse_fraction(x) for x in raw.split(","))


def parse_face_list(raw: str) -> tuple[int, ...]:
    if not raw.strip():
        return tuple()
    vals = tuple(int(x.strip()) for x in raw.split(","))
    if any(v not in (0, 1) for v in vals):
        raise ValueError("Face bits must be 0/1")
    return vals


def frac_str(x: Fraction) -> str:
    return f"{x.numerator}/{x.denominator}" if x.denominator != 1 else str(x.numerator)


def star_theta(theta_plus: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    return tuple(mod_two_turn(-theta_plus[len(theta_plus) - 1 - j]) for j in range(len(theta_plus)))


def star_face(face_plus: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(face_plus[::-1])


def minimal_gonal_order(theta_plus: tuple[Fraction, ...]) -> int:
    """Smallest n such that all anchors mod 2π lie on k/n lattice."""
    if not theta_plus:
        return 1
    residues = [mod_one_turn(t) for t in theta_plus]
    dens = [r.denominator for r in residues]
    return max(1, lcm_many(dens))


@dataclass(frozen=True)
class UCNSObject:
    n_dec: int
    n_min: int
    theta_plus: tuple[Fraction, ...]
    theta_minus: tuple[Fraction, ...]
    face_plus: tuple[int, ...]
    face_minus: tuple[int, ...]

    def to_json(self) -> dict:
        return {
            "n_dec": self.n_dec,
            "n_min": self.n_min,
            "theta_plus": [frac_str(x) for x in self.theta_plus],
            "theta_minus": [frac_str(x) for x in self.theta_minus],
            "face_plus": list(self.face_plus),
            "face_minus": list(self.face_minus),
            "length": len(self.theta_plus),
        }


@dataclass(frozen=True)
class UCNSZero:
    kind: str = "external_zero"


ZERO = UCNSZero()


def geometric_unit() -> UCNSObject:
    return normalize_object(
        UCNSObject(
            n_dec=1,
            n_min=1,
            theta_plus=(Fraction(0),),
            theta_minus=(Fraction(0),),
            face_plus=(0,),
            face_minus=(0,),
        )
    )


def normalize_object(g: UCNSObject) -> UCNSObject:
    if len(g.theta_plus) != len(g.face_plus):
        raise ValueError("Theta+/Face+ length mismatch")
    if len(g.theta_plus) == 0:
        raise ValueError("Geometric object requires non-empty positive branch")
    if any(bit not in (0, 1) for bit in g.face_plus):
        raise ValueError("Face+ bits must be 0/1")

    shift = g.theta_plus[0]
    theta_plus_norm = tuple(mod_two_turn(t - shift) for t in g.theta_plus)
    n_min = minimal_gonal_order(theta_plus_norm)
    if g.n_dec % n_min != 0:
        raise ValueError(f"Declared carrier n_dec={g.n_dec} must be multiple of n_min={n_min}")

    face_plus_norm = tuple(g.face_plus)
    theta_minus_norm = star_theta(theta_plus_norm)
    face_minus_norm = star_face(face_plus_norm)

    return UCNSObject(
        n_dec=g.n_dec,
        n_min=n_min,
        theta_plus=theta_plus_norm,
        theta_minus=theta_minus_norm,
        face_plus=face_plus_norm,
        face_minus=face_minus_norm,
    )


def build_object(n_dec: int, theta_plus: tuple[Fraction, ...], face_plus: tuple[int, ...]) -> UCNSObject:
    raw = UCNSObject(
        n_dec=n_dec,
        n_min=1,
        theta_plus=theta_plus,
        theta_minus=star_theta(theta_plus),
        face_plus=face_plus,
        face_minus=star_face(face_plus),
    )
    return normalize_object(raw)


def equivalent(a: UCNSObject, b: UCNSObject) -> bool:
    na = normalize_object(a)
    nb = normalize_object(b)
    return (na.n_min, na.theta_plus, na.face_plus) == (nb.n_min, nb.theta_plus, nb.face_plus)


def multiply(a: UCNSObject | UCNSZero, b: UCNSObject | UCNSZero) -> UCNSObject | UCNSZero:
    if isinstance(a, UCNSZero) or isinstance(b, UCNSZero):
        return ZERO

    a = normalize_object(a)
    b = normalize_object(b)

    beta0 = b.theta_plus[0]
    theta_plus_prod: list[Fraction] = []
    face_plus_prod: list[int] = []

    for k, alpha_k in enumerate(a.theta_plus):
        for j, beta_j in enumerate(b.theta_plus):
            theta_plus_prod.append(mod_two_turn(alpha_k + (beta_j - beta0)))
            face_plus_prod.append(a.face_plus[k] ^ b.face_plus[j])

    n_min_prod = lcm(a.n_min, b.n_min)
    n_dec_prod = lcm(a.n_dec, b.n_dec)

    prod = UCNSObject(
        n_dec=n_dec_prod,
        n_min=n_min_prod,
        theta_plus=tuple(theta_plus_prod),
        theta_minus=star_theta(tuple(theta_plus_prod)),
        face_plus=tuple(face_plus_prod),
        face_minus=star_face(tuple(face_plus_prod)),
    )
    out = normalize_object(prod)
    if out.n_min != n_min_prod:
        raise ValueError("Intrinsic carrier propagation invariant violated")
    return out


def disk_flip(g: UCNSObject) -> UCNSObject:
    g = normalize_object(g)
    # Build from swapped positive branch so canonical constraints are re-enforced.
    return build_object(g.n_dec, g.theta_minus, g.face_minus)


def _candidate_factor_lengths(L: int) -> list[tuple[int, int]]:
    out: list[tuple[int, int]] = []
    for p in range(2, L):
        if L % p == 0:
            q = L // p
            if q > 1:
                out.append((p, q))
    return out


def _relative_shape(block: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    base = block[0]
    return tuple(mod_two_turn(x - base) for x in block)


def factor_search(p_obj: UCNSObject) -> list[dict]:
    p_norm = normalize_object(p_obj)
    L = len(p_norm.theta_plus)
    facts: list[dict] = []

    for p, q in _candidate_factor_lengths(L):
        theta_blocks = [p_norm.theta_plus[i * q : (i + 1) * q] for i in range(p)]
        face_blocks = [p_norm.face_plus[i * q : (i + 1) * q] for i in range(p)]

        ref_shape = _relative_shape(theta_blocks[0])
        if any(_relative_shape(b) != ref_shape for b in theta_blocks[1:]):
            continue

        theta_b = ref_shape
        theta_a = tuple(block[0] for block in theta_blocks)

        n_min_a = minimal_gonal_order(theta_a)
        n_min_b = minimal_gonal_order(theta_b)
        if lcm(n_min_a, n_min_b) != p_norm.n_min:
            continue

        fb0 = 0
        fa = tuple(block[0] ^ fb0 for block in face_blocks)
        fb = tuple(face_blocks[0][j] ^ fa[0] for j in range(q))
        ok_faces = True
        for k in range(p):
            for j in range(q):
                if face_blocks[k][j] != (fa[k] ^ fb[j]):
                    ok_faces = False
                    break
            if not ok_faces:
                break
        if not ok_faces:
            continue

        a = build_object(n_dec=n_min_a, theta_plus=theta_a, face_plus=fa)
        b = build_object(n_dec=n_min_b, theta_plus=theta_b, face_plus=fb)
        recon_ab = multiply(a, b)
        recon_ba = multiply(b, a)
        ok_ab = isinstance(recon_ab, UCNSObject) and equivalent(recon_ab, p_norm)
        ok_ba = isinstance(recon_ba, UCNSObject) and equivalent(recon_ba, p_norm)

        if ok_ab or ok_ba:
            facts.append(
                {
                    "p": p,
                    "q": q,
                    "A": a.to_json(),
                    "B": b.to_json(),
                    "reconstruct_ab": bool(ok_ab),
                    "reconstruct_ba": bool(ok_ba),
                }
            )

    return facts


def is_prime_candidate(g: UCNSObject) -> bool:
    return len(factor_search(g)) == 0


def run_self_check() -> dict:
    unit = geometric_unit()
    a = build_object(6, parse_angle_list("0,1/3"), parse_face_list("0,1"))
    b = build_object(4, parse_angle_list("0,1/4,1/2"), parse_face_list("1,0,1"))
    prod = multiply(a, b)
    if not isinstance(prod, UCNSObject):
        raise AssertionError("Unexpected zero product")

    flipped_lhs = disk_flip(prod)
    flipped_rhs = multiply(disk_flip(b), disk_flip(a))
    flip_law = isinstance(flipped_rhs, UCNSObject) and equivalent(flipped_lhs, flipped_rhs)

    factors = factor_search(prod)
    prime_test_obj = build_object(5, parse_angle_list("0,1/5,2/5"), parse_face_list("0,1,1"))

    return {
        "unit": unit.to_json(),
        "A": a.to_json(),
        "B": b.to_json(),
        "AB": prod.to_json(),
        "flip_law_holds": flip_law,
        "factorizations_found": len(factors),
        "prime_candidate_example": is_prime_candidate(prime_test_obj),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    build = sub.add_parser("build")
    build.add_argument("--n-dec", type=int, required=True)
    build.add_argument("--theta-plus", required=True, help="Comma-separated turns over 2π, e.g. 0,1/3,5/3")
    build.add_argument("--face-plus", required=True, help="Comma-separated bits, e.g. 0,1,1")

    mul = sub.add_parser("multiply")
    mul.add_argument("--a-n-dec", type=int, required=True)
    mul.add_argument("--a-theta-plus", required=True)
    mul.add_argument("--a-face-plus", required=True)
    mul.add_argument("--b-n-dec", type=int, required=True)
    mul.add_argument("--b-theta-plus", required=True)
    mul.add_argument("--b-face-plus", required=True)

    fac = sub.add_parser("factor-search")
    fac.add_argument("--n-dec", type=int, required=True)
    fac.add_argument("--theta-plus", required=True)
    fac.add_argument("--face-plus", required=True)

    sub.add_parser("self-check")

    args = ap.parse_args()

    if args.cmd == "build":
        obj = build_object(args.n_dec, parse_angle_list(args.theta_plus), parse_face_list(args.face_plus))
        print(json.dumps({"object": obj.to_json()}, indent=2))
    elif args.cmd == "multiply":
        a = build_object(args.a_n_dec, parse_angle_list(args.a_theta_plus), parse_face_list(args.a_face_plus))
        b = build_object(args.b_n_dec, parse_angle_list(args.b_theta_plus), parse_face_list(args.b_face_plus))
        out = multiply(a, b)
        if isinstance(out, UCNSZero):
            print(json.dumps({"product": "ZERO"}, indent=2))
        else:
            print(json.dumps({"product": out.to_json()}, indent=2))
    elif args.cmd == "factor-search":
        obj = build_object(args.n_dec, parse_angle_list(args.theta_plus), parse_face_list(args.face_plus))
        factors = factor_search(obj)
        print(json.dumps({"object": obj.to_json(), "factors": factors, "prime_candidate": len(factors) == 0}, indent=2))
    elif args.cmd == "self-check":
        print(json.dumps(run_self_check(), indent=2))


if __name__ == "__main__":
    main()
