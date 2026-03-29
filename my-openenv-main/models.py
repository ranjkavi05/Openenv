"""
models.py — Data models for the LifeOS ✨.

Defines type-safe enums, dataclasses, and structured types used across
the entire simulation engine. All state representation, action definitions,
and event records live here.
"""

from __future__ import annotations
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any, Dict, List, Optional


# ─────────────────────────────────────────────
# Enums
# ─────────────────────────────────────────────

class Action(Enum):
    """Available actions the agent can take each step."""
    WORK_OVERTIME = "work_overtime"
    EXERCISE = "exercise"
    INVEST_MONEY = "invest_money"
    LEARN_SKILL = "learn_skill"
    SOCIALIZE = "socialize"
    REST = "rest"


class Personality(Enum):
    """Personality archetypes that modify simulation behavior."""
    RISK_TAKER = "risk_taker"
    CONSERVATIVE = "conservative"
    LAZY = "lazy"
    AMBITIOUS = "ambitious"
    BALANCED = "balanced"          # default / neutral


class Difficulty(Enum):
    """Difficulty levels controlling randomness and trade-offs."""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class TaskType(Enum):
    """Specific objectives for the OpenEnv agent benchmark."""
    WEALTH_BUILDER = "wealth_builder"
    CAREER_CLIMBER = "career_climber"
    PERFECT_BALANCE = "perfect_balance"


class EventType(Enum):
    """Types of random life events that can occur during simulation."""
    JOB_PROMOTION = "job_promotion"
    JOB_LOSS = "job_loss"
    MEDICAL_EMERGENCY = "medical_emergency"
    MARKET_CRASH = "market_crash"
    FAMILY_ISSUE = "family_issue"
    LOTTERY_WIN = "lottery_win"
    NATURAL_DISASTER = "natural_disaster"
    INHERITANCE = "inheritance"


# ─────────────────────────────────────────────
# Dataclasses
# ─────────────────────────────────────────────

@dataclass
class LifeState:
    """Complete snapshot of the simulated human's life at a point in time."""
    age: float = 25.0              # years
    health: float = 80.0           # 0–100
    money: float = 1000.0          # dollars (abstract)
    stress: float = 20.0           # 0–100
    career: float = 30.0           # 0–100
    relationships: float = 50.0    # 0–100
    happiness: float = 60.0        # 0–100

    # ── time tracking ──
    step_count: int = 0            # total steps taken
    week: int = 0                  # current week number

    def to_dict(self) -> Dict[str, Any]:
        """Serialize state to a plain dict."""
        return asdict(self)

    def copy(self) -> "LifeState":
        """Return a shallow copy."""
        return LifeState(**self.to_dict())

    @property
    def is_terminal(self) -> bool:
        """Check if the simulation has reached a terminal state."""
        return self.health <= 0 or self.stress >= 100


@dataclass
class EventRecord:
    """Record of a single random event that occurred during simulation."""
    event_type: EventType
    description: str
    effects: Dict[str, float]       # e.g. {"health": -20, "money": -500}
    step: int                        # step at which event occurred
    week: int                        # week at which event occurred


@dataclass
class StepResult:
    """Structured return from env.step(action)."""
    state: Dict[str, Any]
    reward: float
    done: bool
    info: Dict[str, Any]


@dataclass
class AgentDecision:
    """Captures an agent's decision plus reasoning (for UI display)."""
    action: Action
    reasoning: str
    state_before: Dict[str, Any]
    state_after: Optional[Dict[str, Any]] = None
    reward: float = 0.0
    step: int = 0


# ─────────────────────────────────────────────
# Constants
# ─────────────────────────────────────────────

# Default starting state values
DEFAULT_STATE = LifeState()

# All valid action names (for quick lookup)
VALID_ACTIONS = [a.value for a in Action]

# Observation space bounds for OpenEnv
OBSERVATION_BOUNDS = {
    "age":           (18.0, 100.0),
    "health":        (0.0, 100.0),
    "money":         (0.0, 100_000.0),
    "stress":        (0.0, 100.0),
    "career":        (0.0, 100.0),
    "relationships": (0.0, 100.0),
    "happiness":     (0.0, 100.0),
}
