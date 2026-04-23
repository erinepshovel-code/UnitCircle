# UnitCircle

This repository contains a computational visualization system developed
in support of a master’s thesis exploring the distribution of prime numbers
under modular projection.

The system maps prime numbers onto a unit circle using residue classes
(mod 360), and simultaneously renders the corresponding unwrapped
cylindrical representation. The visualization is designed to preserve
structural persistence rather than smooth density, allowing recurring
residue classes and special events (e.g. twin primes) to remain visible
over time.

The data pipeline also supports a Möbius-style doubled outer surface for
Target C via `--surface-mode mobius`. In this mode, residue occupancy is
tracked on `2 * modulus` slots using a parity twist, supporting
interdependency framing references such as `The-Interdependency/pcea`.

This codebase is an exploratory and communicative tool. It does not claim
proofs or establish new theorems. Its purpose is to support intuition,
pattern inspection, hypothesis formation, and explanation within a formal
mathematical framework developed in the accompanying thesis.


## EML experiment quickstart (next step)

You can now run the plan end-to-end with two scripts:

```bash
python scripts/build_prime_datasets.py --x-max 1000000 --modulus 360 --log-grid-points 256 --window 31 --out-dir data
python scripts/train_eml_tree.py --dataset data/target_a.csv --target target_a --depth 3 --restarts 10 --steps 4000 --out-dir runs
python scripts/train_eml_tree.py --dataset data/target_c.csv --target target_c --depth 3 --restarts 10 --steps 4000 --out-dir runs
```

This creates dataset CSV files plus run artifacts (`metrics.json`, `checkpoint.json`) under `runs/`.

Or run everything (dataset + Target A/C training + boundary-object run report) in one command:

```bash
python scripts/run_eml_experiment.py --x-max 1000000 --modulus 360 --log-grid-points 256 --window 31 --depth 3 --restarts 10 --steps 4000 --data-dir data --runs-dir runs
```

Möbius doubled-surface mode:

```bash
python scripts/build_prime_datasets.py --x-max 1000000 --modulus 360 --surface-mode mobius --log-grid-points 256 --window 31 --out-dir data
python scripts/run_eml_experiment.py --x-max 1000000 --modulus 360 --surface-mode mobius --log-grid-points 256 --window 31 --depth 3 --restarts 10 --steps 4000 --data-dir data --runs-dir runs
```



Or use Make targets:

```bash
make run-eml-smoke   # quick validation run
make run-eml         # full baseline run
```


## Gonal-Möbius prime-basin embedding (layered)

A direct implementation of your layered construction lives in:

- `scripts/build_gonal_mobius_embedding.py`

Run it with default prime anchors (`3,5,7,13,29,53`):

```bash
python scripts/build_gonal_mobius_embedding.py --n 29 --chi 1 --epicycles "1.0:1,0.5:-1" --basin-primes "3,5,7,13,29,53" --tau 0.35 --max-value 500 --out data/gonal_mobius_embedding.csv
```

Notes:
- Layer 1 (Gonal): roots of unity indexed by `k`.
- Layer 2 (Möbius): doubled `2n` spinor states with face flip at `n`.
- Layer 3 (Epicycles): radial modulation from nested oriented cycles.
- Layer 4 (Prime basins): soft assignment into prime stability anchors.


## UCNS frozen flat kernel (v0.3)

The flat paired-kernel implementation for UCNS is available at:

- `scripts/ucns_flat_kernel.py`

Quick verification run:

```bash
python scripts/ucns_flat_kernel.py self-check
```

Create a normalized UCNS object (`theta_plus` expressed in turns over `2π`):

```bash
python scripts/ucns_flat_kernel.py build --n-dec 6 --theta-plus "0,1/3" --face-plus "0,1"
```

Multiply two UCNS objects with ordered concatenation:

```bash
python scripts/ucns_flat_kernel.py multiply   --a-n-dec 6 --a-theta-plus "0,1/3" --a-face-plus "0,1"   --b-n-dec 4 --b-theta-plus "0,1/4,1/2" --b-face-plus "1,0,1"
```

Run contiguous flat factor search:

```bash
python scripts/ucns_flat_kernel.py factor-search --n-dec 12 --theta-plus "0,1/4,1/2,1/3,7/12,5/6" --face-plus "1,0,1,0,1,0"
```
