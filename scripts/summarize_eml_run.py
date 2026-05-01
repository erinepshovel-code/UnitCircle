#!/usr/bin/env python3
"""Summarize existing EML run artifacts into a handoff memo.

Useful after running in Codespaces or CI.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def read_best_metrics(path: Path) -> dict:
    if not path.exists():
        return {}
    obj = json.loads(path.read_text())
    return obj.get("best_metrics", {})


def fmt(v: object) -> str:
    if isinstance(v, float):
        return f"{v:.6g}"
    return str(v)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs-dir", default=None, help="Runs directory (auto-detects runs/ then runs_smoke/)")
    ap.add_argument("--out", default=None, help="Output markdown path (default: <runs-dir>/continuation_handoff.md)")
    args = ap.parse_args()

    if args.runs_dir:
        runs = Path(args.runs_dir)
    else:
        runs = Path("runs") if Path("runs").exists() else Path("runs_smoke")
    out = Path(args.out) if args.out else runs / "continuation_handoff.md"

    a = read_best_metrics(runs / "target_a" / "metrics.json")
    c = read_best_metrics(runs / "target_c" / "metrics.json")

    if not a and not c:
        raise SystemExit(f"No run metrics found under {runs}. Run `make run-eml` or `make run-eml-smoke` first.")

    text = f"""# Continuation Handoff (from existing run artifacts)

## Metrics snapshot
### Target A
- train_mse: {fmt(a.get('train_mse', 'n/a'))}
- val_mse: {fmt(a.get('val_mse', 'n/a'))}
- test_mse: {fmt(a.get('test_mse', 'n/a'))}
- restart: {fmt(a.get('restart', 'n/a'))}

### Target C
- train_mse: {fmt(c.get('train_mse', 'n/a'))}
- val_mse: {fmt(c.get('val_mse', 'n/a'))}
- test_mse: {fmt(c.get('test_mse', 'n/a'))}
- restart: {fmt(c.get('restart', 'n/a'))}

## Mandatory boundary object
This section is the **mandatory boundary object** that records unresolved constraints, preserves honest incompletion, and marks the transition between delivered output and living continuation.

### Unresolved constraints
- The current trainer is a lightweight baseline search procedure, not a paper-faithful gradient optimizer.
- Exact symbolic recovery has not been independently validated on these prime targets.
- Cross-seed stability and extrapolation reliability still need systematic sweeps.

### Preserved honest incompletion
This memo reports current run state, not proof of an elementary generative law for primes.

### Transition to living continuation
1. Re-run with larger restart/step budgets and compare seed consistency.
2. Add extrapolation-focused holdout ranges.
3. Upgrade to gradient training and symbolic canonicalization checks.
"""

    runs.mkdir(parents=True, exist_ok=True)
    out.write_text(text)
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
