from __future__ import annotations

from typing import Any, Dict, Protocol


class PrimeAlgorithm(Protocol):
    """Protocol every prime-related algorithm must implement."""

    name: str
    category: str

    def run(self, n: int, **kwargs: Any) -> Dict[str, Any]:
        """Execute the algorithm on input ``n`` and return result + metadata."""
        ...
