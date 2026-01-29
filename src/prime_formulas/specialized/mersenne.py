from __future__ import annotations

import math
import time
from typing import Any, Dict

from ..interfaces import PrimeAlgorithm
from ..registry import register
from ..schemas import AlgorithmMeta, Parameter, VisualizationHint
from ..utils.primes import is_prime_basic


class MersenneCandidate(PrimeAlgorithm):
    name = "mersenne_candidate"
    category = "specialized"

    def run(self, p: int, **kwargs: Any) -> Dict[str, Any]:
        start = time.perf_counter()
        if p <= 1 or not is_prime_basic(p):
            return {"result": None, "meta": {"time_ms": 0.0, "error": "p must be prime"}}
        value = (1 << p) - 1
        return {
            "result": value,
            "meta": {
                "time_ms": (time.perf_counter() - start) * 1000,
                "digits": int(math.log10(value)) + 1,
            },
        }


register(
    MersenneCandidate(),
    AlgorithmMeta(
        name=MersenneCandidate.name,
        category=MersenneCandidate.category,
        summary="Constructs Mersenne number 2^p - 1 for prime exponent p.",
        description=(
            "Produces Mersenne candidate numbers. Use Lucas–Lehmer test to confirm primality."
        ),
        complexity="O(1) plus big-int multiplication cost",
        parameters=[
            Parameter(
                name="p",
                type="int",
                description="Prime exponent for candidate 2^p - 1.",
            )
        ],
        visualization=VisualizationHint(
            mode="curve",
            steps="Show exponential growth of 2^p - 1 as p increases.",
            sample_input={"p": 17},
        ),
    ),
)
