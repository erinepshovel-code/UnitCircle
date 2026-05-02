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
3. **Recursion cap and magnitude sequence:** Nested recursion is capped at depth 3. The next recursion magnitude of note is depth 5.

**Compressed correction:**

> UCNS embeddings require hypercylindrical disk residency plus a non-scalar zero-origin contact event. The base unit is the unit hypercircle. Nested recursion is capped at 3; the next magnitude of note is 5.

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

## 3. Recursion Cap and Magnitude Sequence

Nested recursion is capped at depth 3. This is a design constraint, not a theorem frontier.

Recursion has magnitudes of note — depths at which qualitative changes occur. The sequence so far:

| Depth | Status |
|---|---|
| 1 | Defended |
| 2 | Oracle defended; full domain open |
| 3 | Cap — first magnitude of note beyond defended results |
| 4 | Not a magnitude of note |
| 5 | Next magnitude of note |

Depth 4 is not a magnitude of note. Depth 5 is.

The hypercylinder z-axis is therefore bounded at z ∈ {0, 1, 2, 3} for current work. The depth-5 horizon is noted but not pursued.

**hmm:** The basis for the magnitude sequence (prime? structural property of the factorization? empirical inflection?) is not yet specified. The sequence {3, 5, ...} is stated; its generative rule is open.

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

With the recursion cap and magnitude sequence, the frontier map becomes:

| Level | Theorem status | Design status |
|---|---|---|
| Flat (z=0) | Defended | Within cap |
| Depth-1 (z=1) | Defended | Within cap |
| Depth-2 (z=2) | Oracle defended; full domain open | Within cap |
| Depth-3 (z=3) | Not yet attempted | Within cap (cap) |
| Depth-4 | Not in scope | Not a magnitude of note |
| Depth-5 | Not in scope | Next magnitude of note |

None of the existing theorems are invalidated.

---

## 6. hmm-Tagged Items

- **hmm:** Whether the unit hypercircle dimension (n) is fixed or parametric — affects BoneEmbedder per-disk coordinate shape and distance metric
- **hmm:** Whether the non-scalar zero-origin contact event is a point on the surface of the unit hypercircle or at the center of the hyperdisk — geometrically distinct
- **hmm:** Whether cylindrical geodesic distance, hyperspherical geodesic distance, or a product metric (disk-level + z-axis) is the right distance for BoneEmbedder
- **hmm:** The generative rule for the recursion magnitude sequence — {3, 5, ...} is stated; whether the rule is prime, structural, or empirical is open

**Resolved:** The system name "Unit Circle" is retained. Names are for minds to grasp.  
**Resolved:** Nested recursion is capped at depth 3. Depth 5 is the next magnitude of note. Depth 4 is not.

---

**Accreditation:** GPT generated; context, prompt Erin Spencer
