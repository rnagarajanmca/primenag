from __future__ import annotations

from typing import Dict, Iterable, Optional

from .interfaces import PrimeAlgorithm
from .schemas import AlgorithmMeta

_algorithms: Dict[str, PrimeAlgorithm] = {}
_metadata: Dict[str, AlgorithmMeta] = {}


def register(algo: PrimeAlgorithm, meta: AlgorithmMeta) -> None:
    """Register an algorithm and its metadata."""

    if algo.name in _algorithms:
        raise ValueError(f"Algorithm '{algo.name}' already registered")
    _algorithms[algo.name] = algo
    _metadata[algo.name] = meta


def get(name: str) -> PrimeAlgorithm:
    return _algorithms[name]


def get_metadata(name: str) -> AlgorithmMeta:
    return _metadata[name]


def list_algorithms(category: Optional[str] = None) -> Iterable[AlgorithmMeta]:
    metas = _metadata.values()
    if category is None:
        return tuple(metas)
    return tuple(meta for meta in metas if meta.category == category)
