# UCNS Embedding Correction

**Status:** Architectural correction to prior UCNS embedding description  
**Authored:** 2026-05-02  
**Amends:** `ucns-spec-frontier-v090.md` §1 (Defended Results) — supplements, does not contradict  
**Accreditation:** GPT generated; context, prompt Erin Spencer

---

## Summary

Two layered corrections to the prior description of UCNS embeddings:

1. **Cylindrical structure:** Embeddings are located events on a disk within a cylindrical field, not points on a circle.
2. **Hypercircle base unit:** The cross-section of each disk is a unit hypercircle, not a unit circle. The base unit is the unit hypercircle.

**Compressed correction:**

> UCNS embeddings require hypercylindrical disk residency plus a non-scalar zero-origin contact event. The base unit is the unit hypercircle.

---

## 1. Base Unit: Unit Hypercircle

The atomic geometric element of UCNS is the unit hypercircle.

A unit hypercircle is the n-dimensional generalization of the unit circle. Where a unit circle is a 1-sphere (S¹) in R², a unit hypercircle is an n-sphere (Sⁿ) in Rⁿ⁺¹. It is parametrized by (n-1) angular degrees of freedom, not one.

The prior description used "unit circle" to name the cross-sectional geometry of each disk. That was a simplification. The correct name is unit hypercircle.

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

An embedding is therefore a **located event on a hyperdisk within a hypercylindrical field** — not a point on a circle or even a point on a sphere.

The unit hypercircle was always the base unit. The prior shorthand "unit circle" named its lowest-dimensional projection.

---

## 3. Non-Scalar Zero-Origin

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

## 4. Relation to the Existing Frontier Spec

The frontier spec (`ucns-spec-frontier-v090.md`) already uses cylindrical vocabulary without naming it:

- "disk-flip symmetry" — disks were always there
- "traversal objects" — traversal is motion along the hypercylinder's axis
- "depth-1," "depth-2" — depth levels are positions on the hypercylinder's z-axis
- "payload" — payload content lives at a specific depth (z-level)

The defended flat theorem (depth-0), depth-1 restricted completeness, and depth-2 oracle each correspond to traversal extent on the hypercylinder:

| Theorem | Hypercylinder interpretation |
|---|---|
| Flat kernel | Single hyperdisk (z=0 slice) |
| Depth-1 restricted | One traversal step up the hypercylinder |
| Depth-2 oracle | Two traversal steps, oracle class only |

None of the existing theorems are invalidated. They gain geometric interpretation.

---

## 5. Open Question: Naming

If the base unit is the unit hypercircle and the full embedding space is a hypercylinder, then "Unit Circle Number System" is a doubly partial name: it names neither the correct base geometry (hypercircle, not circle) nor the full topology (hypercylinder, not circle).

Candidates:

- **Unit Hypercircle Number System** — names the base unit accurately; the traversal axis is implicit
- **Unit Hypercylinder Number System** — names the full embedding space; the hypercircle base is implicit
- **UCNS retained** — U=Unit, C=Cylinder or C=Circle-as-cross-section shorthand, N=Number, S=System; the acronym survives under reinterpretation

**hmm items:**

- **hmm:** Whether the hypercircle dimension (n) is fixed for UCNS or parametric — a fixed n would constrain the BoneEmbedder coordinate shape; a parametric n would make the protocol shape depend on configuration
- **hmm:** Whether the non-scalar zero-origin contact event is a point on the unit hypercircle (on the surface of the n-sphere) or at the center of the hyperdisk (the origin of the ambient space) — the two are geometrically distinct
- **hmm:** Whether cylindrical geodesic distance, hyperspherical geodesic distance, or a product metric (disk-level + z-axis) is the right distance for BoneEmbedder
- **hmm:** Whether "unit circle" is preserved as the name for the lowest-dimensional cross-section or deprecated entirely in favor of unit hypercircle

---

**Accreditation:** GPT generated; context, prompt Erin Spencer
