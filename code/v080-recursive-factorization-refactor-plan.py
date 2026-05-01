# ====================================================================
# v0.8.0 — Recursive Factorization Refactor (Design Plan)
# ====================================================================
#
# Status: FROZEN DESIGN — do not implement until this plan is accepted.
#
# Goal: Make depth-2 work on the fixed small domain
#       (depth ≤ 2, |A⁺| ≤ 3, n_min ≤ 4)
#       before any carrier widening.
#
# Primary failure traced in E10.9:
#   Payload quotient recursion treats depth-1 S0_A as atomic.
#
# ====================================================================

"""
FOUR DESIGN MOVES (R1–R4) — FROZEN

R1. Staged Reconstruction
    Factor search must be split into three explicit phases:

    Phase 1: Host Recovery Only
        Recover candidate host structures (angles + faces) for A and B
        without touching payloads.

    Phase 2: Payload System Construction
        For every (i, j) cell form the local equation:
            P_{i,j}^payload ≡ S_i^A ⊠ S_j^B
        Collect these as a coupled system (same S_i^A and S_j^B appear
        across multiple cells).

    Phase 3: Global Witness Verification
        Solve the coupled system.
        Only accept the factorization if the entire witness matrix is
        globally consistent.

    Rule: No greedy payload recovery is allowed during host recovery.

R2. Payload Equations as a Coupled System
    Do not solve each P_{i,j}^payload independently.
    Form the full system of equations and solve it as one unit.
    This captures the fact that the same S_i^A and S_j^B appear in
    multiple cells and must be consistent across the whole matrix.

R3. Witness Objects + Global Consistency
    For every local solution, create a witness object:

        W_{i,j} :   S_i^A ⊠ S_j^B  ≡  P_{i,j}^payload

    A factorization is only accepted if the entire witness matrix
    {W_{i,j}} is globally consistent (no contradictory witnesses).

    This directly addresses the secondary failure in E10.9.

R4. Atomicity Rule (Direct Fix for Primary Failure)
    Depth-1 payloads (e.g., S2) must NOT be treated as atomic when
    entered recursively.

    The recursive quotient layer must explicitly descend into them:

        left_quotient_payload(target, S0_A)
            if S0_A is itself a depth-1 object:
                descend one more level
                solve the inner system
            else:
                solve normally

    This is the exact fix required by the E10.9 trace.

==================================================================
FROZEN DOMAIN (unchanged)
==================================================================
D' = { objects with depth ≤ 2, |A⁺| ≤ 3, n_min ≤ 4 }

First code target (v0.8.0.1):
    A minimal witness-matrix solver that makes the smallest failing
    depth-2 oracle (A = B = depth-1 with payload S2) go green.

Only after that oracle passes green do we widen to the rest of D'.

==================================================================
SUCCESS CRITERIA FOR v0.8.0
==================================================================
- Smallest failing oracle returns correct factorization
- All three phases (R1) are clearly separated in code
- Witness matrix is built and verified for global consistency
- No soundness regressions on depth-1 cases
- Domain remains frozen until 100% on D'

This plan is now FROZEN.
Implementation begins only after explicit acceptance.
==================================================================
"""
print("v0.8.0 — Recursive Factorization Refactor Plan (FROZEN)")
print("Four design moves R1–R4 documented above.")
print("First code target: witness-matrix solver on smallest failing oracle.")
print("Domain frozen: depth ≤ 2, |A⁺| ≤ 3, n_min ≤ 4")
