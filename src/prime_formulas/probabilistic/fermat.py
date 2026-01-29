from __future__ import annotations

import random
import time
from typing import Any, Dict, Iterable, Optional

from ..interfaces import PrimeAlgorithm
from ..registry import register
from ..schemas import AlgorithmMeta, Parameter, VisualizationHint


class FermatTest(PrimeAlgorithm):
    name = "fermat_test"
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

        rng = random.Random(seed)
        witnessed = False
        chosen_bases = list(bases) if bases is not None else []
        if not chosen_bases:
            chosen_bases = [rng.randrange(2, n - 1) for _ in range(rounds)]

        for a in chosen_bases:
            witnessed = pow(a, n - 1, n) != 1
            if witnessed:
                break

        return {
            "result": not witnessed,
            "meta": {
                "time_ms": (time.perf_counter() - start) * 1000,
                "rounds": len(chosen_bases),
                "witness": witnessed,
                "bases": chosen_bases,
            },
        }


register(
    FermatTest(),
    AlgorithmMeta(
        name=FermatTest.name,
        category=FermatTest.category,
        summary="Probabilistic primality test using Fermat's little theorem.",
        description=(
            "Chooses random bases a and checks whether a^(n-1) ≡ 1 (mod n). "
            "A violation identifies a composite. Susceptible to Carmichael numbers."
        ),
        complexity="O(rounds * log^3 n) for modular exponentiation",
        parameters=[
            Parameter(
                name="rounds",
                type="int",
                description="Number of random bases to test.",
                default=5,
            ),
            Parameter(
                name="bases",
                type="Iterable[int]",
                description="Explicit bases; overrides random sampling when provided.",
                default=None,
            ),
            Parameter(
                name="seed",
                type="Optional[int]",
                description="Seed for reproducible random bases.",
                default=None,
            ),
        ],
        visualization=VisualizationHint(
            mode="curve",
            steps="Plot pow(a, n-1, n) for each base and flag witnesses.",
            sample_input={"n": 341, "rounds": 5, "seed": 42},
        ),
    ),
)
