"""
grader.py - Agent grading system for the LifeOS ✨.

Evaluates the quality of an agent's final life state on a normalized
0.0-1.0 scale, where:
    ~0.2   -> poor life outcome
    ~0.5   -> average outcome
    ~0.9+  -> well-balanced, thriving life

Grading is fair, deterministic, and independent of personality/difficulty.
"""

from __future__ import annotations
from typing import Any, Dict
from utils import normalize, clamp, imbalance_penalty


# Weights for final evaluation (sum = 1.0)
GRADE_WEIGHTS = {
    "health":        0.25,
    "money":         0.15,
    "career":        0.20,
    "relationships": 0.20,
    "happiness":     0.10,
    "stress_inv":    0.10,    # inverse stress
}

# Money is open-ended; we cap normalization at this value
MONEY_NORM_CAP = 10_000.0


def grade_agent(final_state: Dict[str, Any], task_type: str = "perfect_balance") -> float:
    """Compute a 0.0-1.0 grade from a final life-state dictionary based on TaskType.

    Parameters
    ----------
    final_state : dict
        Must contain keys: health, money, career, relationships, happiness, stress.
    task_type : str
        The specific objective being evaluated (wealth_builder, career_climber, perfect_balance).

    Returns
    -------
    float  - grade between 0.0 and 1.0
    """
    if task_type == "wealth_builder":
        # Objective: Maximize money (> $50,000)
        money = final_state.get("money", 0)
        health = final_state.get("health", 0)
        if health <= 0: return 0.0
        return round(clamp(money / 50000.0, 0.0, 1.0), 4)

    elif task_type == "career_climber":
        # Objective: Reach Career > 90, penalize for burnout stress
        career = final_state.get("career", 0)
        stress = final_state.get("stress", 50)
        health = final_state.get("health", 0)
        if health <= 0: return 0.0
        base_score = clamp(career / 90.0, 0.0, 1.0)
        penalty = 0.0
        if stress > 80: penalty = (stress - 80) / 100.0
        return round(clamp(base_score - penalty, 0.0, 1.0), 4)

    # PERFECT_BALANCE
    # -- 1. Normalize each dimension --
    health_n     = normalize(final_state.get("health", 0), 0, 100)
    money_n      = normalize(final_state.get("money", 0), 0, MONEY_NORM_CAP)
    career_n     = normalize(final_state.get("career", 0), 0, 100)
    rel_n        = normalize(final_state.get("relationships", 0), 0, 100)
    happy_n      = normalize(final_state.get("happiness", 0), 0, 100)
    stress_inv_n = 1.0 - normalize(final_state.get("stress", 50), 0, 100)

    # -- 2. Weighted base score --
    norm_vals = {
        "health":        health_n,
        "money":         money_n,
        "career":        career_n,
        "relationships": rel_n,
        "happiness":     happy_n,
        "stress_inv":    stress_inv_n,
    }
    weighted_sum = sum(norm_vals[k] * GRADE_WEIGHTS[k] for k in GRADE_WEIGHTS)

    # -- 3. Imbalance penalty --
    core = [health_n, career_n, rel_n, happy_n, stress_inv_n]
    imb = imbalance_penalty(core)
    penalty = imb * 0.20      # up to 20% deduction for extreme imbalance

    # -- 4. Survival bonus --
    survival = 0.05 if final_state.get("health", 0) > 0 else 0.0

    # -- 5. Final score --
    score = weighted_sum - penalty + survival
    return round(clamp(score, 0.0, 1.0), 4)


def grade_label(score: float) -> str:
    """Return a human-readable label for a numeric grade."""
    if score >= 0.85:
        return "[*] Excellent - Balanced & Thriving"
    elif score >= 0.65:
        return "[+] Good - Healthy Life"
    elif score >= 0.45:
        return "[~] Average - Room for Improvement"
    elif score >= 0.25:
        return "[-] Poor - Struggling"
    else:
        return "[!] Critical - Life in Crisis"
