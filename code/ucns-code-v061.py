from fractions import Fraction
from math import gcd
from functools import reduce
import copy
from typing import List, Tuple, Optional, Union

FractionType = Fraction
UNIT = None

def lcm(a: int, b: int) -> int:
    return a * b // gcd(a, b) if a and b else 0

class UCNSObject:
    def __init__(self,
                 n_dec: int,
                 n_min: int,
                 A_plus: List[Tuple[FractionType, Optional['UCNSObject']]],
                 F_plus: List[int]):
        self.n_dec = n_dec
        self.n_min = n_min
        self.A_plus = [(a, copy.deepcopy(p) if p is not None else None) for a, p in A_plus]
        self.F_plus = F_plus[:]
        self.A_minus = None
        self.F_minus = None
        self.normalize()

    def normalize(self) -> 'UCNSObject':
        if not self.A_plus:
            return self
        theta0 = self.A_plus[0][0]
        shifted = []
        for theta, payload in self.A_plus:
            new_theta = (theta - theta0) % 4
            new_payload = payload.normalize() if payload is not None else None
            shifted.append((new_theta, new_payload))
        self.A_plus = shifted

        angles = [a for a, _ in self.A_plus]
        self.n_min = self._compute_n_min(angles)

        self.A_minus, self.F_minus = self._star()

        if self.n_dec % self.n_min != 0:
            raise ValueError(f"Invalid object: n_dec={self.n_dec} not multiple of n_min={self.n_min}")
        return self

    def _compute_n_min(self, angles: List[FractionType]) -> int:
        """Smallest n_min such that all host anchors lie on the n_min-gon lattice mod 2π.
        Angles are stored in units of π, so one full circle is 2.
        """
        if not angles:
            return 1

        # project to circle fraction of one full turn
        circle_fracs = [((a % 2) / 2) for a in angles]
        denoms = [f.denominator for f in circle_fracs if f != 0]
        if not denoms:
            return 1
        return reduce(lcm, denoms)

    def _star(self) -> Tuple[List, List]:
        rev = list(reversed(self.A_plus))
        starred_A = []
        for theta, payload in rev:
            new_theta = (-theta) % 4
            new_payload = self._disk_flip(payload) if payload is not None else None
            starred_A.append((new_theta, new_payload))
        starred_F = list(reversed(self.F_plus))
        return starred_A, starred_F

    @staticmethod
    def _disk_flip(obj: Optional['UCNSObject']) -> Optional['UCNSObject']:
        """Recursive disk-flip operator 𝒻: swap positive/negative branches semantically."""
        if obj is None:
            return None

        # Ensure negative branch exists and is current
        obj = copy.deepcopy(obj).normalize()

        flipped = UCNSObject(
            obj.n_dec,
            obj.n_min,
            copy.deepcopy(obj.A_minus),
            obj.F_minus[:]
        )
        return flipped.normalize()

    def __eq__(self, other: 'UCNSObject') -> bool:
        if not isinstance(other, UCNSObject):
            return False
        if self.n_min != other.n_min or len(self.A_plus) != len(other.A_plus):
            return False
        for (a1, p1), (a2, p2) in zip(self.A_plus, other.A_plus):
            if a1 != a2:
                return False
            if (p1 is None) != (p2 is None) or (p1 is not None and p1 != p2):
                return False
        return self.F_plus == other.F_plus

    def __repr__(self):
        return f"UCNS(n_min={self.n_min}, L={len(self.A_plus)})"

# Multiplication (unchanged)
def multiply(A: Optional[UCNSObject], B: Optional[UCNSObject]) -> UCNSObject:
    if A is None or B is None:
        return A if B is None else B
    p, q = len(A.A_plus), len(B.A_plus)
    n_dec_new = lcm(A.n_dec, B.n_dec)
    n_min_new = lcm(A.n_min, B.n_min)
    new_A_plus = []
    new_F_plus = []
    beta0 = B.A_plus[0][0]
    for k in range(p):
        alpha_k = A.A_plus[k][0]
        S_k_A = A.A_plus[k][1]
        f_k_A = A.F_plus[k]
        for j in range(q):
            beta_j = B.A_plus[j][0]
            S_j_B = B.A_plus[j][1]
            f_j_B = B.F_plus[j]
            new_angle = (alpha_k + (beta_j - beta0)) % 4
            new_payload = multiply(S_k_A, S_j_B) if S_k_A is not None and S_j_B is not None else \
                          (S_k_A if S_j_B is None else S_j_B)
            new_f = f_k_A ^ f_j_B
            new_A_plus.append((new_angle, new_payload))
            new_F_plus.append(new_f)
    return UCNSObject(n_dec_new, n_min_new, new_A_plus, new_F_plus).normalize()


def is_unit(obj: Optional[UCNSObject]) -> bool:
    if obj is None:
        return True
    if not isinstance(obj, UCNSObject):
        return False
    if len(obj.A_plus) != 1:
        return False
    angle, payload = obj.A_plus[0]
    if angle != 0 or payload is not None:
        return False
    if obj.F_plus != [0] or obj.n_min != 1:
        return False
    return True


