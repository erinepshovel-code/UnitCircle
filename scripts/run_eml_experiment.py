#!/usr/bin/env python3
"""One-command runner for the EML prime experiment baseline.

It orchestrates:
1) dataset build
2) Target A training
3) Target C training
4) boundary-object report generation
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str]) -> None:
    print("$", " ".join(cmd))
    subprocess.run(cmd, check=True)


def load_best_metrics(path: Path) -> dict:
    if not path.exists():
        return {}
    obj = json.loads(path.read_text())
    return obj.get("best_metrics", {})


def write_boundary_report(out_path: Path, args: argparse.Namespace, a: dict, c: dict) -> None:
    text = f"""# EML Prime Baseline Run Report

## Run configuration
- x_max: {args.x_max}
- modulus: {args.modulus}
- log_grid_points: {args.log_grid_points}
- window: {args.window}
- depth: {args.depth}
- restarts: {args.restarts}
- steps: {args.steps}

## Result snapshot
### Target A (smoothed prime counting)
- train_mse: {a.get('train_mse', 'n/a')}
- val_mse: {a.get('val_mse', 'n/a')}
- test_mse: {a.get('test_mse', 'n/a')}

### Target C (mod-residue anisotropy)
- train_mse: {c.get('train_mse', 'n/a')}
- val_mse: {c.get('val_mse', 'n/a')}
- test_mse: {c.get('test_mse', 'n/a')}

## Mandatory boundary object
This section is the **mandatory boundary object** that records unresolved constraints, preserves honest incompletion, and marks the transition between delivered output and living continuation.

### Unresolved constraints
- The current trainer is a lightweight baseline search loop; it is not yet a paper-faithful gradient pipeline with symbolic snapping.
- Exact-recovery claims remain unverified for these prime targets.
- Hyperparameter sensitivity and restart consistency need larger sweeps.

### Preserved honest incompletion
This report is an execution checkpoint, not a proof of compact elementary generative laws for primes.

### Transition to living continuation
Next actions:
1. Replace baseline search with true gradient optimization and canonical extraction checks.
2. Add extrapolation split beyond training horizon.
3. Add repeated-seed consistency and complexity-score tracking.
"""
    out_path.write_text(text)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--x-max", type=int, default=1_000_000)
    ap.add_argument("--modulus", type=int, default=360)
    ap.add_argument("--log-grid-points", type=int, default=256)
    ap.add_argument("--window", type=int, default=31)
    ap.add_argument("--depth", type=int, default=3)
    ap.add_argument("--restarts", type=int, default=10)
    ap.add_argument("--steps", type=int, default=4000)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--data-dir", default="data")
    ap.add_argument("--runs-dir", default="runs")
    args = ap.parse_args()

    py = sys.executable

    run(
        [
            py,
            "scripts/build_prime_datasets.py",
            "--x-max",
            str(args.x_max),
            "--modulus",
            str(args.modulus),
            "--log-grid-points",
            str(args.log_grid_points),
            "--window",
            str(args.window),
            "--out-dir",
            args.data_dir,
        ]
    )

    run(
        [
            py,
            "scripts/train_eml_tree.py",
            "--dataset",
            f"{args.data_dir}/target_a.csv",
            "--target",
            "target_a",
            "--depth",
            str(args.depth),
            "--restarts",
            str(args.restarts),
            "--steps",
            str(args.steps),
            "--seed",
            str(args.seed),
            "--out-dir",
            args.runs_dir,
        ]
    )

    run(
        [
            py,
            "scripts/train_eml_tree.py",
            "--dataset",
            f"{args.data_dir}/target_c.csv",
            "--target",
            "target_c",
            "--depth",
            str(args.depth),
            "--restarts",
            str(args.restarts),
            "--steps",
            str(args.steps),
            "--seed",
            str(args.seed + 1000),
            "--out-dir",
            args.runs_dir,
        ]
    )

    a_metrics = load_best_metrics(Path(args.runs_dir) / "target_a" / "metrics.json")
    c_metrics = load_best_metrics(Path(args.runs_dir) / "target_c" / "metrics.json")

    report = Path(args.runs_dir) / "boundary_object_report.md"
    report.parent.mkdir(parents=True, exist_ok=True)
    write_boundary_report(report, args, a_metrics, c_metrics)
    print(f"Wrote report: {report}")


if __name__ == "__main__":
    main()
