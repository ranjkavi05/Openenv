"""
personalities.py — Personality modifier system for the AI Digital Life Simulator.

Each personality archetype adjusts how actions, rewards, and state transitions
behave, creating meaningfully different gameplay experiences.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict
from models import Personality, Action


# ─────────────────────────────────────────────
# Personality Modifier Profiles
# ─────────────────────────────────────────────

@dataclass
class PersonalityProfile:
    """Defines multipliers and biases applied by a personality type."""

    name: str
    description: str

    # Action-effect multipliers — scale the magnitude of each action's impact.
    # > 1.0 = amplifies the effect; < 1.0 = dampens it.
    action_multipliers: Dict[str, float] = field(default_factory=dict)

    # Reward bias — added (or subtracted) to the computed reward each step.
    reward_bias: float = 0.0

    # Stress modifier — extra stress added each step (personality baseline).
    stress_modifier: float = 0.0

    # Investment risk multiplier — scales the variance of investment outcomes.
    investment_risk: float = 1.0

    # Career growth multiplier — how fast career improves from learning/working.
    career_growth: float = 1.0

    # Work output multiplier — how much money is earned from working.
    work_output: float = 1.0

    # Social effectiveness — how much relationships improve from socializing.
    social_effectiveness: float = 1.0


# ─────────────────────────────────────────────
# Predefined Personality Profiles
# ─────────────────────────────────────────────

PERSONALITY_PROFILES: Dict[Personality, PersonalityProfile] = {

    Personality.RISK_TAKER: PersonalityProfile(
        name="Risk Taker",
        description="Lives on the edge — high investment risk, high reward potential, "
                    "elevated baseline stress from constant adrenaline.",
        action_multipliers={
            Action.INVEST_MONEY.value: 1.5,     # bigger wins AND losses
            Action.WORK_OVERTIME.value: 1.2,     # pushes harder at work
            Action.REST.value: 0.7,              # poor at resting
        },
        reward_bias=0.0,
        stress_modifier=2.0,          # always a bit more stressed
        investment_risk=1.8,          # high variance investments
        career_growth=1.1,
        work_output=1.2,
        social_effectiveness=0.9,     # slightly brash socially
    ),

    Personality.CONSERVATIVE: PersonalityProfile(
        name="Conservative",
        description="Plays it safe — low investment risk, stable but modest growth, "
                    "excels at maintaining relationships.",
        action_multipliers={
            Action.INVEST_MONEY.value: 0.6,     # small, safe investments
            Action.REST.value: 1.2,              # good at resting
            Action.SOCIALIZE.value: 1.1,
        },
        reward_bias=0.0,
        stress_modifier=-1.0,         # naturally calmer
        investment_risk=0.4,          # very low variance
        career_growth=0.8,            # slow but steady
        work_output=0.9,
        social_effectiveness=1.2,
    ),

    Personality.LAZY: PersonalityProfile(
        name="Lazy",
        description="Minimal effort — low work output, slow career progression, "
                    "but good at resting and low baseline stress.",
        action_multipliers={
            Action.WORK_OVERTIME.value: 0.5,    # half-hearted work
            Action.LEARN_SKILL.value: 0.6,      # barely studies
            Action.REST.value: 1.4,              # champion rester
            Action.EXERCISE.value: 0.6,          # couch potato
        },
        reward_bias=-0.02,            # slight penalisation for laziness
        stress_modifier=-2.0,         # low stress naturally
        investment_risk=0.8,
        career_growth=0.5,            # stagnant career
        work_output=0.6,
        social_effectiveness=1.0,
    ),

    Personality.AMBITIOUS: PersonalityProfile(
        name="Ambitious",
        description="Career-driven powerhouse — accelerated career and money growth, "
                    "but burns hot with elevated stress and weaker relationships.",
        action_multipliers={
            Action.WORK_OVERTIME.value: 1.4,
            Action.LEARN_SKILL.value: 1.5,
            Action.SOCIALIZE.value: 0.7,         # neglects social life
            Action.REST.value: 0.6,               # can't sit still
        },
        reward_bias=0.0,
        stress_modifier=3.0,          # constantly wired
        investment_risk=1.2,
        career_growth=1.6,            # rapid career growth
        work_output=1.4,
        social_effectiveness=0.7,
    ),

    Personality.BALANCED: PersonalityProfile(
        name="Balanced",
        description="Well-rounded individual — no extreme modifiers, "
                    "neutral across all dimensions. The default personality.",
        action_multipliers={},
        reward_bias=0.0,
        stress_modifier=0.0,
        investment_risk=1.0,
        career_growth=1.0,
        work_output=1.0,
        social_effectiveness=1.0,
    ),
}


def get_profile(personality: Personality) -> PersonalityProfile:
    """Retrieve the personality profile for a given type."""
    return PERSONALITY_PROFILES[personality]


def get_action_multiplier(profile: PersonalityProfile, action_name: str) -> float:
    """Return the action-specific multiplier, defaulting to 1.0 if unset."""
    return profile.action_multipliers.get(action_name, 1.0)
