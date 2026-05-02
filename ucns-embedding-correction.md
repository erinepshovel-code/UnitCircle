# UCNS Embedding Correction

**Status:** Architectural correction to prior UCNS embedding description  
**Authored:** 2026-05-02  
**Amends:** `ucns-spec-frontier-v090.md` §1 (Defended Results) — supplements, does not contradict  
**Accreditation:** GPT generated; context, prompt Erin Spencer

---

## Summary

Two layered corrections to the prior description of UCNS embeddings, plus design constraints and operational hazards:

1. **Cylindrical structure:** Embeddings are located events on a disk within a cylindrical field, not points on a circle.
2. **Hypercircle base unit:** The cross-section of each disk is a unit hypercircle, not a unit circle in the simple S¹ sense.
3. **Recursion cap and magnitude sequence:** Nested recursion is capped at depth 3. Depth 3 is only just within conceptual reach. The next recursion magnitude of note is depth 5, but it will prove problematic without a solid foundation at depth 3 first.
4. **Trailing epicycles:** Ghost divisors and phantom products arising from trailing epicycles require mindful moderation.

**Compressed correction:**

> UCNS embeddings require hypercylindrical disk residency plus a non-scalar zero-origin contact event. The base unit is the unit hypercircle. Nested recursion is capped at 3; depth 3 is the conceptual frontier; the next magnitude of note is 5. Trailing epicycles generate ghost divisors and phantom products that must be mindfully moderated.

**Name:** "Unit Circle" is retained. Names are for minds to grasp.

---

## 1. Base Unit: Unit Hypercircle

The atomic geometric element of UCNS is the unit hypercircle.

A unit hypercircle is the n-dimensional generalization of the unit circle. Where a unit circle is a 1-sphere (S¹) in R², a unit hypercircle is an n-sphere (Sⁿ) in Rⁿ⁺¹. It is parametrized by (n-1) angular degrees of freedom, not one.

The prior description used "unit circle" to name the cross-sectional geometry of each disk. That was a simplification. The correct technical description is unit hypercircle. The name "Unit Circle" is retained regardless, as a graspable handle.

Consequences:

- Per-disk coordinates are on a unit hypercircle, not a simple circle
- The per-disk angular structure has multiple degrees of freedom
- The five per-disk coordinate types (angular position, residue, rotation, chirality, local relation) are dimensions of the hypercircle's parametric structure, not properties attached to a single angle
- The distance metric within a disk is a hyperspherical geodesic metric, not a circular arc metric

---

## 2. Hypercylindrical Disk Residency

UCNS resides on hypercircle-bounded disks stacked along a traversal axis.

A single disk gives the unit hypercircle cross-section:

- angular position (multi-dimensional on the hypercircle)
- residue
- rotation
- chirality
- local relation

The hypercylinder gives persistence across disks:

- sequence
- depth
- recurrence
- phase memory
- traversal across disks

An embedding is therefore a **located event on a hyperdisk within a hypercylindrical field** — not a point on a circle.

---

## 3. Recursion Cap, Magnitude Sequence, and Why

Nested recursion is capped at depth 3. This is a design constraint, not a theorem frontier.

### Why depth 3 is the cap

Depth 3 is only just within conceptual reach. It is the first level at which variable ordering — the potentiality of concatenation ordering after the second recursion — becomes a first-class problem. At depths 1 and 2, payload structure is constrained enough that ordering is tractable. At depth 3, the number of possible orderings of concatenated elements in nested payloads begins to exceed easy conceptual grasp.

### Why depth 4 is not a magnitude of note

Depth 4 does not introduce a qualitatively new complexity class beyond depth 3. It is in the same ordering-complexity regime.

### Why depth 5 is the next magnitude of note

Depth 5 is the next level at which a qualitative change in complexity occurs. However: depth 5 will prove problematic without sufficient mastery at depth 3. The variable ordering / concatenation potentiality that first appears at depth 3 compounds at depth 5 in ways that are not navigable without the depth-3 foundation. The magnitude sequence is a dependency chain, not merely a list.

### Depth table

