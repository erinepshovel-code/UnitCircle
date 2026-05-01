"""
ucns.factorization (EXPERIMENTAL)
=================================
v0.8.0-staged-factorization-experiment

EXPERIMENTAL BRANCH ARTIFACT — NOT CANONICAL
DO NOT MERGE INTO MAIN / ucns/ PACKAGE YET

Version 1: Uses relative import (from .core import UCN, TAU)
For use as part of the ucns/ package.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Optional, List, Tuple

from .core import UCN, TAU

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

    def is_valid(self) -> bool:
        return (self.local_consistent and
                self.global_consistent and
                self.host_recovered and
                self.payload_built)

    def add_note(self, note: str) -> None:
        self.notes.append(note)


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
        prod = multiply(A, B_cand)
        if _objects_equal(prod, P):
            return B_cand
    return None


def right_quotient(P: UCNSObject, B: UCNSObject, catalogue: List[UCNSObject]) -> Optional[UCNSObject]:
    for A_cand in catalogue:
        prod = multiply(A_cand, B)
        if _objects_equal(prod, P):
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
    def __init__(self, catalogue: Optional[List[UCNSObject]] = None):
        self.catalogue = catalogue or self._build_frozen_catalogue()
        self._witness: Optional[WitnessMatrix] = None

    def _build_frozen_catalogue(self) -> List[UCNSObject]:
        s1 = UCNSObject([(UCN(0.0), None)], [0], n_min=1)
        s2 = UCNSObject([(UCN(0.5), s1)], [1], n_min=2)
        s3 = UCNSObject([(UCN(1.0), s2)], [0], n_min=4)
        return [s1, s2, s3]

    def _recover_host(self, P: UCNSObject) -> Optional[UCNSObject]:
        for cand in self.catalogue:
            if len(cand.A_plus) == len(P.A_plus):
                match = True
                for (ca, _), (pa, _) in zip(cand.A_plus, P.A_plus):
                    if abs(ca.theta - pa.theta) > 1e-9:
                        match = False
                        break
                if match:
                    self._witness.host_recovered = True
                    return cand
        return None

    def _build_payload_system(self, host: UCNSObject, P: UCNSObject) -> Optional[Tuple[UCNSObject, WitnessMatrix]]:
        if P.is_atomic():
            wm = WitnessMatrix(local_consistent=True, payload_built=True, depth=1)
            return host, wm

        sub_engine = StagedFactorSearch(self.catalogue)
        sub_result = sub_engine.factorize(P.A_plus[0][1]) if P.A_plus[0][1] else None

        if sub_result is None:
            return None

        factor_A, factor_B, sub_wm = sub_result

        wm = WitnessMatrix(
            local_consistent=sub_wm.local_consistent,
            global_consistent=True,
            host_recovered=True,
            payload_built=True,
            depth=host.depth() + 1
        )
        wm.add_note("Coupled payload-system constructed (staged)")

        new_A_plus = [(host.A_plus[0][0], factor_A)]
        new_host = UCNSObject(new_A_plus, host.F_plus, host.n_min)
        return new_host, wm

    def _verify_globally(self, A: UCNSObject, B: UCNSObject, P: UCNSObject, wm: WitnessMatrix) -> bool:
        reconstructed = multiply(A, B)
        if _objects_equal(reconstructed, P):
            wm.global_consistent = True
            wm.add_note("Global multiplication round-trip PASSED")
            return True
        else:
            wm.global_consistent = False
            wm.add_note("Global multiplication round-trip FAILED")
            return False

    def factorize(self, P: UCNSObject) -> Optional[Tuple[UCNSObject, UCNSObject, WitnessMatrix]]:
        self._witness = WitnessMatrix(depth=P.depth())

        host = self._recover_host(P)
        if host is None:
            self._witness.add_note("Host recovery failed")
            return None

        result = self._build_payload_system(host, P)
        if result is None:
            self._witness.add_note("Payload system construction failed")
            return None

        new_host, wm = result

        A = new_host
        B = None
        for cand in self.catalogue:
            if left_quotient(P, A, [cand]) is not None:
                B = cand
                break
        if B is None:
            B = P.A_plus[0][1] if P.A_plus[0][1] else UCNSObject([(UCN(0.0), None)])

        if not self._verify_globally(A, B, P, wm):
            return None

        wm.depth = P.depth()
        self._witness = wm
        return A, B, wm

    def factor_search(self, P: UCNSObject) -> Optional[Tuple[UCNSObject, UCNSObject]]:
        result = self.factorize(P)
        if result is None:
            return None
        A, B, _ = result
        return A, B


def factor_search(P: UCNSObject, catalogue: Optional[List[UCNSObject]] = None) -> Optional[Tuple[UCNSObject, UCNSObject]]:
    engine = StagedFactorSearch(catalogue)
    return engine.factor_search(P)


def multiply_objects(A: UCNSObject, B: UCNSObject) -> UCNSObject:
    return multiply(A, B)


if __name__ == "__main__":
    print("=== v0.8.0 Staged Factorization Experiment (factorization1) ===\n")

    s1 = UCNSObject([(UCN(0.0), None)], [0], n_min=1)
    s2 = UCNSObject([(UCN(0.5), s1)], [1], n_min=2)

    engine = StagedFactorSearch()
    result = engine.factorize(s2)

    if result:
        A, B, wm = result
        print("✓ Staged factorization succeeded on depth-2 oracle case")
        print(f"  Witness valid: {wm.is_valid()}")
        print("\nThis is still EXPERIMENTAL — full frozen depth-2 domain not yet green.")
    else:
        print("✗ Factorization failed on this case")
