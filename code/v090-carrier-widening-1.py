# ====================================================================
# v0.9.0 — Carrier Widening (after depth-2 oracle) — variant 1
# ====================================================================
#
# Now that depth-2 oracle is GREEN, we widen carriers while keeping
# depth fixed at proven levels.
#
# Widening targets:
#   - n_min from 4 → 5/6
#   - host length from 3 → 4 (on depth-1 and oracle depth-2)
#
# Domain remains: depth ≤ 2 (oracle) or depth ≤ 1 + oracle
# ====================================================================

from fractions import Fraction
import copy

exec(open('/home/workdir/artifacts/ucns_v073.py').read().split('if __name__')[0])

def v090_widened_solver(P, catalogue):
    """v0.9.0 solver on widened carriers"""
    # Use the best depth-2 logic we have
    result = depth2_aware_factor_search(P, catalogue)
    if isinstance(result, tuple):
        return result
    return "SEQ-PRIME-UP-TO-QUOTIENT-DOMAIN"

print("="*72)
print("v0.9.0 — Carrier Widening (after depth-2 oracle)")
print("="*72)

# Generate widened catalogue (higher n_min and host length)
base = generate_small_catalogue()

# Add higher n_min objects
widened = []
for n_min in [5, 6]:
    for length in [1, 2, 3, 4]:
        for face_config in range(2 ** length):
            angles = [Fraction(k, n_min) * 2 for k in range(length)]
            faces = [(face_config >> i) & 1 for i in range(length)]
            try:
                obj = UCNSObject(n_dec=n_min * 2, n_min=n_min,
                                 A_plus=list(zip(angles, [UNIT] * length)),
                                 F_plus=faces)
                widened.append(obj)
            except:
                pass

D_widened = base + widened
print(f"Widened domain: {len(D_widened)} objects (n_min up to 6, host up to 4)")

# Test on widened domain
successes = 0
tested = 0

# Test oracle (depth-2)
S2 = create_S2()
A = UCNSObject(2, 2, [(Fraction(0), S2), (Fraction(1), UNIT)], [0, 0])
B = UCNSObject(2, 2, [(Fraction(0), S2), (Fraction(1), UNIT)], [0, 0])
P = multiply(A, B)
res = v090_widened_solver(P, D_widened)
tested += 1
if isinstance(res, tuple) and res[0] == A and res[1] == B:
    successes += 1
    print("  PASS: Depth-2 oracle on widened carriers")

# Test a few widened objects
import random
random.seed(42)
for _ in range(5):
    if widened:
        A2 = random.choice(widened)
        B2 = UCNSObject(2, 2, [(Fraction(0), UNIT), (Fraction(1), UNIT)], [0, 0])
        P2 = multiply(A2, B2)
        res2 = v090_widened_solver(P2, D_widened)
        tested += 1
        if isinstance(res2, tuple) and res2[0] == A2 and res2[1] == B2:
            successes += 1
            print(f"  PASS: Widened carrier object")

print(f"\nCarrier widening coverage on tested cases: {successes}/{tested} ({100*successes/max(1,tested):.1f}%)")

if successes == tested:
    print("\nSUCCESS: Carrier widening works on tested cases!")
else:
    print("\nSome widened cases are still failing.")
    print("The depth-2 oracle remains GREEN, but full widening needs more work.")

print("="*72)
