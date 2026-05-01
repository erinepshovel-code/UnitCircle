"""
Class III Finder vs. v0.6 fix — what (if anything) does the new primitive still miss?

Search space (same as the original class3_finder for direct comparability):
  - host lengths p, q ∈ {2, 3}
  - host carriers from {2, 3}
  - payload alphabet: {None, S_2, S_3} where S_2, S_3 are flat 2-gon / 3-gon

For each (A, B) pair with both S^A_0 and S^B_0 non-unit (the original
Class III condition):

  1. Build P = A ⊠ B by construction.
  2. Confirm refined E10 (v0.5) misses it (sanity: it's actually Class III).
  3. Test v0.6 fix in two flavors:
     (a) left_quotient(P, A, catalogue=None)  — direct, structural only
     (b) factor_search(P, catalogue=[A, B, S_2, S_3]) — bounded search

Tally:
  - direct miss:  v0.6 left_quotient with A given returns None
  - search miss:  v0.6 factor_search returns SEQ-PRIME-UP-TO-CATALOGUE
"""

from __future__ import annotations
from fractions import Fraction
from itertools import product as iproduct
from typing import List, Optional

from ucns_v04 import (
    UCNSObject, AnchorPayload,
    unit_obj, is_unit_payload, multiply,
)
from ucns_v05 import sequence_factor_search
from ucns_v06_fix import left_quotient, right_quotient, factor_search


# ---------- payload alphabet (matching the original finder) ----------

def flat(n_dec, thetas, faces):
    return UCNSObject(
        n_dec=n_dec, n_min=1,
        anchors_pos=tuple(AnchorPayload(t, None) for t in thetas),
        faces_pos=tuple(faces),
    ).normalize()

S2 = flat(2, [Fraction(0), Fraction(1, 2)], [0, 0])
S3 = flat(3, [Fraction(0), Fraction(1, 3), Fraction(2, 3)], [0, 0, 0])

PAYLOADS_NONUNIT = [S2, S3]
PAYLOADS_WITH_UNIT = [None, S2, S3]


# ---------- object construction ----------

def make_object(anchors, payloads):
    L = len(anchors)
    assert len(payloads) == L
    shift = anchors[0]
    shifted = [(t - shift) % 2 for t in anchors]
    raw = UCNSObject(
        n_dec=6, n_min=1,
        anchors_pos=tuple(AnchorPayload(t, p) for t, p in zip(shifted, payloads)),
        faces_pos=tuple([0] * L),
    )
    return raw.normalize()


def host_anchor_sets():
    yield (2, [Fraction(0), Fraction(1, 2)])
    yield (3, [Fraction(0), Fraction(1, 3)])
    yield (3, [Fraction(0), Fraction(1, 3), Fraction(2, 3)])


def enumerate_class3_candidates():
    """Yield (A, B, meta, size) with both leading payloads non-unit."""
    host_configs = list(host_anchor_sets())
    out = []
    for (n_A, anchors_A), (n_B, anchors_B) in iproduct(host_configs, host_configs):
        p = len(anchors_A); q = len(anchors_B)
        for first_A in PAYLOADS_NONUNIT:
            for rest_A in iproduct(PAYLOADS_WITH_UNIT, repeat=p-1):
                payloads_A = [first_A] + list(rest_A)
                for first_B in PAYLOADS_NONUNIT:
                    for rest_B in iproduct(PAYLOADS_WITH_UNIT, repeat=q-1):
                        payloads_B = [first_B] + list(rest_B)
                        try:
                            A = make_object(anchors_A, payloads_A)
                            B = make_object(anchors_B, payloads_B)
                        except ValueError:
                            continue
                        size = p + q + sum(
                            len(x.anchors_pos) for x in payloads_A + payloads_B
                            if x is not None
                        )
                        out.append((size, A, B, (p, q, n_A, n_B)))
    out.sort(key=lambda t: t[0])
    for size, A, B, meta in out:
        yield A, B, meta, size


# ---------- runner ----------

