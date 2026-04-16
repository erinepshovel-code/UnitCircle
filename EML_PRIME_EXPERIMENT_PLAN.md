# Next Layer: Toy EML-Tree Experiment for Prime Geometry Discovery

This document lays out a practical, falsifiable toy experiment that follows the EML-tree bonus direction: use a *uniform differentiable symbolic grammar* to probe whether compact elementary laws can explain prime-derived structure.

## 1) Objective

Build a minimal experiment that answers three questions:

1. Can an EML tree recover known smooth approximations related to primes (sanity check)?
2. Does the same setup find compact expressions for structured-but-irregular prime observables (stress test)?
3. When it fails, can we clearly separate "model class limitation" from "no simple elementary law present"?


## 2) Paper-grounded spec lock (so we are training the *actual* EML setup)

### 2.1 Bibliographic lock
- **Paper**: Andrzej Odrzywołek, *All elementary functions from a single operator*.
- **License**: CC BY 4.0.
- **Version/date**: `arXiv:2603.21852v2 [cs.SC]`, April 4, 2026.
- **Companion artifact**: Zenodo DOI `10.5281/zenodo.19183008`.
- **Code tag**: `VA00/SymbolicRegressionPackage` @ `v1.0`.

### 2.2 Mathematical lock
Before implementing scripts, pin the exact assumptions from the paper and companion code:

- **Operator**: \(\mathrm{eml}(x,y)=e^x-\ln(y)\).
- **Grammar**: \(S \to 1 \mid \mathrm{eml}(S,S)\), i.e., one uniform binary tree family.
- **Computational domain**: the paper explicitly works over complex numbers with principal branch conventions where needed.
- **Constant role**: terminal `1` is distinguished because \(\ln(1)=0\) neutralizes the log branch.
- **Claimed SR behavior**: gradient-based training (Adam) can recover exact closed-form elementary expressions for some generated targets at shallow depth (reported up to depth 4).

### 2.3 Spec checks you must run before modeling primes

1. **Branch/domain check**: document whether your training code uses real-only data, complex arithmetic, or a constrained real surrogate for \(\ln(y)\).
2. **Domain safety check**: if real-only, specify how positivity of the second input branch is enforced (reparameterization, softplus, clipping, etc.).
3. **Constant handling check**: verify how constants beyond `1` are represented/recovered in trainable trees.
4. **Extraction check**: verify simplification + canonicalization rules used to declare “exact recovery.”
5. **Depth check**: reproduce at least one paper-style toy recovery at depth 3 or 4 before prime targets.

If any of these are unclear, stop and mark the run **non-comparable** to the paper claims.

## 3) Candidate Targets (in increasing difficulty)

### Target A — Smoothed prime counting baseline
- **Data**: pairs \((x, y)\) with \(y = \pi(x)\) or normalized variants.
- **Recommended transformed target**: \(y = \pi(x) / (x / \log x)\), which is closer to 1 and easier to fit.
- **Purpose**: verify optimization stability and symbolic compression on a classic prime quantity.

### Target B — First-order gap trend
- **Data**: prime gaps \(g_n = p_{n+1}-p_n\) and a smoothed statistic such as local moving average \(\bar g(x)\).
- **Recommended transformed target**: \(\bar g(x)/\log x\).
- **Purpose**: evaluate if EML trees discover known logarithmic scaling behavior without hard-coding it.

### Target C — Mod-residue occupancy dynamics (closest to your unit-circle geometry)
- **Data**: for modulus \(m=360\), cumulative occupancy per residue class among primes up to \(x\).
- **Derived observables**:
  - entropy over admissible residue classes,
  - anisotropy score (max minus mean occupancy),
  - twin-prime co-hit indicators by residues.
- **Purpose**: bridge symbolic regression directly to your geometric representation.

## 4) EML-Tree Training Protocol

### Parameterization concept
Use one fixed-depth binary EML tree with trainable node parameters (and optional trainable leaf scalars). Keep architecture fixed across targets.

### Depth schedule
- Start depth = 3 (fast diagnostics).
- Increase to depth = 4 only if validation plateaus.
- Depth = 5 only for residue-geometry tasks.

