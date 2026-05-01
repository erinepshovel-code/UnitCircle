"""
ucns.factorization (EXPERIMENTAL)
=================================
v0.8.0-staged-factorization-experiment (variant 2)

EXPERIMENTAL BRANCH ARTIFACT — NOT CANONICAL
DO NOT MERGE INTO MAIN / ucns/ PACKAGE YET

This is a second experimental variant of the staged factorization engine,
with E10-style host enumeration and RIO-style coupled payload equation matrix.

Placement rule (per maintainer):
- Track as code/v080-staged-factorization-experiment-2.py
- Must pass the same frozen benchmark envelope that v0.8.2 / v0.9.0 failed
  before any frontier update is considered.

Accreditation: Built from context in ucns-spec-frontier-v090.md + ucns-code-v065.py
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Optional, List, Tuple

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from ucns.core import UCN, TAU

__all__ = [
    "UCNSObject",
    "WitnessMatrix",
    "StagedFactorSearch",
    "factor_search",
    "multiply",
    "left_quotient",
]


@dataclass
class UCNSObject:
    A_plus: List[Tuple[UCN, Optional["UCNSObject"]]]
    F_plus: List[int] = field(default_factory=lambda: [0])
    n_min: int = 1

    def __post_init__(self):
        if not self.A_plus:
            self.A_plus = [(UCN(0.0), None)]
        if len(self.F_plus) != len(self.A_plus):
            self.F_plus = [0] * len(self.A_plus)

    def depth(self) -> int:
        if not self.A_plus or self.A_plus[0][1] is None:
            return 1
        return 1 + max(p.depth() if p else 1 for _, p in self.A_plus)

    def is_atomic(self) -> bool:
        return all(payload is None for _, payload in self.A_plus)

    def __repr__(self) -> str:
        return f"UCNSObject(A_plus={len(self.A_plus)}, depth={self.depth()}, n_min={self.n_min})"


@dataclass
class WitnessMatrix:
    local_consistent: bool = True
    global_consistent: bool = True
    host_recovered: bool = False
    payload_built: bool = False
    depth: int = 0
    notes: List[str] = field(default_factory=list)
    matrix_size: Tuple[int, int] = (0, 0)
    recovered_host: Optional[UCNSObject] = None
    local_equations: List[str] = field(default_factory=list)
    quotient_witnesses: dict = field(default_factory=dict)
    global_flags: dict = field(default_factory=dict)

    def is_valid(self) -> bool:
        return (self.local_consistent and self.global_consistent and
                self.host_recovered and self.payload_built and
                all(self.global_flags.values()))

    def add_note(self, note: str) -> None:
        self.notes.append(note)

    def mark_global_consistent(self, size: Tuple[int, int]):
        self.global_consistent = True
        self.matrix_size = size
        self.global_flags["reconstruction"] = True
        self.add_note("Global witness matrix fully consistent (RIO)")


def multiply(A: UCNSObject, B: UCNSObject) -> UCNSObject:
    new_A_plus: List[Tuple[UCN, Optional[UCNSObject]]] = []
    new_F_plus: List[int] = []
    for (alpha, payloadA), fa in zip(A.A_plus, A.F_plus):
        for (beta, payloadB), fb in zip(B.A_plus, B.F_plus):
            new_angle = UCN((alpha.theta + beta.theta) % TAU)
            new_payload = None
            if payloadA is not None and payloadB is not None:
                new_payload = multiply(payloadA, payloadB)
            elif payloadA is not None:
                new_payload = payloadA
            elif payloadB is not None:
                new_payload = payloadB
            new_face = fa ^ fb
            new_A_plus.append((new_angle, new_payload))
            new_F_plus.append(new_face)
    return UCNSObject(new_A_plus, new_F_plus, n_min=max(A.n_min, B.n_min))


def left_quotient(P: UCNSObject, A: UCNSObject, catalogue: List[UCNSObject]) -> Optional[UCNSObject]:
    for B_cand in catalogue:
        if _objects_equal(multiply(A, B_cand), P):
            return B_cand
    return None


def right_quotient(P: UCNSObject, B: UCNSObject, catalogue: List[UCNSObject]) -> Optional[UCNSObject]:
    for A_cand in catalogue:
        if _objects_equal(multiply(A_cand, B), P):
            return A_cand
    return None


def _objects_equal(a: UCNSObject, b: UCNSObject) -> bool:
    if len(a.A_plus) != len(b.A_plus):
        return False
    for (aa, pa), (bb, pb) in zip(a.A_plus, b.A_plus):
        if abs(aa.theta - bb.theta) > 1e-9:
            return False
        if (pa is None) != (pb is None):
            return False
        if pa is not None and pb is not None and not _objects_equal(pa, pb):
            return False
    return True


class StagedFactorSearch:
    def __init__(self, catalogue=None):
        self.catalogue = catalogue or self._build_frozen_catalogue()
        self._witness = None

    def _build_frozen_catalogue(self):
        s1 = UCNSObject([(UCN(0.0), None)], [0], n_min=1)
        s2 = UCNSObject([(UCN(0.5), s1)], [1], n_min=2)
        s3 = UCNSObject([(UCN(1.0), s2)], [0], n_min=4)
        s2b = UCNSObject([(UCN(0.25), s1), (UCN(0.75), None)], [1, 0], n_min=3)
        s3b = UCNSObject([(UCN(0.33), s2), (UCN(0.66), s1), (UCN(0.99), None)], [0, 1, 0], n_min=4)
        return [s1, s2, s3, s2b, s3b]

    def _recover_host(self, P):
        n = len(P.A_plus)
        best_candidate, best_score = None, -1
        for A_cand in self.catalogue:
            for B_cand in self.catalogue:
                try:
                    reconstructed = multiply(A_cand, B_cand)
                    if len(reconstructed.A_plus) != n:
                        continue
                    angle_score = sum(1.0 - abs(ra.theta - pa.theta) / TAU
                                      for (ra, _), (pa, _) in zip(reconstructed.A_plus, P.A_plus)) / n
                    face_score = sum(1.0 if ra == pa else 0.0
                                     for ra, pa in zip(reconstructed.F_plus, P.F_plus)) / n
                    total_score = 0.6 * angle_score + 0.4 * face_score
                    if total_score > best_score:
                        best_score, best_candidate = total_score, reconstructed
                except Exception:
                    continue
        if best_candidate and best_score > 0.7:
            self._witness.host_recovered = True
            self._witness.add_note(f"Phase 1: Host recovered (score={best_score:.2f})")
            return best_candidate
        return None

    def _build_payload_equation_system(self, host, P):
        if P.is_atomic():
            wm = WitnessMatrix(local_consistent=True, payload_built=True, depth=1)
            wm.add_note("Phase 2: Atomic")
            return host, wm
        equations = [f"P[{i},{j}] = {ha.theta:.3f} ⊠ payload_{j}"
                     for i, (ha, _) in enumerate(host.A_plus)
                     for j, _ in enumerate(P.A_plus)]
        sub_engine = StagedFactorSearch(self.catalogue)
        payload_obj = P.A_plus[0][1]
        sub_result = sub_engine.factorize(payload_obj) if payload_obj else None
        if sub_result is None:
            return None
        factor_A, factor_B, sub_wm = sub_result
        wm = WitnessMatrix(
            local_consistent=sub_wm.local_consistent, global_consistent=True,
            host_recovered=True, payload_built=True, depth=host.depth() + 1,
            matrix_size=(len(host.A_plus), len(P.A_plus)), local_equations=equations
        )
        wm.add_note("Phase 2: Coupled payload equation matrix built (RIO)")
        new_host = UCNSObject([(host.A_plus[0][0], factor_A)], host.F_plus, host.n_min)
        return new_host, wm

    def _verify_globally(self, A, B, P, wm):
        reconstructed = multiply(A, B)
        if not _objects_equal(reconstructed, P):
            wm.global_consistent = False
            wm.add_note("Phase 3 FAILED: multiply(A,B) ≠ P")
            return False
        wm.mark_global_consistent((len(A.A_plus), len(B.A_plus)))
        wm.add_note("Phase 3 PASSED")
        return True

    def factorize(self, P):
        self._witness = WitnessMatrix(depth=P.depth())
        host = self._recover_host(P)
        if host is None:
            return None
        result = self._build_payload_equation_system(host, P)
        if result is None:
            return None
        new_host, wm = result
        A = new_host
        B = P.A_plus[0][1] if P.A_plus[0][1] else UCNSObject([(UCN(0.0), None)])
        if not self._verify_globally(A, B, P, wm):
            return None
        wm.depth = P.depth()
        self._witness = wm
        return A, B, wm

    def factor_search(self, P):
        result = self.factorize(P)
        if result is None:
            return None
        A, B, _ = result
        return A, B


def factor_search(P, catalogue=None):
    return StagedFactorSearch(catalogue).factor_search(P)


def multiply_objects(A, B):
    return multiply(A, B)


if __name__ == "__main__":
    print("=== v0.8.0 Staged Factorization Experiment (variant 2) ===\n")
    s1 = UCNSObject([(UCN(0.0), None)], [0], n_min=1)
    s2 = UCNSObject([(UCN(0.5), s1)], [1], n_min=2)
    engine = StagedFactorSearch()
    result = engine.factorize(s2)
    if result:
        A, B, wm = result
        print("✓ Staged factorization succeeded")
        print(f"  Witness valid: {wm.is_valid()}")
    else:
        print("✗ Factorization failed")
