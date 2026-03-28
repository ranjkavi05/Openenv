"""
events.py — Dynamic real-world events system for the AI Digital Life Simulator.

Provides a probabilistic event engine that triggers life events during
simulation steps. Events affect multiple state variables and are logged
for replay and analysis.
"""

from __future__ import annotations
import random
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from models import EventType, EventRecord, Difficulty, LifeState


# ─────────────────────────────────────────────
# Event Definitions
# ─────────────────────────────────────────────

@dataclass
class EventDefinition:
    """Blueprint for a random life event."""
    event_type: EventType
    description: str
    base_probability: float               # 0–1, before difficulty scaling
    effects: Dict[str, float]             # state variable → delta
    min_age: float = 18.0                 # minimum age for eligibility
    cooldown_steps: int = 4               # minimum steps between repeats


# All possible events in the simulation
EVENT_CATALOG: List[EventDefinition] = [

    EventDefinition(
        event_type=EventType.JOB_PROMOTION,
        description="🎉 You got promoted! Career and pay rise.",
        base_probability=0.06,
        effects={"career": 15, "money": 300, "happiness": 10, "stress": 5},
        cooldown_steps=8,
    ),

    EventDefinition(
        event_type=EventType.JOB_LOSS,
        description="😰 You lost your job! Income drops and stress rises.",
        base_probability=0.04,
        effects={"career": -20, "money": -200, "stress": 20, "happiness": -15},
        cooldown_steps=10,
    ),

    EventDefinition(
        event_type=EventType.MEDICAL_EMERGENCY,
        description="🏥 Medical emergency! Health and savings take a hit.",
        base_probability=0.05,
        effects={"health": -25, "money": -500, "stress": 15, "happiness": -10},
        cooldown_steps=6,
    ),

    EventDefinition(
        event_type=EventType.MARKET_CRASH,
        description="📉 Market crash! Investments lose value.",
        base_probability=0.04,
        effects={"money": -400, "stress": 15, "happiness": -8},
        cooldown_steps=12,
    ),

    EventDefinition(
        event_type=EventType.FAMILY_ISSUE,
        description="👨‍👩‍👧 Family issue! Relationships and well-being suffer.",
        base_probability=0.06,
        effects={"relationships": -15, "stress": 12, "happiness": -10},
        cooldown_steps=5,
    ),

    EventDefinition(
        event_type=EventType.LOTTERY_WIN,
        description="🎰 Lucky day! You won a small lottery.",
        base_probability=0.02,
        effects={"money": 800, "happiness": 15, "stress": -5},
        cooldown_steps=20,
    ),

    EventDefinition(
        event_type=EventType.NATURAL_DISASTER,
        description="🌪️ Natural disaster! Property and health impacted.",
        base_probability=0.03,
        effects={"health": -10, "money": -300, "stress": 20, "happiness": -12},
        cooldown_steps=15,
    ),

    EventDefinition(
        event_type=EventType.INHERITANCE,
        description="💰 You received an inheritance! Financial windfall.",
        base_probability=0.02,
        effects={"money": 1000, "happiness": 10, "relationships": 5},
        min_age=30.0,
        cooldown_steps=50,
    ),
]


# ─────────────────────────────────────────────
# Difficulty → probability scale
# ─────────────────────────────────────────────

DIFFICULTY_SCALE = {
    Difficulty.EASY: 0.0,          # no random events
    Difficulty.MEDIUM: 1.0,        # normal probability
    Difficulty.HARD: 1.8,          # almost double event frequency
}


# ─────────────────────────────────────────────
# Event System Engine
# ─────────────────────────────────────────────

class EventSystem:
    """Probabilistic event engine for the life simulator.

    Manages event triggering, cooldowns, and logging.
    """

    def __init__(self, difficulty: Difficulty = Difficulty.MEDIUM,
                 rng: Optional[random.Random] = None):
        self.difficulty = difficulty
        self.scale = DIFFICULTY_SCALE[difficulty]
        self.rng = rng or random.Random()
        self.event_log: List[EventRecord] = []
        # Track last step each event fired (for cooldowns)
        self._last_fired: Dict[EventType, int] = {}

    def reset(self) -> None:
        """Clear event log and cooldowns."""
        self.event_log.clear()
        self._last_fired.clear()

    def check_events(self, state: LifeState) -> List[EventRecord]:
        """Roll for each eligible event and return those that trigger.

        Called once per simulation step. Applies difficulty scaling,
        cooldown logic, and age eligibility.
        """
        if self.scale == 0.0:
            return []                      # easy mode → no events

        triggered: List[EventRecord] = []
        for edef in EVENT_CATALOG:
            # Age eligibility
            if state.age < edef.min_age:
                continue
            # Cooldown check
            last = self._last_fired.get(edef.event_type, -999)
            if state.step_count - last < edef.cooldown_steps:
                continue
            # Probability roll (scaled by difficulty)
            prob = edef.base_probability * self.scale
            if self.rng.random() < prob:
                record = EventRecord(
                    event_type=edef.event_type,
                    description=edef.description,
                    effects=dict(edef.effects),
                    step=state.step_count,
                    week=state.week,
                )
                triggered.append(record)
                self._last_fired[edef.event_type] = state.step_count

        # Log all triggered events
        self.event_log.extend(triggered)
        return triggered

    def apply_events(self, state: LifeState,
                     events: List[EventRecord]) -> LifeState:
        """Apply the effects of triggered events to a LifeState (mutates in-place)."""
        for event in events:
            for attr, delta in event.effects.items():
                if hasattr(state, attr):
                    current = getattr(state, attr)
                    setattr(state, attr, current + delta)
        return state

    def get_log(self) -> List[Dict]:
        """Return the full event log as a list of dicts."""
        return [
            {
                "event": rec.event_type.value,
                "description": rec.description,
                "effects": rec.effects,
                "step": rec.step,
                "week": rec.week,
            }
            for rec in self.event_log
        ]