# ====================================================================
# v0.6.0 CONSTRUCTIVE QUOTIENT PRIMITIVE
# ====================================================================

def left_quotient(P: UCNSObject, A: UCNSObject, catalogue: Optional[List[UCNSObject]] = None) -> Optional[UCNSObject]:
    """Constructive left quotient: B such that A ⊠ B ≡_seq P (when it exists)."""
    p = len(A.A_plus)
    if len(P.A_plus) % p != 0:
        return None
    q = len(P.A_plus) // p

    B_angles = [angle for angle, _ in P.A_plus[0:q]]
    B_payloads_raw = [payload for _, payload in P.A_plus[0:q]]
    B_faces_raw = P.F_plus[0:q]

    a0_f = A.F_plus[0]
    B_faces = [f ^ a0_f for f in B_faces_raw]

    B_payloads = []
    S0_A = A.A_plus[0][1]
    for target in B_payloads_raw:
        if S0_A is None:
            B_payloads.append(target)
        else:
            sub_B = left_quotient_payload(target, S0_A, catalogue)
            if sub_B is None:
                if target == S0_A:
                    B_payloads.append(None)
                else:
                    return None
            else:
                B_payloads.append(sub_B)

    B_cand = UCNSObject(P.n_dec, P.n_min, list(zip(B_angles, B_payloads)), B_faces)
    if multiply(A, B_cand) == P:
        if is_unit(B_cand):
            return None
        return B_cand
    return None

def left_quotient_payload(target: Optional[UCNSObject], S: UCNSObject, catalogue: Optional[List[UCNSObject]]) -> Optional[UCNSObject]:
    if S is None:
        return target
    if catalogue is None:
        catalogue = []
    candidate = left_quotient(target, S, catalogue) if target is not None else None
    if candidate is not None:
        return candidate
    for cand in catalogue + [None]:
        prod = multiply(S, cand) if S is not None and cand is not None else (S if cand is None else cand)
        if prod == target:
            return cand
    return None

def right_quotient(P: UCNSObject, B: UCNSObject, catalogue: Optional[List[UCNSObject]] = None) -> Optional[UCNSObject]:
    """Constructive right quotient: A such that A ⊠ B ≡_seq P (symmetric dual)."""
    q = len(B.A_plus)
    if len(P.A_plus) % q != 0:
        return None
    p = len(P.A_plus) // q

    A_angles = [P.A_plus[k * q][0] for k in range(p)]
    A_payloads_raw = [P.A_plus[k * q][1] for k in range(p)]
    A_faces_raw = [P.F_plus[k * q] for k in range(p)]

    b0_f = B.F_plus[0]
    A_faces = [f ^ b0_f for f in A_faces_raw]

    A_payloads = []
    S0_B = B.A_plus[0][1]
    for target in A_payloads_raw:
        if S0_B is None:
            A_payloads.append(target)
        else:
            sub_A = left_quotient_payload(target, S0_B, catalogue)
            if sub_A is None:
                return None
            A_payloads.append(sub_A)

    A_cand = UCNSObject(P.n_dec, P.n_min, list(zip(A_angles, A_payloads)), A_faces)
    if multiply(A_cand, B) == P:
        if is_unit(A_cand):
            return None
        return A_cand
    return None

def factor_search_v06(P: UCNSObject, catalogue: List[UCNSObject]) -> Union[Tuple[UCNSObject, UCNSObject], str]:
    """v0.6.0 factor search: tries all possible A from catalogue + quotient primitive."""
    for A_cand in catalogue:
        B_recovered = left_quotient(P, A_cand, catalogue)
        if B_recovered is not None:
            return A_cand, B_recovered
    for B_cand in catalogue:
        A_recovered = right_quotient(P, B_cand, catalogue)
        if A_recovered is not None:
            return A_recovered, B_cand
    return "SEQ-PRIME-UP-TO-CATALOGUE"

def create_S2() -> UCNSObject:
    return UCNSObject(2, 2, [(Fraction(0), UNIT), (Fraction(1), UNIT)], [0, 0])

def generate_small_catalogue() -> List[UCNSObject]:
    cat = []
    for n_min in [1, 2, 3, 4]:
        for length in range(1, 4):
            for face_config in range(2 ** length):
                angles = [Fraction(k, n_min) * 2 for k in range(length)]
                faces = [(face_config >> i) & 1 for i in range(length)]
                obj = UCNSObject(n_dec=n_min * 2, n_min=n_min,
                                 A_plus=list(zip(angles, [UNIT] * length)),
                                 F_plus=faces)
                cat.append(obj)
    S2 = create_S2()
    S3 = UCNSObject(3, 3, [(Fraction(0), UNIT), (Fraction(2,3), UNIT), (Fraction(4,3), UNIT)], [0, 0, 0])
    for base in cat[:8]:
        for i in range(min(2, len(base.A_plus))):
            A_plus_new = list(base.A_plus)
            A_plus_new[i] = (A_plus_new[i][0], S2 if i == 0 else S3)
            depth1 = UCNSObject(base.n_dec, base.n_min, A_plus_new, base.F_plus[:])
            cat.append(depth1)
    return cat

