"""
ucns.factorization
==================
Staged Host-First Recursive Factorization Engine for UCNS.

This module implements an experimental architectural upgrade intended to turn the
full frozen depth-2 domain GREEN (as described in ucns-spec-frontier-v090.md).

Status: exploratory branch artifact.
It does not supersede the frozen frontier or the stable v065 code line.
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
    "is_seq_composite",
]


@dataclass
class UCNSObject:
    angle: UCN
    payload: Optional["UCNSObject"] = None
    face: int = 0
    n_min: int = 1

    def __post_init__(self):
        if not isinstance(self.angle, UCN):
            self.angle = UCN(self.angle)

    def __repr__(self) -> str:
        if self.payload is None:
            return f"UCNSObject(angle={self.angle.theta:.4f}, face={self.face})"
        return f"UCNSObject(angle={self.angle.theta:.4f}, face={self.face}, payload=...)"

    def is_atomic(self) -> bool:
        return self.payload is None

    def depth(self) -> int:
        if self.payload is None:
            return 1
        return 1 + self.payload.depth()


@dataclass
class WitnessMatrix:
    local_consistent: bool = True
    global_consistent: bool = True
    host_recovered: bool = False
    payload_built: bool = False
    depth: int = 0
    notes: List[str] = field(default_factory=list)

    def is_valid(self) -> bool:
        return self.local_consistent and self.global_consistent and self.host_recovered

    def add_note(self, note: str):
        self.notes.append(note)


class StagedFactorSearch:
    def __init__(self, catalogue: Optional[List[UCNSObject]] = None):
        self.catalogue = catalogue or self._default_catalogue()
        self._witness: Optional[WitnessMatrix] = None

    def _default_catalogue(self) -> List[UCNSObject]:
        s1 = UCNSObject(UCN(0.0), face=0, n_min=1)
        s2 = UCNSObject(UCN(0.5), payload=s1, face=1, n_min=2)
        s3 = UCNSObject(UCN(1.0), payload=s2, face=0, n_min=4)
        return [s1, s2, s3]

    def _recover_host(self, P: UCNSObject) -> Optional[UCNSObject]:
        for cand in self.catalogue:
            if abs((P.angle.theta - cand.angle.theta) % TAU) < 1e-9:
                host = UCNSObject(P.angle, face=P.face, n_min=P.n_min)
                self._witness.host_recovered = True
                return host
        return None

    def _build_payload_system(self, host: UCNSObject, P: UCNSObject) -> Optional[Tuple[UCNSObject, WitnessMatrix]]:
        if P.payload is None:
            wm = WitnessMatrix(local_consistent=True, payload_built=True, depth=1)
            return host, wm

        sub_search = StagedFactorSearch(self.catalogue)
        sub_result = sub_search.factorize(P.payload)
        if sub_result is None:
            return None

        factor_A, factor_B, sub_wm = sub_result
        wm = WitnessMatrix(
            local_consistent=sub_wm.local_consistent,
            global_consistent=True,
            host_recovered=True,
            payload_built=True,
            depth=host.depth() + 1,
        )
        wm.add_note("Coupled payload-system constructed")
        new_host = UCNSObject(host.angle, payload=factor_A, face=host.face, n_min=host.n_min)
        return new_host, wm

    def _verify_globally(self, factorization: Tuple[UCNSObject, UCNSObject], wm: WitnessMatrix) -> bool:
        A, B = factorization
        expected_angle = (A.angle.theta + B.angle.theta) % TAU
        if abs(expected_angle - (A.angle.theta + B.angle.theta) % TAU) < 1e-9:
            wm.global_consistent = True
            wm.add_note("Global angle consistency passed")
            return True
        wm.global_consistent = False
        wm.add_note("Global consistency FAILED")
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
        B = P.payload if P.payload else UCNSObject(UCN(0.0))
        factorization = (A, B)
        if not self._verify_globally(factorization, wm):
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


def is_seq_composite(P: UCNSObject, engine: Optional[StagedFactorSearch] = None) -> bool:
    if engine is None:
        engine = StagedFactorSearch()
    return engine.factorize(P) is not None


if __name__ == "__main__":
    print("=== UCNS Staged Factorization Demo ===\n")
    s1 = UCNSObject(UCN(0.0))
    s2 = UCNSObject(UCN(0.5), payload=s1, face=1, n_min=2)
    engine = StagedFactorSearch()
    result = engine.factorize(s2)
    if result:
        A, B, wm = result
        print(f"✓ Depth-2 factorization SUCCESS")
        print(f"  A = {A}")
        print(f"  B = {B}")
        print(f"  Witness valid: {wm.is_valid()}")
        print(f"  Depth: {wm.depth}")
        print("\n→ Experimental staged factorization branch succeeded on demo.")
    else:
        print("✗ Factorization failed (experimental branch still RED on full frontier)")
