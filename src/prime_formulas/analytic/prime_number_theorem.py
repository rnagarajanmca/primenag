from __future__ import annotations

import math
import time
from typing import Any, Dict

from ..interfaces import PrimeAlgorithm
from ..registry import register
from ..schemas import AlgorithmMeta, Parameter, VisualizationHint
from ..utils.primes import primes_up_to


def li_approx(n: int) -> float:
    """Simple logarithmic integral approximation using series expansion."""

    if n < 2:
        return 0.0
    x = math.log(n)
    # li(x) ≈ x / ln x + x / (ln x)^2 + 2x / (ln x)^3
    inv = 1 / x
    return n * (inv + inv**2 + 2 * inv**3)


class PrimeNumberTheoremAlgo(PrimeAlgorithm):
    name = "prime_number_theorem"
    category = "analytic"

    def run(self, n: int, **kwargs: Any) -> Dict[str, Any]:
        start = time.perf_counter()
        if n < 2:
            return {
                "result": {
                    "actual": 0,
                    "pnt": 0.0,
                    "li": 0.0,
                },
                "meta": {"time_ms": 0.0},
            }

        actual = len(primes_up_to(n))
        pnt_estimate = n / math.log(n)
        li_estimate = li_approx(n)

        return {
            "result": {"actual": actual, "pnt": pnt_estimate, "li": li_estimate},
            "meta": {"time_ms": (time.perf_counter() - start) * 1000},
        }


register(
    PrimeNumberTheoremAlgo(),
    AlgorithmMeta(
        name=PrimeNumberTheoremAlgo.name,
        category=PrimeNumberTheoremAlgo.category,
        summary="Compares actual π(n) with Prime Number Theorem and logarithmic integral estimates.",
        description=(
            "Counts primes ≤ n and returns approximations π(n) ≈ n/log n and Li(n). "
            "Useful to visualize asymptotic accuracy of analytic estimates."
        ),
        complexity="O(n log log n) to count primes + constant-time approximations",
        parameters=[
            Parameter(
                name="n",
                type="int",
                description="Upper bound for prime counting.",
            )
        ],
        visualization=VisualizationHint(
            mode="curve",
            steps="Plot actual π(n) alongside n/log n and Li(n) approximations.",
            sample_input={"n": 1000},
        ),
    ),
)
