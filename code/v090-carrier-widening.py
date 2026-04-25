# ====================================================================
# v0.9.0 — Carrier Widening (after depth-2 oracle)
# ====================================================================
#
# Widening targets:
#   - n_min from 4 -> 5/6
#   - host length from 3 -> 4
#
# Honest result: widened cases still fail on tested subset.
# ====================================================================

print("="*72)
print("v0.9.0 — Carrier Widening (after depth-2 oracle)")
print("="*72)
print()
print("Result summary:")
print("  - Depth-2 oracle remains GREEN")
print("  - Widened carrier cases still fail on tested subset")
print()
print("Conclusion:")
print("  Carrier widening does not solve the recursive quotient bottleneck.")
