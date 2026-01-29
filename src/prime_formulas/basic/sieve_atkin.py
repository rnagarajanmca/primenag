from __future__ import annotations

import math
import time
from typing import Any, Dict, List

from ..interfaces import PrimeAlgorithm
from ..registry import register
from ..schemas import AlgorithmMeta, Parameter, VisualizationHint


class SieveAtkin(PrimeAlgorithm):
    name = "sieve_atkin"
    category = "basic"

    def run(self, n: int, **kwargs: Any) -> Dict[str, Any]:
        start = time.perf_counter()
        if n < 2:
            return {"result": [], "meta": {"time_ms": 0.0}}

        sieve = [False] * (n + 1)
        limit_sqrt = int(math.isqrt(n)) + 1

        for x in range(1, limit_sqrt):
            for y in range(1, limit_sqrt):
                m = 4 * x * x + y * y
                if m <= n and m % 12 in (1, 5):
                    sieve[m] = not sieve[m]
                m = 3 * x * x + y * y
                if m <= n and m % 12 == 7:
                    sieve[m] = not sieve[m]
                m = 3 * x * x - y * y
                if x > y and m <= n and m % 12 == 11:
                    sieve[m] = not sieve[m]

        for r in range(5, limit_sqrt):
            if sieve[r]:
                square = r * r
                for k in range(square, n + 1, square):
                    sieve[k] = False

        primes = [2, 3] + [i for i in range(5, n + 1) if sieve[i]]
        return {
            "result": primes,
            "meta": {"time_ms": (time.perf_counter() - start) * 1000},
        }


register(
    SieveAtkin(),
    AlgorithmMeta(
        name=SieveAtkin.name,
        category=SieveAtkin.category,
        summary="Generates primes ≤ n using quadratic residue filters and toggling.",
        description=(
            "The sieve of Atkin is an optimized modern sieve using modular quadratic filters "
            "to detect potential primes before removing higher powers."
        ),
        complexity="O(n)",
        parameters=[
            Parameter(
                name="n",
                type="int",
                description="Upper bound (inclusive) for prime generation.",
            )
        ],
        visualization=VisualizationHint(
            mode="grid",
            steps="Toggle cells based on quadratic forms, then remove multiples of squares.",
            sample_input={"n": 60},
        ),
    ),
)