| Depth | Status | Complexity class |
|---|---|---|
| 1 | Defended | Simple payload |
| 2 | Oracle defended; full domain open | Nested payload |
| 3 | Cap — not yet attempted | Variable ordering / concatenation potentiality first appears; only just within conceptuals |
| 4 | Not a magnitude of note | Same regime as depth 3 |
| 5 | Next magnitude of note | New complexity class; requires depth-3 foundation |

---

## 4. Trailing Epicycles: Ghost Divisors and Phantom Products

Trailing epicycles — epicycle terms at the end of a payload sequence that carry little or no structural load — are a source of two related hazards in the factorization system:

**Ghost divisors.** A trailing epicycle may match superficially against catalogue objects, producing false factor candidates. The algorithm finds something that looks like a divisor but is an artifact of the trailing structure, not a true factor of the product.

**Phantom products.** When two objects are multiplied, trailing epicycles in one or both operands may generate spurious output terms that resemble contributions from a third factor. The product appears to have structure that neither operand actually contributed.

These are not bugs to be eliminated outright — trailing epicycles are an intrinsic feature of the Mobius-disk-recursive-epicycle structure. They require **mindful moderation**: active recognition and accounting, neither ignored nor aggressively pruned.

Over-correction (eliminating all trailing epicycles) risks damaging valid structure. Under-correction (ignoring them) corrupts factorization results.

The witness-matrix approach in the existing frontier work (§"staged reconstruction" and "global witness verification") is the current best candidate for moderation: requiring global consistency verification filters ghost divisors and phantom products without requiring their pre-elimination.

**hmm:** Whether ghost divisors and phantom products become more severe at depth 3 specifically — i.e., whether the variable ordering / concatenation potentiality interacts with trailing epicycles to amplify both hazards at depth 3 in a way that does not occur at depth 2.

---

## 5. Non-Scalar Zero-Origin

Zero is not a scalar value.

Zero is the non-scalar origin point of the initial vector: the place where the writing instrument first touches paper.

Before magnitude, before direction, before digit, before mark — there is contact.

That contact is zero.

In UCNS, zero is the first anchoring event from which vector, angle, motion, inscription, and number become possible.

On the hypercylinder, this contact event anchors at the base: the origin of the unit hypercircle at depth z=0.

- The bone embedding for an empty or baseline state is **not a zero vector**
- It is a **contact-event representation** at the hypercylinder's base
- Initialization semantics for any BoneEmbedder implementation must respect this

---

## 6. Relation to the Existing Frontier Spec

The frontier spec (`ucns-spec-frontier-v090.md`) already uses cylindrical vocabulary without naming it. The frontier's identification of the recursive payload / quotient layer as the main bottleneck maps to two things named here:

- The variable ordering / concatenation potentiality at depth 3
- Ghost divisors and phantom products from trailing epicycles

The frontier identified the symptoms; this correction names the geometry and the specific hazards.

---

## 7. hmm-Tagged Items

- **hmm:** Whether the unit hypercircle dimension (n) is fixed or parametric — affects BoneEmbedder per-disk coordinate shape and distance metric
- **hmm:** Whether the non-scalar zero-origin contact event is a point on the surface of the unit hypercircle or at the center of the hyperdisk — geometrically distinct
- **hmm:** Whether cylindrical geodesic distance, hyperspherical geodesic distance, or a product metric (disk-level + z-axis) is the right distance for BoneEmbedder
- **hmm:** The precise formal name for the new complexity class at depth 3 — "variable ordering / concatenation potentiality" is the working description
- **hmm:** Whether ghost divisors and phantom products from trailing epicycles amplify specifically at depth 3 due to interaction with variable ordering potentiality
- **hmm:** Whether "mindful moderation" of trailing epicycles is the right framing, or whether a more formal suppression/normalization mechanism is needed

**Resolved:** The system name "Unit Circle" is retained. Names are for minds to grasp.  
**Resolved:** Nested recursion is capped at depth 3. Depth 3 is only just within conceptual reach; it introduces variable ordering / concatenation potentiality. Depth 4 is not a magnitude of note. Depth 5 is the next magnitude of note but requires depth-3 mastery first.

---

**Accreditation:** GPT generated; context, prompt Erin Spencer