def main():
    print("=" * 72)
    print("Class III rerun vs. v0.6 fix")
    print("=" * 72)

    # Catalogue for factor_search: includes both the basic flat objects and
    # the depth-1 building blocks. We deliberately do NOT include the specific
    # A and B for each test — we want to see if factor_search can find them.
    catalogue = [S2, S3]

    total = 0
    e10_misses = 0
    v06_direct_misses = 0
    v06_search_misses = 0
    direct_examples = []
    search_examples = []

    for A, B, meta, size in enumerate_class3_candidates():
        try:
            P = multiply(A, B)
        except Exception:
            continue
        total += 1

        # Sanity: this should be Class III (no unit leading block).
        p, q, _, _ = meta
        blocks = [P.anchors_pos[i*q:(i+1)*q] for i in range(p)]
        if any(is_unit_payload(blocks[i][0].payload) for i in range(p)):
            # Not actually Class III for this (p,q). Skip.
            continue

        # Sanity: confirm v0.5 E10 misses it.
        e10 = sequence_factor_search(P)
        if e10[0] != "SEQ-PRIME":
            # E10 didn't miss it — not Class III in practice for this case.
            continue
        e10_misses += 1

        # v0.6 fix: direct test (left_quotient with A given, no catalogue).
        B_rec = left_quotient(P, A, catalogue=None)
        direct_ok = (B_rec is not None and multiply(A, B_rec).equivalent(P))
        if not direct_ok:
            v06_direct_misses += 1
            if len(direct_examples) < 5:
                direct_examples.append((size, A, B, P, meta))

        # v0.6 fix: search test (factor_search with bounded catalogue).
        result = factor_search(P, catalogue=catalogue)
        search_ok = (result[0] == "SEQ-COMPOSITE"
                     and multiply(result[1], result[2]).equivalent(P))
        if not search_ok:
            v06_search_misses += 1
            if len(search_examples) < 5:
                search_examples.append((size, A, B, P, meta))

    print(f"\n  Total candidates considered:        {total}")
    print(f"  v0.5 E10-refined misses (Class III):  {e10_misses}")
    print(f"  v0.6 fix direct misses (no cat):       {v06_direct_misses}")
    print(f"  v0.6 fix search misses (cat=[S2,S3]):  {v06_search_misses}")

    if direct_examples:
        print("\n  Sample direct misses (left_quotient(P, A) → None):")
        for size, A, B, P, meta in direct_examples[:3]:
            p, q, n_A, n_B = meta
            print(f"    size={size}, p={p} q={q}, n_A={n_A} n_B={n_B}")
            print(f"      A: L={len(A.anchors_pos)} payloads="
                  f"{['·' if a.payload is None else f'L{len(a.payload.anchors_pos)}' for a in A.anchors_pos]}")
            print(f"      B: L={len(B.anchors_pos)} payloads="
                  f"{['·' if b.payload is None else f'L{len(b.payload.anchors_pos)}' for b in B.anchors_pos]}")
            print(f"      P: L={len(P.anchors_pos)}, n_min={P.n_min}")

    if search_examples:
        print("\n  Sample search misses (factor_search → SEQ-PRIME-UP-TO-CATALOGUE):")
        for size, A, B, P, meta in search_examples[:3]:
            p, q, n_A, n_B = meta
            print(f"    size={size}, p={p} q={q}, n_A={n_A} n_B={n_B}")
            print(f"      A: L={len(A.anchors_pos)} payloads="
                  f"{['·' if a.payload is None else f'L{len(a.payload.anchors_pos)}' for a in A.anchors_pos]}")
            print(f"      B: L={len(B.anchors_pos)} payloads="
                  f"{['·' if b.payload is None else f'L{len(b.payload.anchors_pos)}' for b in B.anchors_pos]}")

    print("\n" + "=" * 72)
    if v06_direct_misses == 0:
        print("v0.6 fix left_quotient is COMPLETE on this domain (when A is given).")
    else:
        print(f"v0.6 fix left_quotient still misses {v06_direct_misses} cases — "
              f"genuine open subclass.")
    if v06_search_misses == 0:
        print("v0.6 fix factor_search is COMPLETE on this domain "
              "(catalogue=[S2,S3] suffices).")
    else:
        print(f"v0.6 fix factor_search misses {v06_search_misses} cases at "
              f"this catalogue size.")
    print("=" * 72)


if __name__ == "__main__":
    main()