### Loss
Use a robust composite objective:
- primary: MSE on normalized target,
- + sparsity/complexity penalty (encourage symbolic compressibility),
- + optional derivative regularization for smooth targets.

### Optimization
- Adam with cosine decay or step decay.
- 5–10 random restarts per target.
- Early stopping on validation loss and expression stability.

## 5) Expression Extraction & Verification

After convergence:
1. prune near-zero/identity-equivalent parameters,
2. simplify algebraically,
3. fit constants at high precision,
4. re-evaluate on held-out ranges significantly beyond training window.

Success criterion is not only low error but **cross-range stability** and **symbolic compactness**.

## 6) Falsification-Focused Evaluation

For each target, report:
- in-range error (train/val/test split),
- extrapolation error (e.g., train up to \(10^6\), test to \(10^7\) if feasible),
- expression complexity score,
- restart consistency (how often equivalent forms recur).

Interpretation matrix:
- **Low error + compact + stable extrapolation** → plausible elementary skeleton.
- **Low error + high complexity + unstable extrapolation** → interpolation artifact.
- **Persistent high error at increasing depth** → likely no low-complexity elementary form (for that observable).

## 7) Concrete Minimal Run (recommended first pass)

1. Generate primes up to \(10^6\).
2. Build dataset for Target A: \(x\mapsto \pi(x)/(x/\log x)\) on logarithmically spaced \(x\).
3. Train depth-3 EML tree with 10 restarts.
4. Extract/simplify best expression.
5. Extrapolation test on \([10^6, 5\times10^6]\).
6. Repeat for Target C anisotropy score at modulus 360.

This gives a quick read on both classical smooth behavior and your geometry-linked observable.

## 8) Why this aligns with “prime geometry” language

Your geometry thesis concerns persistent residue structures rather than one-shot density fitting. This protocol targets exactly that by training on *geometric invariants* derived from residue evolution (entropy/anisotropy/twin co-hit fields), then asking whether a compact elementary dynamic appears.

In other words: it operationalizes “prime geometry as an attractor” into a learnable and falsifiable symbolic workflow.

## 9) Honest boundaries (mandatory boundary object: unresolved constraints + honest incompletion + living continuation handoff)

This section is the **mandatory boundary object**: it records unresolved constraints, preserves honest incompletion, and marks the transition between delivered output and living continuation.

### Unresolved constraints
- We now have the operator/grammar spec, but still need implementation-level extraction and canonicalization details from the reference code path.
- The phrase “exact recovery” is target-dependent; for noisy/discrete prime observables, exact symbolic recovery may be impossible even if useful structure exists.
- Computational budget will determine reachable depth/restarts, which strongly affects discovery probability.

### Preserved incompletion
This plan is a rigorous scaffold, not a proof that primes admit compact elementary generative laws. Negative outcomes are informative and expected in some targets.

### Transition to living continuation
Next concrete step is to implement a reproducible script pair:
- `scripts/build_prime_datasets.py`
- `scripts/train_eml_tree.py`

Then run the minimal pass in Section 7 and decide whether to escalate depth or redesign observables.

## 10) What to do with this right now (operator checklist)

1. **Create dataset builder (`scripts/build_prime_datasets.py`)**
   - Inputs: `--x-max`, `--modulus`, `--log-grid-points`, `--window`.
   - Outputs (CSV/Parquet): Target A/B/C tables with train/val/test splits.
2. **Create trainer (`scripts/train_eml_tree.py`)**
   - Inputs: dataset path + target name + depth + restarts + seed.
   - Outputs: best checkpoint, extracted symbolic form, metrics JSON.
3. **Run first baseline**
   - Target A, depth 3, 10 restarts, train to \(10^6\), test to \(5\times10^6\).
4. **Run geometry probe**
   - Target C anisotropy (mod 360), depth 3 then 4 if plateau.
5. **Write one-page run report**
   - Include: error table, extrapolation plot, complexity score, restart consistency.
   - Decide go/no-go for depth 5 or observable redesign.

If you want, the immediate next deliverable can be the two scripts plus a single command-line entrypoint so this plan becomes executable end-to-end.
