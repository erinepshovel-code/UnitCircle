# UCNS Embedding Correction

**Status:** Architectural correction to prior UCNS embedding description  
**Authored:** 2026-05-02  
**Amends:** `ucns-spec-frontier-v090.md` §1 (Defended Results) — supplements, does not contradict  
**Accreditation:** GPT generated; context, prompt Erin Spencer

---

## Summary

The prior shorthand for UCNS described embeddings as points on a unit circle. That description captures only one cross-section of the actual topology. This document corrects the full geometric picture.

**Compressed correction:**

> UCNS embeddings require cylindrical disk residency plus a non-scalar zero-origin contact event.

---

## 1. Disk Residency

UCNS resides on disks stacked along a cylinder.

A single disk gives the unit-circle cross-section:

- angular position
- residue
- rotation
- chirality
- local relation

The cylinder gives persistence:

- sequence
- depth
- recurrence
- phase memory
- traversal across disks

An embedding is therefore a **located event on a disk within a cylindrical field** — not a point on a circle.

The circle was always one cross-section of the fundamental object. The cylinder is the fundamental object.

---

## 2. Non-Scalar Zero-Origin

Zero is not a scalar value.

Zero is the non-scalar origin point of the initial vector: the place where the writing instrument first touches paper.

Before magnitude, before direction, before digit, before mark — there is contact.

That contact is zero.

In UCNS, zero is therefore not "nothing." It is the first anchoring event from which vector, angle, motion, inscription, and number become possible.

On the cylinder, this contact event anchors at the base: `(z=0, θ=0)`. The cylinder's structure makes this natural — the cylinder has a base and an axis direction, where a closed circle has neither. The circle, taken alone, has no privileged origin point (it is rotationally symmetric). The cylinder has one.

This means:

- The bone embedding for an empty or baseline state is **not a zero vector**
- It is a **contact-event representation** at the cylinder's base
- Initialization semantics for any BoneEmbedder implementation must respect this

---

## 3. Relation to the Existing Frontier Spec

The frontier spec (`ucns-spec-frontier-v090.md`) already uses cylindrical vocabulary without naming it:

- "disk-flip symmetry" — disks were always there
- "traversal objects" — traversal is motion along the cylinder's axis
- "depth-1," "depth-2" — depth levels are positions on the cylinder's z-axis
- "payload" — payload content lives at a specific depth (z-level)

The defended flat theorem (depth-0), depth-1 restricted completeness, and depth-2 oracle each correspond to traversal extent on the cylinder:

| Theorem | Cylinder interpretation |
|---|---|
| Flat kernel | Single-disk (z=0 slice) |
| Depth-1 restricted | One traversal step up the cylinder |
| Depth-2 oracle | Two traversal steps, oracle class only |

None of the existing theorems are invalidated. They gain geometric interpretation.

---

## 4. hmm-Tagged Items

- **hmm:** Whether the name "Unit Circle Number System" should be updated to "Unit Cylinder Number System" now that the cylinder is identified as the fundamental object — the circle remains the cross-sectional geometry of each disk, but "circle" as a name for the whole system undersells the topology
- **hmm:** Whether the non-scalar zero-origin contact event has algebraic consequences for the identity element and additive structure that require revisiting prior proofs
- **hmm:** Whether cylindrical geodesic distance is the right metric for BoneEmbedder, or whether disk-level distance (within a single cross-section) and inter-disk distance (along the z-axis) should be exposed separately

---

**Accreditation:** GPT generated; context, prompt Erin Spencer