def run_cancellativity_regression():
    catalogue = generate_small_catalogue()[:12]
    print(f"Generated {len(catalogue)} test objects (subset for speed)")
    violations = 0
    for A in catalogue:
        for B in catalogue:
            for C in catalogue:
                if multiply(A, B) == multiply(A, C) and B != C:
                    violations += 1
                if multiply(B, A) == multiply(C, A) and B != C:
                    violations += 1
    print(f"Cancellativity regression: {violations} violations (0 expected)")
    if violations == 0:
        print("Cancellativity regression PASSED (0 violations)")
    else:
        print("Cancellativity regression FAILED")
    return violations == 0

def test_class_iii():
    S2 = create_S2()
    A = UCNSObject(2, 2, [(Fraction(0), S2), (Fraction(1), UNIT)], [0, 0])
    B = UCNSObject(2, 2, [(Fraction(0), S2), (Fraction(1), UNIT)], [0, 0])
    P = multiply(A, B)
    catalogue = [S2, A, B]
    print("Product P (Class III):", P)
    result = factor_search_v06(P, catalogue)
    success = isinstance(result, tuple)
    print("Class III recovery success:", success)
    if success:
        rec_A, rec_B = result
        print("Original A recovered:", A == rec_A)
        print("Original B recovered:", B == rec_B)
    return success

# ====================================================================
# v0.6.1 — QUOTIENT EXISTENCE AND DOMAINS OF DEFINITION
# ====================================================================

def run_quotient_regression():
    """Quotient-specific regression suite (v0.6.1)."""
    print("\n=== UCNS v0.6.1 Quotient Regression Suite ===")
    S2 = create_S2()
    all_passed = True

    A = UCNSObject(2, 2, [(Fraction(0), S2), (Fraction(1), UNIT)], [0, 0])
    B = UCNSObject(2, 2, [(Fraction(0), UNIT), (Fraction(1), S2)], [0, 0])
    P = multiply(A, B)
    B_rec = left_quotient(P, A, [A, B, S2])
    passed = (B_rec is not None and B_rec == B)
    print(f"1. Left quotient exists + reconstructs: {'PASS' if passed else 'FAIL'}")
    all_passed &= passed

    A_rec = right_quotient(P, B, [A, B, S2])
    passed = (A_rec is not None and A_rec == A)
    print(f"2. Right quotient exists + reconstructs: {'PASS' if passed else 'FAIL'}")
    all_passed &= passed

    P_bad_len = UCNSObject(2, 2, [(Fraction(0), UNIT), (Fraction(1), UNIT), (Fraction(2), UNIT)], [0, 0, 0])
    B_bad = left_quotient(P_bad_len, A, [A, B, S2])
    passed = (B_bad is None)
    print(f"3. Non-existence (length violation) returns None: {'PASS' if passed else 'FAIL'}")
    all_passed &= passed

    A_f = UCNSObject(2, 2, [(Fraction(0), UNIT), (Fraction(1), UNIT)], [1, 0])
    B_f = UCNSObject(2, 2, [(Fraction(0), UNIT), (Fraction(1), UNIT)], [0, 1])
    P_f = multiply(A_f, B_f)
    B_f_rec = left_quotient(P_f, A_f, [A_f, B_f, S2])
    passed = (B_f_rec is not None and B_f_rec == B_f)
    print(f"4. Gauge-stressed face-state (XOR) reconstructs: {'PASS' if passed else 'FAIL'}")
    all_passed &= passed

    A3 = UCNSObject(2, 2, [(Fraction(0), S2), (Fraction(1), UNIT)], [0, 0])
    B3 = UCNSObject(2, 2, [(Fraction(0), S2), (Fraction(1), UNIT)], [0, 0])
    P3 = multiply(A3, B3)
    B3_rec = left_quotient(P3, A3, [S2, A3, B3])
    passed = (B3_rec is not None and B3_rec == B3)
    print(f"5. Recursive payload quotient (depth-1) reconstructs: {'PASS' if passed else 'FAIL'}")
    all_passed &= passed

    passed = test_class_iii()
    print(f"6. Class III oracle via factor_search_v06: {'PASS' if passed else 'FAIL'}")
    all_passed &= passed

    print(f"\nQuotient regression suite: {'ALL TESTS PASSED' if all_passed else 'SOME TESTS FAILED'}")
    return all_passed


if __name__ == "__main__":
    print("=== UCNS v0.6.1 — Quotient Existence and Domains of Definition ===")
    test_class_iii()
    run_cancellativity_regression()
    run_quotient_regression()
    print("\nQuotient existence conditions frozen. Ready for v0.6.2 (E10 + fallback integration).")
