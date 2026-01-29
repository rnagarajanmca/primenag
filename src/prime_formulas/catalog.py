"""Central module to load all prime algorithms for registration."""

from __future__ import annotations

import importlib
from typing import List

MODULES: List[str] = [
    # basic
    "prime_formulas.basic.trial_division",
    "prime_formulas.basic.sieve_eratosthenes",
    "prime_formulas.basic.sieve_atkin",
    # probabilistic
    "prime_formulas.probabilistic.fermat",
    "prime_formulas.probabilistic.miller_rabin",
    # deterministic
    "prime_formulas.deterministic.lucas_lehmer",
    "prime_formulas.deterministic.wilson",
    # generating
    "prime_formulas.generating.euclid_mullin",
    "prime_formulas.generating.mills",
    # specialized
    "prime_formulas.specialized.mersenne",
    "prime_formulas.specialized.sophie_germain",
    # modular
    "prime_formulas.modular.legendre_symbol",
    # analytic
    "prime_formulas.analytic.prime_number_theorem",
]


def load_all_algorithms() -> None:
    for module in MODULES:
        importlib.import_module(module)
