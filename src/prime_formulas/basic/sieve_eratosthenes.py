from __future__ import annotations

import math
import time
from typing import Any, Dict, List

from ..interfaces import PrimeAlgorithm
from ..registry import register
from ..schemas import AlgorithmMeta, Parameter, VisualizationHint


class SieveEratosthenes(PrimeAlgorithm):
    name = "sieve_eratosthenes"
    category = "basic"

    def run(self, n: int, **kwargs: Any) -> Dict[str, Any]:
        start = time.perf_counter()
        if n < 2:
            return {"result": [], "meta": {"time_ms": 0.0, "frames": []}}

        sieve = [True] * (n + 1)
        sieve[0] = sieve[1] = False
        frames: List[Dict[str, Any]] = []

        for p in range(2, int(math.isqrt(n)) + 1):
            if sieve[p]:
                frames.append({"t": p, "payload": {"prime": p}})
                for multiple in range(p * p, n + 1, p):
                    sieve[multiple] = False

        primes = [i for i, is_prime in enumerate(sieve) if is_prime]
        return {
            "result": primes,
            "meta": {
                "time_ms": (time.perf_counter() - start) * 1000,
                "frames": frames,
            },
        }


register(
    SieveEratosthenes(),
    AlgorithmMeta(
        name=SieveEratosthenes.name,
        category=SieveEratosthenes.category,
        summary="Generates all primes ≤ n by iteratively marking multiples.",
        description=(
            "The sieve of Eratosthenes marks composites by iteratively striking multiples "
            "of each discovered prime. Complexity O(n log log n)."
        ),
        complexity="O(n log log n)",
        parameters=[
            Parameter(
                name="n",
                type="int",
                description="Upper bound (inclusive) for prime generation.",
            )
        ],
        visualization=VisualizationHint(
            mode="grid",
            steps="Mark multiples of each prime starting from its square.",
            sample_input={"n": 50},
        ),
    ),
)
