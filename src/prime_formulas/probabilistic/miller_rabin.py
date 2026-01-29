from __future__ import annotations

import random
import time
from typing import Any, Dict, Iterable, Optional

from ..interfaces import PrimeAlgorithm
from ..registry import register
from ..schemas import AlgorithmMeta, Parameter, VisualizationHint


class MillerRabin(PrimeAlgorithm):
    name = "miller_rabin"
    category = "probabilistic"

    def run(
        self,
        n: int,
        *,
        rounds: int = 5,
        bases: Optional[Iterable[int]] = None,
        seed: Optional[int] = None,
    ) -> Dict[str, Any]:
        start = time.perf_counter()
        if n < 2:
            return {"result": False, "meta": {"time_ms": 0.0}}
        if n in (2, 3):
            return {"result": True, "meta": {"time_ms": 0.0}}
        if n % 2 == 0:
            return {"result": False, "meta": {"time_ms": 0.0}}

        # write n-1 as d * 2^s with d odd
        d = n - 1
        s = 0
        while d % 2 == 0:
            d //= 2
            s += 1

        rng = random.Random(seed)
        chosen_bases = list(bases) if bases is not None else []
        if not chosen_bases:
            chosen_bases = [rng.randrange(2, n - 2) for _ in range(rounds)]

        def check(a: int) -> bool:
            x = pow(a, d, n)
            if x in (1, n - 1):
                return True
            for _ in range(s - 1):
                x = pow(x, 2, n)
                if x == n - 1:
                    return True
            return False

        witnessed = False
        for a in chosen_bases:
            if not check(a):
                witnessed = True
                break

        return {
            "result": not witnessed,
            "meta": {
                "time_ms": (time.perf_counter() - start) * 1000,
                "rounds": len(chosen_bases),
                "witness": witnessed,
                "bases": chosen_bases,
                "s": s,
                "d": d,
            },
        }


register(
    MillerRabin(),
    AlgorithmMeta(
        name=MillerRabin.name,
        category=MillerRabin.category,
        summary="Probabilistic primality test using Miller–Rabin strong pseudoprime rounds.",
        description=(
            "Miller–Rabin writes n-1 = d·2^s and checks whether random bases witness compositeness. "
            "If all rounds pass, n is probably prime with error ≤ 4^-rounds."
        ),
        complexity="O(rounds * log^3 n)",
        parameters=[
            Parameter(
                name="rounds",
                type="int",
                description="Number of random bases when 'bases' not provided.",
                default=5,
            ),
            Parameter(
                name="bases",
                type="Iterable[int]",
                description="Optional explicit bases to test.",
                default=None,
            ),
            Parameter(
                name="seed",
                type="Optional[int]",
                description="Seed for deterministic base sampling.",
                default=None,
            ),
        ],
        visualization=VisualizationHint(
            mode="bars",
            steps="Show modular exponentiation traces for each base; flag first witness.",
            sample_input={"n": 561, "rounds": 5, "seed": 7},
        ),
    ),
)
