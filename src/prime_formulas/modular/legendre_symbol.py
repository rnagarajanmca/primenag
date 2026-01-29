from __future__ import annotations

import time
from typing import Any, Dict

from ..interfaces import PrimeAlgorithm
from ..registry import register
from ..schemas import AlgorithmMeta, Parameter, VisualizationHint
from ..utils.primes import is_prime_basic


def legendre_symbol(a: int, p: int) -> int:
    """Compute the Legendre symbol (a|p) for odd prime p."""

    a %= p
    if a == 0:
        return 0
    if a == 1:
        return 1
    if a == 2:
        return 1 if p % 8 in (1, 7) else -1
    if a == p - 1:
        return -1 if p % 4 == 3 else 1

    # Quadratic reciprocity
    ls = 1
    while a:
        while a % 2 == 0:
            a //= 2
            if p % 8 in (3, 5):
                ls = -ls
        a, p = p, a
        if a % 4 == 3 and p % 4 == 3:
            ls = -ls
        a %= p
        if a > p // 2:
            a -= p
    return ls if p == 1 else 0


class LegendreSymbolAlgo(PrimeAlgorithm):
    name = "legendre_symbol"
    category = "modular"

    def run(self, p: int, *, a: int) -> Dict[str, Any]:
        start = time.perf_counter()
        if p <= 2 or not is_prime_basic(p):
            return {
                "result": None,
                "meta": {"time_ms": 0.0, "error": "p must be an odd prime"},
            }
        result = legendre_symbol(a, p)
        return {
            "result": result,
            "meta": {"time_ms": (time.perf_counter() - start) * 1000},
        }


register(
    LegendreSymbolAlgo(),
    AlgorithmMeta(
        name=LegendreSymbolAlgo.name,
        category=LegendreSymbolAlgo.category,
        summary="Computes the Legendre symbol (a|p) for quadratic residue testing.",
        description=(
            "Uses quadratic reciprocity to determine whether a is a quadratic residue modulo p."
        ),
        complexity="O(log p)",
        parameters=[
            Parameter(name="p", type="int", description="Odd prime modulus."),
            Parameter(name="a", type="int", description="Residue to test."),
        ],
        visualization=VisualizationHint(
            mode="graph",
            steps="Display residues modulo p and highlight quadratic residues vs. non-residues.",
            sample_input={"p": 23, "a": 7},
        ),
    ),
)
