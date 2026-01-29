from __future__ import annotations

import math
import time
from typing import Any, Dict

from ..interfaces import PrimeAlgorithm
from ..registry import register
from ..schemas import AlgorithmMeta, Parameter, VisualizationHint


class WilsonTest(PrimeAlgorithm):
    name = "wilson_test"
    category = "deterministic"

    def run(self, n: int, **kwargs: Any) -> Dict[str, Any]:
        start = time.perf_counter()
        if n < 2:
            return {"result": False, "meta": {"time_ms": 0.0}}
        if n == 2:
            return {"result": True, "meta": {"time_ms": 0.0}}

        factorial_mod = 1
        for i in range(2, n):
            factorial_mod = (factorial_mod * i) % n
            if factorial_mod == 0:
                break

        result = (factorial_mod + 1) % n == 0
        return {
            "result": result,
            "meta": {
                "time_ms": (time.perf_counter() - start) * 1000,
                "iterations": n - 2,
            },
        }


register(
    WilsonTest(),
    AlgorithmMeta(
        name=WilsonTest.name,
        category=WilsonTest.category,
        summary="Deterministic primality test using Wilson's theorem.",
        description=(
            "Wilson's theorem states that n is prime iff (n-1)! ≡ -1 (mod n). "
            "This implementation computes factorial modulo n."
        ),
        complexity="O(n)",
        parameters=[
            Parameter(
                name="n",
                type="int",
                description="Candidate integer to test for primality.",
            )
        ],
        visualization=VisualizationHint(
            mode="bars",
            steps="Accumulate factorial modulo n and observe when it deviates.",
            sample_input={"n": 11},
        ),
    ),
)
