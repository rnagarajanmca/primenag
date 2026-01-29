#!/usr/bin/env python3
"""Export algorithm metadata and optional sample runs to JSON."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict

import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from prime_formulas.catalog import load_all_algorithms  # noqa: E402
from prime_formulas.registry import get, list_algorithms  # noqa: E402


def run_sample(name: str, sample_input: Dict[str, Any]) -> Dict[str, Any]:
    algo = get(name)
    return algo.run(**sample_input)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        default="public/algorithms.json",
        type=Path,
        help="Path to write metadata JSON.",
    )
    parser.add_argument(
        "--examples-dir",
        default="public/examples",
        type=Path,
        help="Directory to store sample outputs (if available).",
    )
    parser.add_argument(
        "--samples",
        action="store_true",
        help="Generate sample runs for algorithms that define sample_input in metadata.",
    )
    args = parser.parse_args()

    load_all_algorithms()
    metas = list(list_algorithms())

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.examples_dir.mkdir(parents=True, exist_ok=True)

    json.dump([asdict(meta) for meta in metas], args.output.open("w"), indent=2)

    if args.samples:
        for meta in metas:
            viz = meta.visualization
            if viz and viz.sample_input:
                try:
                    result = run_sample(meta.name, viz.sample_input)
                except Exception as exc:  # noqa: BLE001
                    result = {"error": str(exc)}
                sample_path = args.examples_dir / f"{meta.name}.json"
                json.dump(
                    {
                        "input": viz.sample_input,
                        "output": result,
                    },
                    sample_path.open("w"),
                    indent=2,
                )


if __name__ == "__main__":
    main()
