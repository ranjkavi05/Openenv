"""
utils.py — Utility functions for the AI Digital Life Simulator.

General-purpose helpers used across modules: value clamping,
normalization, pretty-printing, and statistics.
"""

from __future__ import annotations
from typing import Any, Dict, List
import statistics


def clamp(value: float, lo: float = 0.0, hi: float = 100.0) -> float:
    """Clamp *value* to the inclusive range [lo, hi].

    >>> clamp(120, 0, 100)
    100
    >>> clamp(-5, 0, 100)
    0
    """
    return max(lo, min(hi, value))


def normalize(value: float, lo: float = 0.0, hi: float = 100.0) -> float:
    """Linearly scale *value* from range [lo, hi] to [0, 1].

    >>> normalize(50, 0, 100)
    0.5
    """
    if hi == lo:
        return 0.0
    return clamp((value - lo) / (hi - lo), 0.0, 1.0)


def weighted_average(values: Dict[str, float],
                     weights: Dict[str, float]) -> float:
    """Compute a weighted average where both dicts share the same keys.

    Any key present in *values* but missing from *weights* is ignored.
    """
    total_w = sum(weights.get(k, 0) for k in values)
    if total_w == 0:
        return 0.0
    return sum(values[k] * weights.get(k, 0) for k in values) / total_w


def imbalance_penalty(values: List[float]) -> float:
    """Return a penalty (0–1) based on the standard deviation of *values*.

    Higher deviation → higher penalty. Encourages a balanced life.
    Values are expected to be already normalized to 0–1.
    """
    if len(values) < 2:
        return 0.0
    stdev = statistics.pstdev(values)
    # Max possible stdev for values in [0,1] is 0.5 → scale to 0–1
    return clamp(stdev / 0.5, 0.0, 1.0)


def format_state(state: Dict[str, Any], indent: int = 2) -> str:
    """Pretty-print a state dictionary as aligned key: value lines."""
    lines = []
    max_key = max(len(str(k)) for k in state) if state else 0
    for k, v in state.items():
        if isinstance(v, float):
            lines.append(f"{' ' * indent}{str(k).ljust(max_key)} : {v:>8.1f}")
        else:
            lines.append(f"{' ' * indent}{str(k).ljust(max_key)} : {v!s:>8}")
    return "\n".join(lines)


def format_bar(label: str, value: float, max_val: float = 100.0,
               width: int = 30) -> str:
    """Return a text-based progress bar string.

    >>> format_bar("Health", 75)
    'Health  |██████████████████████▒▒▒▒▒▒▒▒|  75.0%'
    """
    ratio = clamp(value / max_val, 0.0, 1.0)
    filled = int(ratio * width)
    bar = "█" * filled + "▒" * (width - filled)
    return f"{label.ljust(14)} |{bar}| {value:6.1f} / {max_val:.0f}"
