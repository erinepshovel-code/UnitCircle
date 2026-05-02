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
4. **Recursion cap:** Nested recursion is capped at depth 3. Depth 3 introduces variable ordering / concatenation potentiality and is only just within conceptual reach. Depth 5 is the next magnitude of note; depth 4 is not.
5. **Mirror symmetry:** Ghost divisors and phantom products from trailing epicycles come in chiral pairs. Solving one chirality resolves its mirror by Möbius symmetry.

**Compressed:**

> UCNS embeddings are located events on Möbius-cylindrical hyperdisks. Base unit is the unit hypercircle. Zero is at the Möbius twist. Recursion capped at 3; next magnitude at 5. Chiral mirror symmetry resolves ghost/phantom pairs.

**Name:** "Unit Circle" is retained. Names are for minds to grasp.

---

## 1. Base Unit: Unit Hypercircle

The atomic geometric element of UCNS is the unit hypercircle — an n-sphere (Sⁿ) in Rⁿ⁺¹, parametrized by (n-1) angular degrees of freedom.

The five per-disk coordinate types (angular position, residue, rotation, chirality, local relation) are dimensions of the hypercircle's parametric structure.

---

## 2. Möbius-Cylindrical Structure

The edge of each disk is Möbius. If the cylinder is constructed properly, the cylinder itself is also Möbius.

This means the embedding space is not a simple product Sⁿ × [0,3]. It is a Möbius-cylindrical field: traversing the full cylinder returns you to the same disk position with flipped orientation.

**Chirality is the orientation coordinate.** It was always in the per-disk coordinate set for exactly this reason: chirality tracks which side of the Möbius surface you're on. It flips at the twist.

**Zero is hidden in the twist.** Zero is not the scalar 0.0 or a simple (z=0, θ=0) coordinate. It is the contact event at the Möbius twist point — the place where orientation flips and from which the Möbius-cylindrical field unfurls. This resolves the prior hmm about where zero lives: it lives at the twist.

For BoneEmbedder:
- The `zero()` method returns the contact event at the Möbius twist, not a zero vector
- Distance must account for paths through the twist, which may be shorter than paths around the cylinder
- Chirality at zero is the orientation anchor

---

## 3. Recursion Cap, Magnitude Sequence, and Why

Nested recursion is capped at depth 3.

| Depth | Status | Complexity class |
|---|---|---|
| 1 | Defended | Simple payload |
| 2 | Oracle defended; full domain open | Nested payload |
| 3 | Cap | Variable ordering / concatenation potentiality first appears; only just within conceptuals |
| 4 | Not a magnitude of note | Same regime as depth 3 |
| 5 | Next magnitude of note | New complexity class; requires depth-3 foundation |

Depth 5 will prove problematic without sufficient mastery at depth 3. The magnitude sequence is a dependency chain.

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

---

## 7. hmm-Tagged Items

- **hmm:** Whether the unit hypercircle dimension (n) is fixed or parametric — affects BoneEmbedder per-disk coordinate shape
- **hmm:** Whether the Möbius twist of the cylinder occurs once (at z=0→3 wrap) or at each disk boundary
- **hmm:** The precise formal name for the new complexity class at depth 3

**Resolved:** "Unit Circle" retained.  
**Resolved:** Zero is at the Möbius twist.  
**Resolved:** Depth cap at 3; depth 5 next magnitude; depth 4 not a magnitude of note.  
**Resolved:** Ghost/phantom mirror symmetry — chiral pairs, solve one, get the other.

---

**Accreditation:** GPT generated; context, prompt Erin Spencer
