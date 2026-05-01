#!/usr/bin/env python3
"""Minimal trainable EML-tree runner.

This is a lightweight baseline trainer using random-search refinement,
intended to turn the experiment plan into something executable.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import random
from dataclasses import dataclass
from pathlib import Path


EPS = 1e-9


def softplus(x: float) -> float:
    if x > 40:
        return x
    if x < -40:
        return math.exp(x)
    return math.log1p(math.exp(x))


def safe_exp(x: float) -> float:
    return math.exp(max(-40.0, min(40.0, x)))


def eml(x: float, y: float) -> float:
    return safe_exp(x) - math.log(softplus(y) + EPS)


@dataclass
class Model:
    depth: int
    leaf_params: list[tuple[float, float]]  # a,b for a*x+b
    node_params: list[tuple[float, float, float, float]]  # al,bl,ar,br

    @staticmethod
    def random(depth: int, rng: random.Random) -> "Model":
        leaves = 2**depth
        nodes = 2**depth - 1
        leaf_params = [(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(leaves)]
        node_params = [(rng.uniform(0.5, 1.5), rng.uniform(-1, 1), rng.uniform(0.5, 1.5), rng.uniform(-1, 1)) for _ in range(nodes)]
        return Model(depth, leaf_params, node_params)

    def clone(self) -> "Model":
        return Model(self.depth, self.leaf_params[:], self.node_params[:])

    def mutate(self, rng: random.Random, scale: float) -> None:
        if rng.random() < 0.5:
            i = rng.randrange(len(self.leaf_params))
            a, b = self.leaf_params[i]
            self.leaf_params[i] = (a + rng.gauss(0, scale), b + rng.gauss(0, scale))
        else:
            i = rng.randrange(len(self.node_params))
            al, bl, ar, br = self.node_params[i]
            self.node_params[i] = (
                al + rng.gauss(0, scale),
                bl + rng.gauss(0, scale),
                ar + rng.gauss(0, scale),
                br + rng.gauss(0, scale),
            )

    def predict(self, x: float) -> float:
        vals = [a * x + b for (a, b) in self.leaf_params]
        idx = 0
        while len(vals) > 1:
            nxt = []
            for i in range(0, len(vals), 2):
                l, r = vals[i], vals[i + 1]
                al, bl, ar, br = self.node_params[idx]
                idx += 1
                nxt.append(eml(al * l + bl, ar * r + br))
            vals = nxt
        return vals[0]

    def expression(self) -> str:
        nodes = [f"({a:.6g}*x+{b:.6g})" for a, b in self.leaf_params]
        idx = 0
        while len(nodes) > 1:
            nxt = []
            for i in range(0, len(nodes), 2):
                l, r = nodes[i], nodes[i + 1]
                al, bl, ar, br = self.node_params[idx]
                idx += 1
                nxt.append(f"eml({al:.6g}*{l}+{bl:.6g}, {ar:.6g}*{r}+{br:.6g})")
            nodes = nxt
        return nodes[0]


def mse(model: Model, rows: list[tuple[float, float]]) -> float:
    if not rows:
        return float("inf")
    s = 0.0
    for x, y in rows:
        yhat = model.predict(x)
        d = yhat - y
        s += d * d
    return s / len(rows)


def load_rows(path: Path) -> dict[str, list[tuple[float, float]]]:
    out = {"train": [], "val": [], "test": []}
    with path.open() as f:
        r = csv.DictReader(f)
        for row in r:
            x = float(row["x"])
            y = float(row["y"])
            split = row.get("split", "train")
            out.setdefault(split, []).append((x, y))
    # x normalization for stability
    for k, rows in out.items():
        out[k] = [(math.log10(x), y) for x, y in rows if x > 1]
    return out


def train_once(data: dict[str, list[tuple[float, float]]], depth: int, steps: int, seed: int) -> tuple[Model, dict]:
    rng = random.Random(seed)
    model = Model.random(depth, rng)
    best = model.clone()
    best_val = mse(best, data["val"])
    temp = 1.0

    for _ in range(steps):
        cand = model.clone()
        cand.mutate(rng, scale=max(0.01, temp * 0.1))
        cval = mse(cand, data["val"])
        mval = mse(model, data["val"])
        if cval < mval or rng.random() < math.exp((mval - cval) / max(1e-6, temp)):
            model = cand
            mval = cval
        if mval < best_val:
            best = model.clone()
            best_val = mval
        temp *= 0.999

    metrics = {
        "train_mse": mse(best, data["train"]),
        "val_mse": mse(best, data["val"]),
        "test_mse": mse(best, data["test"]),
    }
    return best, metrics


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", required=True)
    ap.add_argument("--target", default="target_a")
    ap.add_argument("--depth", type=int, default=3)
    ap.add_argument("--restarts", type=int, default=5)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--steps", type=int, default=4000)
    ap.add_argument("--out-dir", default="runs")
    args = ap.parse_args()

    dataset = Path(args.dataset)
    data = load_rows(dataset)

    out_dir = Path(args.out_dir) / args.target
    out_dir.mkdir(parents=True, exist_ok=True)

    best_model = None
    best_val = float("inf")
    all_metrics = []

    for i in range(args.restarts):
        seed = args.seed + i
        model, metrics = train_once(data, args.depth, args.steps, seed)
        metrics["restart"] = i
        all_metrics.append(metrics)
        if metrics["val_mse"] < best_val:
            best_val = metrics["val_mse"]
            best_model = model

    assert best_model is not None

    summary = {
        "dataset": str(dataset),
        "target": args.target,
        "depth": args.depth,
        "restarts": args.restarts,
        "best_metrics": min(all_metrics, key=lambda m: m["val_mse"]),
        "all_metrics": all_metrics,
        "expression": best_model.expression(),
    }

    (out_dir / "metrics.json").write_text(json.dumps(summary, indent=2))
    (out_dir / "checkpoint.json").write_text(
        json.dumps(
            {
                "depth": best_model.depth,
                "leaf_params": best_model.leaf_params,
                "node_params": best_model.node_params,
            },
            indent=2,
        )
    )
    print(json.dumps(summary["best_metrics"], indent=2))


if __name__ == "__main__":
    main()
