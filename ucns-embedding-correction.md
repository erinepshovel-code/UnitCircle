# UCNS Embedding Correction

**Status:** Architectural correction to prior UCNS embedding description  
**Authored:** 2026-05-02  
**Amends:** `ucns-spec-frontier-v090.md` §1 (Defended Results) — supplements, does not contradict  
**Accreditation:** GPT generated; context, prompt Erin Spencer

---

## Summary

Two layered corrections to the prior description of UCNS embeddings, plus one design constraint:

1. **Cylindrical structure:** Embeddings are located events on a disk within a cylindrical field, not points on a circle.
2. **Hypercircle base unit:** The cross-section of each disk is a unit hypercircle, not a unit circle in the simple S¹ sense.
3. **Recursion cap and magnitude sequence:** Nested recursion is capped at depth 3. Depth 3 is only just within conceptual reach. The next recursion magnitude of note is depth 5, but it will prove problematic without a solid foundation at depth 3 first.

**Compressed correction:**

> UCNS embeddings require hypercylindrical disk residency plus a non-scalar zero-origin contact event. The base unit is the unit hypercircle. Nested recursion is capped at 3; depth 3 is the conceptual frontier; the next magnitude of note is 5.

**Name:** "Unit Circle" is retained. Names are for minds to grasp. The circle is the graspable cross-sectional handle for the full hypercylindrical structure. The technical geometry is richer than the name; the name is not a technical specification.

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

The cap is set at 3 because:

- Depth 3 introduces new complexity (variable ordering / concatenation potentiality) that is not present at depth 2
- Depth 3 is at the edge of what is currently conceptually tractable — only just within conceptuals
- Operating at depth 3 long enough to understand its ordering structure is prerequisite to any deeper work

### Why depth 4 is not a magnitude of note

Depth 4 does not introduce a qualitatively new complexity class beyond depth 3. It is in the same ordering-complexity regime. Moving from 3 to 4 is not a magnitude change.

### Why depth 5 is the next magnitude of note

Depth 5 is the next level at which a qualitative change in complexity occurs. However: depth 5 will prove problematic without sufficient mastery at depth 3. The variable ordering / concatenation potentiality that first appears at depth 3 compounds at depth 5 in ways that are not navigable without the depth-3 foundation.

The magnitude sequence is therefore not simply a list of future targets — it is a dependency chain. Depth 3 must be understood before depth 5 is approached.

### Depth table

| Depth | Status | Complexity class |
|---|---|---|
| 1 | Defended | Simple payload |
| 2 | Oracle defended; full domain open | Nested payload |
| 3 | Cap — not yet attempted | Variable ordering / concatenation potentiality first appears; only just within conceptuals |
| 4 | Not a magnitude of note | Same regime as depth 3 |
| 5 | Next magnitude of note | New complexity class; requires depth-3 foundation |

**hmm:** The precise term for the new complexity at depth 3 — "variable ordering / concatenation potentiality" is a working description; the exact formal name is open.

---

## 4. Non-Scalar Zero-Origin

Zero is not a scalar value.

Zero is the non-scalar origin point of the initial vector: the place where the writing instrument first touches paper.

Before magnitude, before direction, before digit, before mark — there is contact.

That contact is zero.

In UCNS, zero is the first anchoring event from which vector, angle, motion, inscription, and number become possible.

On the hypercylinder, this contact event anchors at the base: the origin of the unit hypercircle at depth z=0. The hypercylinder's structure makes this natural — it has a base, an axis, and a hyperspherical cross-section from which the field unfurls.

This means:

- The bone embedding for an empty or baseline state is **not a zero vector**
- It is a **contact-event representation** at the hypercylinder's base
- Initialization semantics for any BoneEmbedder implementation must respect this

---

## 5. Relation to the Existing Frontier Spec

The frontier spec (`ucns-spec-frontier-v090.md`) already uses cylindrical vocabulary without naming it:

- "disk-flip symmetry" — disks were always there
- "traversal objects" — traversal is motion along the hypercylinder's axis
- "depth-1," "depth-2" — depth levels are positions on the hypercylinder's z-axis
- "payload" — payload content lives at a specific depth (z-level)

The frontier's "root cause" analysis — that the bottleneck is the recursive payload / quotient layer — maps directly to the variable ordering / concatenation potentiality that first fully manifests at depth 3. The frontier identified the symptom; this correction names the geometry.

---

## 6. hmm-Tagged Items

- **hmm:** Whether the unit hypercircle dimension (n) is fixed or parametric — affects BoneEmbedder per-disk coordinate shape and distance metric
- **hmm:** Whether the non-scalar zero-origin contact event is a point on the surface of the unit hypercircle or at the center of the hyperdisk — geometrically distinct
- **hmm:** Whether cylindrical geodesic distance, hyperspherical geodesic distance, or a product metric (disk-level + z-axis) is the right distance for BoneEmbedder
- **hmm:** The precise formal name for the new complexity at depth 3 — "variable ordering / concatenation potentiality" is a working description

**Resolved:** The system name "Unit Circle" is retained. Names are for minds to grasp.  
**Resolved:** Nested recursion is capped at depth 3. Depth 3 is only just within conceptual reach; it introduces variable ordering / concatenation potentiality. Depth 4 is not a magnitude of note. Depth 5 is the next magnitude of note but requires depth-3 mastery first.

---

**Accreditation:** GPT generated; context, prompt Erin Spencer
