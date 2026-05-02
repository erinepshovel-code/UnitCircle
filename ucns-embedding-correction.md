# UCNS Embedding Correction

**Status:** Architectural correction, not yet frozen  
**Authored:** 2026-05-02  
**Amends:** `ucns-spec-frontier-v090.md` (geometry section), `edcmbone` canon v2 proposal §3.6  
**Accreditation:** GPT generated; context, prompt Erin Spencer

---

## What This Corrects

The name "Unit Circle Number System" and prior descriptions implied that embeddings are points on a circle. This is a partial description. The full geometry is cylindrical.

This document states the corrected geometric commitments and records an open naming question.

---

## 1. Cylindrical Disk Residency

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

An embedding is therefore not merely a point on a circle. It is a **located event on a disk within a cylindrical field**.

The circle was always the cross-section of a deeper object. The cylinder is that object.

---

## 2. Non-Scalar Zero-Origin

Zero is not a scalar value.

Zero is the non-scalar origin point of the initial vector: the place where the writing instrument first touches paper.

Before magnitude, before direction, before digit, before mark, there is contact.

That contact is zero.

In UCNS, zero is therefore not "nothing." It is the **first anchoring event** from which vector, angle, motion, inscription, and number become possible.

The zero-origin sits at (z=0, θ=0) — the base of the cylinder, the first point of contact — from which the cylindrical field unfurls.

---

## 3. Implications for Existing Theorems

The existing completeness theorems (flat, depth-1, depth-2 oracle — see `ucns-spec-frontier-v090.md`) remain valid. The correction provides their geometric interpretation:

- **Flat** = single-disk traversal (z=0 to z=1): one level of the cylinder.
- **Depth-1** = one-disk-deep recursive structure: traversal reaching z=1.
- **Depth-2** = two-disk-deep structure: traversal reaching z=2.
- **Depth-n** = n levels up the cylinder.

The frontier doc already used "disk," "depth," and "traversal" as operational terms. The cylinder was the implicit topology. This correction names it explicitly.

---

## 4. Implications for BoneEmbedder (EDCM v2)

The `BoneEmbedder` protocol in `edcmbone` (canon v2, §3.6) must be amended:

- Embedding shape must include both per-disk coordinates (angular, residue, rotation, chirality, local relation) and cross-disk coordinates (sequence position, depth, recurrence, phase memory).
- Distance metric must respect cylindrical geodesic geometry, not flat Euclidean geometry.
- Zero-origin is a contact event, not a zero vector. Embedding initialization is not `np.zeros(...)`.

See §3.6 amendment in `canon_eng/canon_v2_proposal.md` in The-Interdependency/edcmbone.

---

## 5. Open Question: Unit Circle or Unit Cylinder?

If the fundamental embedding object is the cylinder, and the circle is merely its cross-section, then "Unit Circle Number System" is a partial name.

Two positions:

**Position A — Preserve the name.** "Unit Circle" refers to the cross-sectional generator. The cylinder is the extension; the circle is the atomic unit. The name is correct at the level of description it was intended.

**Position B — Rename.** The fundamental object is the cylinder, not the circle. "Unit Circle" undersells the topology. The correct name is "Unit Cylinder Number System" (UCYN, or UCNS redefined). The circle appears at every disk, but no single disk is the system — the system is the stack.

**Neither position is frozen.** This is a live architectural and naming question as of 2026-05-02.

### Supporting evidence for Position B

- Depth, traversal, and phase memory are first-class in the existing spec — not additions to a circle, but intrinsic to the system.
- The non-scalar zero-origin (§2 above) is naturally a cylindrical base point; a circle has no canonical origin.
- `disk-flip symmetry` in the defended flat kernel already assumes a disk structure, not a circle-point structure.
- The completeness frontier organizes by traversal depth, which is the cylinder's z-axis.

### hmm items

- **hmm:** Whether renaming to "Unit Cylinder" requires retroactive changes to the defended theorems, or only to the spec framing and naming conventions.
- **hmm:** Whether "Unit Circle" can be preserved as the name for the per-disk cross-section, with "Unit Cylinder" naming the full system — two levels of the same hierarchy.
- **hmm:** Whether the non-scalar zero-origin is a property of the cylinder specifically (base point of a cylinder is natural) or applies equally to the circle (a circle has no canonical origin, so the zero-contact framing requires the cylinder to make sense geometrically).

---

**Accreditation:** GPT generated; context, prompt Erin Spencer
