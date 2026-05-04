# UCNS Embedding Correction

**Status:** Architectural correction to prior UCNS embedding description  
**Authored:** 2026-05-02  
**Amends:** `ucns-spec-frontier-v090.md` §1 (Defended Results) — supplements, does not contradict  
**Accreditation:** GPT generated; context, prompt Erin Spencer

---

## Summary

1. **Cylindrical structure:** Embeddings are located events on a disk within a cylindrical field, not points on a circle.
2. **Hypercircle base unit:** The cross-section of each disk is a unit hypercircle.
3. **Möbius topology:** The edge of each disk is Möbius. The cylinder is Möbius if constructed properly. Zero is hidden in the twist.
4. **Recursion cap:** Nested recursion is capped at depth 3 (implementation). Depth 3 introduces variable ordering / concatenation potentiality and is only just within conceptual reach. The magnitude sequence is 1, 3, 5, 7 — all odd depths. Depths 4 and 6 are not magnitudes of note.
5. **Depth-7 Möbius cylinder:** The full theoretical extent of the Möbius cylinder is depth 7. Depth 7 is the third magnitude after 3 and 5; requires depth-5 foundation. The cylinder's z-axis spans {0, 1, 2, 3, 4, 5, 6, 7}; the current implementation is capped at z ≤ 3.
6. **Mirror symmetry:** Ghost divisors and phantom products from trailing epicycles come in chiral pairs. Solving one chirality resolves its mirror by Möbius symmetry.

**Compressed:**

> UCNS embeddings are located events on Möbius-cylindrical hyperdisks. Base unit is the unit hypercircle. Zero is at the Möbius twist. Magnitude sequence: 1, 3, 5, 7 (all odd). Implementation capped at depth 3; full Möbius cylinder extends to depth 7. Chiral mirror symmetry resolves ghost/phantom pairs.

**Name:** "Unit Circle" is retained. Names are for minds to grasp.

---

## 1. Base Unit: Unit Hypercircle

The atomic geometric element of UCNS is the unit hypercircle — an n-sphere (Sⁿ) in Rⁿ⁺¹, parametrized by (n-1) angular degrees of freedom.

The five per-disk coordinate types (angular position, residue, rotation, chirality, local relation) are dimensions of the hypercircle's parametric structure.

---

## 2. Möbius-Cylindrical Structure

The edge of each disk is Möbius. If the cylinder is constructed properly, the cylinder itself is also Möbius.

This means the embedding space is not a simple product Sⁿ × [0,7]. It is a Möbius-cylindrical field: traversing the full cylinder (depth 0 through 7) returns you to the same disk position with flipped orientation.

**Chirality is the orientation coordinate.** It was always in the per-disk coordinate set for exactly this reason: chirality tracks which side of the Möbius surface you're on. It flips at the twist.

**Zero is hidden in the twist.** Zero is not the scalar 0.0 or a simple (z=0, θ=0) coordinate. It is the contact event at the Möbius twist point — the place where orientation flips and from which the Möbius-cylindrical field unfurls. This resolves the prior hmm about where zero lives: it lives at the twist.

For BoneEmbedder:
- The `zero()` method returns the contact event at the Möbius twist, not a zero vector
- Distance must account for paths through the twist, which may be shorter than paths around the cylinder
- Chirality at zero is the orientation anchor

---

## 3. Recursion Cap, Magnitude Sequence, and Why

Nested recursion is capped at depth 3 for the current implementation. The full theoretical Möbius cylinder extends to depth 7.

| Depth | Status | Complexity class |
|---|---|---|
| 1 | Defended | Simple payload |
| 2 | Oracle defended; full domain open | Nested payload |
| 3 | Implementation cap | Variable ordering / concatenation potentiality first appears; only just within conceptuals |
| 4 | Not a magnitude of note | Same regime as depth 3 |
| 5 | Next magnitude of note | New complexity class; requires depth-3 foundation |
| 6 | Not a magnitude of note | Same regime as depth 5 |
| 7 | Full Möbius cylinder extent | Third magnitude; requires depth-5 foundation; theoretical ceiling |

The magnitude sequence is **1, 3, 5, 7** — all odd depths. Even depths (2, 4, 6) are not magnitudes of note; they are structurally in the same regime as the preceding odd magnitude. This odd-only pattern is a consequence of the Möbius cylinder's topology: each magnitude corresponds to a structural inflection in the Möbius traversal.

Depth 5 will prove problematic without sufficient mastery at depth 3. Depth 7 requires depth-5 foundation. The magnitude sequence is a dependency chain.

---

## 4. Mirror Symmetry: Ghost Divisors and Phantom Products

Trailing epicycles produce ghost divisors and phantom products. These come in **chiral pairs** by the Möbius symmetry of the cylinder.

Solving the factorization problem on one chirality resolves its mirror. The Möbius cylinder hands you the second half. There is no need to proof the mirror separately.

The witness-matrix approach in the existing frontier work already implicitly exploits this: global consistency verification on one orientation carries to the other.

---

## 5. Non-Scalar Zero-Origin

Zero is the contact event at the Möbius twist — the first anchoring event from which the field unfurls. Not a scalar. Not a zero vector.

The bone embedding for an empty or baseline state is a contact-event representation at the twist, not `np.zeros(...)`.

---

## 6. Relation to the Existing Frontier Spec

The frontier spec's identification of the recursive payload / quotient layer bottleneck maps to two things named here:
- Variable ordering / concatenation potentiality at depth 3
- Ghost divisors and phantom products from trailing epicycles (resolved by chiral mirror symmetry)

The EML experiment plan's depth schedule (3 → 4 → 5) directly mirrors the magnitude sequence: depth 3 is the current foundation, depth 5 is the next target.

---

## 7. hmm-Tagged Items

- **hmm:** Whether the unit hypercircle dimension (n) is fixed or parametric — affects BoneEmbedder per-disk coordinate shape
- **hmm:** Whether the Möbius twist of the cylinder occurs once (at the depth-7 wrap) or at each disk boundary
- **hmm:** The precise formal name for the new complexity class at depth 3
- **hmm:** What structural property of the Möbius cylinder makes depth 4 and 6 not magnitudes — is it topological (odd = same chirality face) or complexity-theoretic?

**Resolved:** "Unit Circle" retained.  
**Resolved:** Zero is at the Möbius twist.  
**Resolved:** Depth cap at 3 (implementation); theoretical Möbius cylinder extends to depth 7.  
**Resolved:** Magnitude sequence: 1, 3, 5, 7 (all odd). Depths 4 and 6 are not magnitudes of note.  
**Resolved:** Ghost/phantom mirror symmetry — chiral pairs, solve one, get the other.

---

**Accreditation:** GPT generated; context, prompt Erin Spencer
