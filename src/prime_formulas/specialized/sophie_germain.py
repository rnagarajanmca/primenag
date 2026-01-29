from __future__ import annotations

import time
from typing import Any, Dict

from ..interfaces import PrimeAlgorithm
from ..registry import register
from ..schemas import AlgorithmMeta, Parameter, VisualizationHint
from ..utils.primes import is_prime_basic


class SophieGermainTest(PrimeAlgorithm):
    name = "sophie_germain_test"
    category = "specialized"

    def run(self, p: int, **kwargs: Any) -> Dict[str, Any]:
        start = time.perf_counter()
        prime = is_prime_basic(p)
        safe_prime = is_prime_basic(2 * p + 1) if prime else False

        return {
            "result": prime and safe_prime,
            "meta": {
                "time_ms": (time.perf_counter() - start) * 1000,
                "safe_prime": 2 * p + 1 if safe_prime else None,
            },
        }


register(
    SophieGermainTest(),
    AlgorithmMeta(
        name=SophieGermainTest.name,
        category=SophieGermainTest.category,
        summary="Determines whether p is a Sophie Germain prime (p and 2p+1 both prime).",
        description=(
            "Checks primality of p and its associated safe prime q = 2p+1. "
            "Important for cryptography (safe primes)."
        ),
        complexity="O(√(2p+1)) using basic primality checks",
        parameters=[
            Parameter(
                name="p",
                type="int",
                description="Candidate prime p for Sophie Germain property.",
            )
        ],
        visualization=VisualizationHint(
            mode="bars",
            steps="Show both p and 2p+1 on a number line and indicate primality.",
            sample_input={"p": 23},
        ),
    ),
)
