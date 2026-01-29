from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class Parameter:
    name: str
    type: str
    description: str
    default: Optional[Any] = None


@dataclass(frozen=True)
class VisualizationHint:
    mode: str  # e.g., "bars", "grid", "graph", "custom"
    steps: Optional[str] = None
    sample_input: Optional[Dict[str, Any]] = None


@dataclass(frozen=True)
class AlgorithmMeta:
    name: str
    category: str
    summary: str
    description: str
    complexity: str
    references: List[str] = field(default_factory=list)
    parameters: List[Parameter] = field(default_factory=list)
    visualization: Optional[VisualizationHint] = None
