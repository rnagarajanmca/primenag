from __future__ import annotations

import math
import time
from typing import Any, Dict, List

from ..interfaces import PrimeAlgorithm
from ..registry import register
from ..schemas import AlgorithmMeta, Parameter, VisualizationHint
from ..utils.primes import is_prime_basic

# Approximate Mills' constant
MILLS_CONSTANT = 1.3063778838630806904686144926


class MillsFormula(PrimeAlgorithm):
    name = "mills_formula"
    category = "generating"

    def run(self, k: int, **kwargs: Any) -> Dict[str, Any]:
        start = time.perf_counter()
        if k <= 0:
            return {"result": [], "meta": {"time_ms": 0.0}}

        primes: List[int] = []
        current = MILLS_CONSTANT ** 3  # corresponds to floor(A^(3^1))
        for _ in range(k):
            candidate = math.floor(current + 1e-12)
            while not is_prime_basic(candidate):
                candidate += 1
            primes.append(candidate)
            current = current ** 3

        return {
            "result": primes,
            "meta": {"time_ms": (time.perf_counter() - start) * 1000},
        }


register(
    MillsFormula(),
    AlgorithmMeta(
        name=MillsFormula.name,
        category=MillsFormula.category,
        summary="Generates primes using Mills' constant and repeated cubing.",
        description=(
            "Mills proved that floor(A^(3^n)) is prime for some constant A (~1.30637788). "
            "Using an approximation yields a rapidly growing sequence of primes."
        ),
        complexity="Dominated by primality checks for exponentially growing numbers.",
        parameters=[
            Parameter(name="k", type="int", description="Number of primes to generate."),
        ],
        visualization=VisualizationHint(
            mode="curve",
            steps="Plot values of floor(A^(3^n)) as n increases.",
            sample_input={"k": 4},
        ),
    ),
)
