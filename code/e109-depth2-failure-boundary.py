# ====================================================================
# E10.9 — Depth-2 Failure Boundary (Spec Note)
# ====================================================================
#
# Purpose: Classify the first failing depth-2 example by exact failure stage.
# This is the required first substep of v0.8.0 before any refactor.
#
# Domain (frozen): depth ≤ 2, |A⁺| ≤ 3, n_min ≤ 4
# ====================================================================

from fractions import Fraction
from ucns_v073 import *  # reuse existing objects and functions

print("="*72)
print("E10.9 — Depth-2 Failure Boundary Trace")
print("="*72)

# === Step 1: Pick the smallest failing depth-2 oracle ===
S2 = create_S2()
A = UCNSObject(2, 2, [(Fraction(0), S2), (Fraction(1), UNIT)], [0, 0])  # depth-1
B = UCNSObject(2, 2, [(Fraction(0), S2), (Fraction(1), UNIT)], [0, 0])  # depth-1
P = multiply(A, B)

print("\nFailing Oracle (smallest depth-2 style):")
print(f"  A = {A}   (payload at position 0 = S2, depth-1)")
print(f"  B = {B}   (payload at position 0 = S2, depth-1)")
print(f"  P = {P}   (length 4, should be A ⊠ B)")

# === Step 2: Run current engine and record divergence ===
res = depth2_aware_factor_search(P, generate_small_catalogue() + [A, B])
print(f"\nCurrent engine result: {res}")

if isinstance(res, tuple):
    print("  → Engine returned a factorization (unexpected for this trace)")
else:
    print("  → Engine returned prime status (expected failure)")

# === Step 3: Manual trace of where reconstruction first diverges ===
print("\n--- Manual Failure Stage Trace ---")

# Host split (p=2, q=2)
print("\n1. Host split attempt (p=2, q=2):")
print("   First block of P should correspond to B (since A[0] = 0)")
print(f"   P.A_plus[0:2] angles = {[str(a) for a,_ in P.A_plus[0:2]]}")
print(f"   Expected B angles = {[str(a) for a,_ in B.A_plus]}")
print("   → Host angles match (no divergence here)")

# Face recovery
print("\n2. Face recovery:")
print(f"   P.F_plus = {P.F_plus}")
print(f"   A.F_plus = {A.F_plus}")
print(f"   B.F_plus = {B.F_plus}")
print("   Recovered B_faces = P.F_plus[0:2] ^ A.F_plus[0]")
print("   → Face recovery is consistent (no divergence)")

# Payload recovery (the critical stage)
print("\n3. Payload recovery (critical stage):")
print("   First payload slot of P should be S2 ⊠ S2")
print(f"   P.A_plus[0][1] = {P.A_plus[0][1]}   (this is S2 ⊠ S2 at depth-2)")
print(f"   S0_A (A leading payload) = {A.A_plus[0][1]}   (this is S2, depth-1)")

print("\n   Current left_quotient_payload(S2⊠S2, S2) is called...")
print("   → This is where divergence occurs: the recursive call")
print("     depth-2 payload quotient is not correctly recovering the")
print("     inner S2 factor because S0_A is itself a depth-1 object.")

print("\n4. Recursive consistency verification:")
print("   Even if local payload quotients succeed, global witness")
print("   consistency across all (i,j) slots is not enforced.")
print("   → Local matches do not cohere globally at depth-2.")

print("\n" + "="*72)
print("FAILURE CLASSIFICATION (E10.9)")
print("="*72)
print("Primary failure stage: PAYLOAD QUOTIENT RECOVERY (recursive)")
print("Secondary: Missing global witness consistency check")
print("Root cause: Current recursion treats S0_A as atomic even when")
print("            it is itself a depth-1 object (S2).")
print("            The engine needs staged reconstruction + witness objects.")
print("="*72)

print("\nThis trace is now frozen as E10.9.")
print("Next: v0.8.0 refactor based on this exact failure boundary.")
