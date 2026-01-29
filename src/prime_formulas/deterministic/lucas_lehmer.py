from __future__ import annotations

import time
from typing import Any, Dict

from ..interfaces import PrimeAlgorithm
from ..registry import register
from ..schemas import AlgorithmMeta, Parameter, VisualizationHint


class LucasLehmer(PrimeAlgorithm):
    name = "lucas_lehmer"
    category = "deterministic"

    def run(self, p: int, **kwargs: Any) -> Dict[str, Any]:
        start = time.perf_counter()
        if p == 2:
            return {"result": True, "meta": {"time_ms": 0.0}}
        if p < 2:
            return {"result": False, "meta": {"time_ms": 0.0}}

        M_p = (1 << p) - 1
        s = 4
        frames = [{"t": 0, "payload": {"s": s}}]
        for i in range(p - 2):
            s = (s * s - 2) % M_p
            frames.append({"t": i + 1, "payload": {"s": s}})

        return {
            "result": s == 0,
            "meta": {
                "time_ms": (time.perf_counter() - start) * 1000,
                "iterations": p - 2,
                "frames": frames,
            },
        }


register(
    LucasLehmer(),
    AlgorithmMeta(
        name=LucasLehmer.name,
        category=LucasLehmer.category,
        summary="Deterministic test for Mersenne primes with exponent p.",
        description=(
            "Lucas–Lehmer test checks whether 2^p - 1 is prime. "
            "Iteratively computes s_{i+1} = s_i^2 - 2 modulo M_p."
        ),
        complexity="O(p log^2 p)",
        parameters=[
            Parameter(
                name="p",
                type="int",
                description="Prime exponent for Mersenne number 2^p - 1.",
            )
        ],
        visualization=VisualizationHint(
            mode="curve",
            steps="Plot sequence s_i modulo M_p; prime iff final state is 0.",
            sample_input={"p": 13},
        ),
    ),
)
