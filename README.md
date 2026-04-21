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
