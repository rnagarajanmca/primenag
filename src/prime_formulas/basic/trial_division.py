from __future__ import annotations

import math
import time
from typing import Any, Dict, List

from ..interfaces import PrimeAlgorithm
from ..registry import register
from ..schemas import AlgorithmMeta, Parameter, VisualizationHint


class TrialDivision(PrimeAlgorithm):
    name = "trial_division"
    category = "basic"

    def run(self, n: int, *, return_factors: bool = False) -> Dict[str, Any]:
        start = time.perf_counter()
        if n < 2:
            return {
                "result": False,
                "meta": {
                    "time_ms": (time.perf_counter() - start) * 1000,
                    "factors": [] if return_factors else None,
                },
            }

        limit = int(math.isqrt(n))
        factors: List[int] = []
        if n % 2 == 0:
            if return_factors:
                factors.append(2)
            return {
                "result": n == 2,
                "meta": {
                    "time_ms": (time.perf_counter() - start) * 1000,
                    "iterations": 1,
                    "factors": factors if return_factors else None,
                },
            }

        iterations = 0
        for divisor in range(3, limit + 1, 2):
            iterations += 1
            if n % divisor == 0:
                if return_factors:
                    factors.append(divisor)
                return {
                    "result": False,
                    "meta": {
                        "time_ms": (time.perf_counter() - start) * 1000,
                        "iterations": iterations,
                        "factors": factors if return_factors else None,
                    },
                }

        return {
            "result": True,
            "meta": {
                "time_ms": (time.perf_counter() - start) * 1000,
                "iterations": iterations,
                "factors": factors if return_factors else None,
            },
        }


register(
    TrialDivision(),
    AlgorithmMeta(
        name=TrialDivision.name,
        category=TrialDivision.category,
        summary="Deterministic primality test by checking divisibility up to √n.",
        description=(
            "Trial division is the most fundamental primality test. "
            "It checks divisibility of n by every odd number up to √n."
        ),
        complexity="O(√n)",
        parameters=[
            Parameter(
                name="return_factors",
                type="bool",
                description="Include found factors in metadata when composite.",
                default=False,
            )
        ],
        visualization=VisualizationHint(
            mode="bars",
            steps="Highlight each attempted divisor up to √n.",
            sample_input={"n": 221},
        ),
    ),
)
