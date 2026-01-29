from __future__ import annotations

import math
from typing import Iterable


def is_prime_basic(n: int) -> bool:
    """Deterministic primality test suitable for moderate-size integers."""

    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False
    limit = int(math.isqrt(n))
    for divisor in range(3, limit + 1, 2):
        if n % divisor == 0:
            return False
    return True


def smallest_prime_factor(n: int) -> int:
    """Return the smallest prime factor of n (n > 1)."""

    if n % 2 == 0:
        return 2
    limit = int(math.isqrt(n))
    for divisor in range(3, limit + 1, 2):
        if n % divisor == 0:
            return divisor
    return n  # n is prime


def primes_up_to(limit: int) -> Iterable[int]:
    """Simple sieve returning primes up to limit inclusive."""

    if limit < 2:
        return []
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
    for p in range(2, int(math.isqrt(limit)) + 1):
        if sieve[p]:
            for multiple in range(p * p, limit + 1, p):
                sieve[multiple] = False
    return [i for i, flag in enumerate(sieve) if flag]
