# CLAUDE.md — UnitCircle

This file gives AI assistants context needed to work effectively in this repository.

---

## What This Repo Is

**UnitCircle** is a computational visualization and mathematical research codebase supporting a master's thesis on the distribution of prime numbers under modular projection. It maps primes onto a unit circle using residue classes (mod 360), rendering both circular and cylindrical views.

The repo also contains:
- An **EML (Emergent Machine Learning) experiment pipeline** for training decision-tree models on prime datasets
- A **UCNS flat kernel** (`scripts/ucns_flat_kernel.py`) — implementation of the Unit Circle Number System v0.3 paired-kernel
- A **Gonal-Möbius prime-basin embedding** construction
- Versioned historical artifacts of the UCNS theorem frontier

This is a **research/exploratory codebase**, not a pip-installable library. There is no formal test suite, no CI pipeline, and no package to install.

---

## Repository Layout

```
scripts/
  build_prime_datasets.py          Build Target A / Target C prime CSV datasets
  train_eml_tree.py                Train EML tree model on a dataset
  run_eml_experiment.py            Full pipeline: dataset + training + report
  summarize_eml_run.py             Generate handoff summary from run artifacts
  build_gonal_mobius_embedding.py  Gonal-Möbius prime-basin layered embedding
  ucns_flat_kernel.py              UCNS v0.3 flat paired-kernel (self-contained)

code/                              Versioned historical UCNS theorem artifacts (read-only)
  v080-coupled-witness-solver.py
  v080-recursive-factorization-refactor-plan.py
  v081-depth2-oracle-theorem.py
  v082-depth2-final-push.py
  v090-carrier-widening.py
  e109-depth2-failure-boundary.py

ucns-code-v065.py                  Stable UCNS v0.6.5 snapshot (read-only reference)
ucns-depth2-staged-engine.py       Depth-2 staged engine artifact (historical)

Primes                             Prime number dataset file
Makefile                           Make targets for EML pipeline

EML_PRIME_EXPERIMENT_PLAN.md       Experiment design plan
MANIFEST.md                        Repository manifest — what each file is
frontier/ucns-spec-frontier-v090.md  Current UCNS completeness frontier spec
ucns-embedding-correction.md       Embedding correction notes
a0_architecture.md                 a0 architecture reference
accreditation.md                   Accreditation notes
```

---

## Development Workflows

### EML Experiment Pipeline

```bash
# Quick smoke test (small params, fast)
make run-eml-smoke

# Full baseline run (1M primes, 4000 steps)
make run-eml

# Manual step-by-step
python scripts/build_prime_datasets.py \
  --x-max 1000000 --modulus 360 \
  --log-grid-points 256 --window 31 --out-dir data

python scripts/train_eml_tree.py \
  --dataset data/target_a.csv --target target_a \
  --depth 3 --restarts 10 --steps 4000 --out-dir runs

python scripts/train_eml_tree.py \
  --dataset data/target_c.csv --target target_c \
  --depth 3 --restarts 10 --steps 4000 --out-dir runs

# Möbius doubled-surface mode
python scripts/build_prime_datasets.py \
  --x-max 1000000 --modulus 360 --surface-mode mobius \
  --log-grid-points 256 --window 31 --out-dir data

python scripts/run_eml_experiment.py \
  --x-max 1000000 --modulus 360 --surface-mode mobius \
  --log-grid-points 256 --window 31 \
  --depth 3 --restarts 10 --steps 4000 \
  --data-dir data --runs-dir runs

# Generate continuation handoff report from completed run
make summarize-eml
# Writes runs/continuation_handoff.md

# Clean generated artifacts
make clean-eml-artifacts
```

### UCNS Flat Kernel (`scripts/ucns_flat_kernel.py`)

```bash
# Self-check / verify kernel
python scripts/ucns_flat_kernel.py self-check

# Build a UCNS object (theta_plus expressed in turns over 2π)
python scripts/ucns_flat_kernel.py build \
  --n-dec 6 --theta-plus "0,1/3" --face-plus "0,1"

# Multiply two UCNS objects (ordered concatenation)
python scripts/ucns_flat_kernel.py multiply \
  --a-n-dec 6 --a-theta-plus "0,1/3" --a-face-plus "0,1" \
  --b-n-dec 4 --b-theta-plus "0,1/4,1/2" --b-face-plus "1,0,1"

# Contiguous flat factor search
python scripts/ucns_flat_kernel.py factor-search \
  --n-dec 12 \
  --theta-plus "0,1/4,1/2,1/3,7/12,5/6" \
  --face-plus "1,0,1,0,1,0"
```

### Gonal-Möbius Embedding

```bash
python scripts/build_gonal_mobius_embedding.py \
  --n 29 --chi 1 \
  --epicycles "1.0:1,0.5:-1" \
  --basin-primes "3,5,7,13,29,53" \
  --tau 0.35 --max-value 500 \
  --out data/gonal_mobius_embedding.csv
```

---

## Key Concepts

- **Residue classes mod 360**: primes are mapped to unit circle positions by `p mod 360`
- **Target A / Target C**: two EML dataset targets; A = standard residue features, C = Möbius-doubled surface
- **Möbius surface mode**: residue occupancy tracked on `2 × modulus` slots with a parity twist; supports interdependency framing via `The-Interdependency/pcea`
- **UCNS flat kernel**: pairs `(theta_plus, face_plus)` — unit-circle angle sequences and face-bit sequences; supports multiply and factor-search operations
- **Gonal-Möbius layers**: (1) Gonal roots of unity, (2) Möbius `2n` spinor states, (3) Epicycle radial modulation, (4) Prime stability basin soft-assignment
- **EML tree**: Emergent Machine Learning decision-tree trained on prime-dataset features

---

## File Status

| File/Dir | Status | Notes |
|----------|--------|-------|
| `scripts/run_eml_experiment.py` | Active | Main pipeline entry point |
| `scripts/ucns_flat_kernel.py` | Active | UCNS v0.3 flat kernel |
| `scripts/build_gonal_mobius_embedding.py` | Active | Gonal-Möbius construction |
| `ucns-code-v065.py` | Read-only | Historical v0.6.5 snapshot |
| `ucns-depth2-staged-engine.py` | Read-only | Historical artifact |
| `code/` | Read-only | Versioned theorem artifacts |

Do **not** modify `ucns-code-v065.py` or anything in `code/` — they are preserved reference points.

---

## Run Artifact Layout

After running the EML pipeline, artifacts appear in:

```
data/                    # Generated CSV datasets (target_a.csv, target_c.csv)
runs/
  metrics.json           # Training metrics
  checkpoint.json        # Model checkpoint
  continuation_handoff.md  # Handoff summary (from make summarize-eml)
```

---

## What Does Not Exist

- No formal test suite
- No CI/CD pipeline
- No pip-installable package
- No external runtime dependencies documented (scripts appear to use stdlib + common scientific Python; check individual scripts for imports)

---

## Related Repos

| Repo | Role |
|------|------|
| The-Interdependency/ucns | UCNS library (packaged version of theory developed here) |
| The-Interdependency/pcea | PCEA library referenced by Möbius surface mode |
| The-Interdependency/a0 | Agent platform whose architecture is referenced in `a0_architecture.md` |

---

## Git Workflow

- Main branch: `main`
- Author: Erin Patrick Spencer (erin.eps.hovel@gmail.com)
- License: see repo (research codebase)
