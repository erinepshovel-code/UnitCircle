# ====================================================================
# E10.9 — Depth-2 Failure Boundary (Spec Note)
# ====================================================================
#
# Purpose: classify the first failing depth-2 example by exact failure stage.
# This is the required first substep of v0.8.0 before any refactor.
# ====================================================================

print("="*72)
print("E10.9 — Depth-2 Failure Boundary")
print("="*72)
print()
print("Primary failure stage:")
print("  PAYLOAD QUOTIENT RECOVERY (recursive)")
print()
print("Secondary failure:")
print("  Missing global witness consistency check")
print()
print("Root cause:")
print("  Current recursion treats S0_A as atomic even when")
print("  it is itself a depth-1 object (S2).")
print()
print("This note is frozen as the first exact failure boundary")
print("driving the v0.8.0 refactor direction.")
