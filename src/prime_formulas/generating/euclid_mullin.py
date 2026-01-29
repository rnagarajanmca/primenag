from __future__ import annotations

import math
import time
from typing import Any, Dict, List

from ..interfaces import PrimeAlgorithm
from ..registry import register
from ..schemas import AlgorithmMeta, Parameter, VisualizationHint
from ..utils.primes import smallest_prime_factor


class EuclidMullin(PrimeAlgorithm):
    name = "euclid_mullin_sequence"
    category = "generating"

    def run(self, k: int, **kwargs: Any) -> Dict[str, Any]:
        start = time.perf_counter()
        if k <= 0:
            return {"result": [], "meta": {"time_ms": 0.0}}

        sequence: List[int] = [2]
        for _ in range(1, k):
            product = 1
            for val in sequence:
                product *= val
            next_term = smallest_prime_factor(product + 1)
            sequence.append(next_term)

        return {
            "result": sequence,
            "meta": {"time_ms": (time.perf_counter() - start) * 1000, "length": k},
        }


register(
    EuclidMullin(),
    AlgorithmMeta(
        name=EuclidMullin.name,
        category=EuclidMullin.category,
        summary="Generates Euclid–Mullin sequence: next term is smallest prime factor of product+1.",
        description=(
            "Start at 2; multiply known terms, add 1, and take the smallest prime factor. "
            "Sequence illustrates Euclid's proof idea for infinitude of primes."
        ),
        complexity="Super-exponential growth; practical for small k.",
        parameters=[
            Parameter(
                name="k",
                type="int",
                description="Number of terms to generate (k ≥ 1).",
            )
        ],
        visualization=VisualizationHint(
            mode="bars",
            steps="Show cumulative product and factorization at each step.",
            sample_input={"k": 5},
        ),
    ),
)
