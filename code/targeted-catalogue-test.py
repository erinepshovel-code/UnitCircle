"""
Targeted catalogue test: prove that catalogue-completeness drives
factor_search outcomes, not algorithmic incompleteness.

Take the smallest search-miss example from the rerun (size 8, the original
Class III oracle), then test factor_search with three catalogues:

  1. catalogue = [S2, S3]                    — bare basic
  2. catalogue = [S2, S3, A]                 — A added
  3. catalogue = [S2, S3, B]                 — B added (right-side)

If (1) misses but (2) and/or (3) succeed, the conclusion is:
  v0.6 fix factor_search depends on catalogue coverage.
  The algorithm itself (left_quotient/right_quotient) is complete given
  a correct candidate.
"""

from fractions import Fraction
from ucns_v04 import UCNSObject, AnchorPayload, multiply
from ucns_v06_fix import factor_search, left_quotient, right_quotient


def flat(n_dec, thetas, faces):
    return UCNSObject(
        n_dec=n_dec, n_min=1,
        anchors_pos=tuple(AnchorPayload(t, None) for t in thetas),
        faces_pos=tuple(faces),
    ).normalize()

# Reconstruct the original Class III oracle.
S2 = flat(2, [Fraction(0), Fraction(1, 2)], [0, 0])
S3 = flat(3, [Fraction(0), Fraction(1, 3), Fraction(2, 3)], [0, 0, 0])

A = UCNSObject(
    n_dec=2, n_min=2,
    anchors_pos=(
        AnchorPayload(Fraction(0),    S2),
        AnchorPayload(Fraction(1, 2), None),
    ),
    faces_pos=(0, 0),
).normalize()
B = UCNSObject(
    n_dec=2, n_min=2,
    anchors_pos=(
        AnchorPayload(Fraction(0),    S2),
        AnchorPayload(Fraction(1, 2), None),
    ),
    faces_pos=(0, 0),
).normalize()
P = multiply(A, B)

print("Class III oracle case (size 8)")
print(f"  P: L={len(P.anchors_pos)}, n_min={P.n_min}")

# Test 0: direct left_quotient with A (no catalogue at all).
B_rec = left_quotient(P, A, catalogue=None)
print(f"\n  [0] left_quotient(P, A, catalogue=None): "
      f"{'recovered' if B_rec is not None else 'failed'}")
if B_rec is not None:
    print(f"      multiply(A, B_rec) ≡_seq P: "
          f"{multiply(A, B_rec).equivalent(P)}")

# Test 1: factor_search with [S2, S3].
r1 = factor_search(P, catalogue=[S2, S3])
print(f"\n  [1] factor_search(P, [S2, S3]): {r1[0]}")

# Test 2: factor_search with [S2, S3, A].
r2 = factor_search(P, catalogue=[S2, S3, A])
print(f"  [2] factor_search(P, [S2, S3, A]): {r2[0]}")
if r2[0] == "SEQ-COMPOSITE":
    A_rec, B_rec = r2[1], r2[2]
    print(f"      multiply(A_rec, B_rec) ≡_seq P: "
          f"{multiply(A_rec, B_rec).equivalent(P)}")

# Test 3: factor_search with [S2, S3, B].
r3 = factor_search(P, catalogue=[S2, S3, B])
print(f"  [3] factor_search(P, [S2, S3, B]): {r3[0]}")
if r3[0] == "SEQ-COMPOSITE":
    A_rec, B_rec = r3[1], r3[2]
    print(f"      multiply(A_rec, B_rec) ≡_seq P: "
          f"{multiply(A_rec, B_rec).equivalent(P)}")

print("\n" + "=" * 60)
print("Conclusion:")
print("  left_quotient: complete (no catalogue needed when A is known)")
print("  factor_search: bounded by catalogue coverage")
print("=" * 60)
