import importlib

import pytest

# Ensure all initial algorithms are registered
MODULES = [
    "prime_formulas.basic.trial_division",
    "prime_formulas.basic.sieve_eratosthenes",
    "prime_formulas.basic.sieve_atkin",
    "prime_formulas.probabilistic.fermat",
    "prime_formulas.probabilistic.miller_rabin",
    "prime_formulas.deterministic.lucas_lehmer",
    "prime_formulas.deterministic.wilson",
]

for module in MODULES:
    importlib.import_module(module)

from prime_formulas.registry import get


def test_trial_division():
    algo = get("trial_division")
    assert algo.run(29)["result"] is True
    res = algo.run(221, return_factors=True)
    assert res["result"] is False
    assert res["meta"]["factors"] == [13]


def test_sieve_eratosthenes():
    algo = get("sieve_eratosthenes")
    assert algo.run(20)["result"] == [2, 3, 5, 7, 11, 13, 17, 19]


def test_sieve_atkin_matches_sieve():
    erat = get("sieve_eratosthenes").run(100)["result"]
    atkin = get("sieve_atkin").run(100)["result"]
    assert atkin == erat


def test_fermat_detects_composite():
    algo = get("fermat_test")
    res = algo.run(341, rounds=3, seed=1)
    assert res["result"] is False  # Carmichael number failed with chosen base


def test_miller_rabin_prime_vs_composite():
    algo = get("miller_rabin")
    assert algo.run(101, rounds=5, seed=2)["result"] is True
    assert algo.run(221, rounds=5, seed=2)["result"] is False


def test_lucas_lehmer():
    algo = get("lucas_lehmer")
    assert algo.run(7)["result"] is True  # 2^7 - 1 = 127 prime
    assert algo.run(11)["result"] is False  # 2^11 - 1 composite


def test_wilson():
    algo = get("wilson_test")
    assert algo.run(13)["result"] is True
    assert algo.run(15)["result"] is False
