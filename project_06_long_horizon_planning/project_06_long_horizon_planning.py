# ============================================
# Project 06: Long-Horizon Planning Agent
# Full end-to-end minimal implementation
# ============================================

import time
import random
from dataclasses import dataclass, field
from typing import List, Dict, Optional
import json


# -----------------------------
# Data Models
# -----------------------------

@dataclass
class GoalState:
    goal: str
    confidence: float = 0.7
    active: bool = True
    progress: float = 0.0
    last_checkpoint_ts: float = field(default_factory=time.time)
    history: List[str] = field(default_factory=list)


@dataclass
class Checkpoint:
    description: str
    expected_progress: float


# -----------------------------
# Long-Horizon Planner
# -----------------------------

class LongHorizonPlanner:
    def __init__(self, replanning_threshold: float = 0.15):
        self.replanning_threshold = replanning_threshold

    def evaluate_progress(self, state: GoalState, checkpoint: Checkpoint) -> bool:
        """
        Returns True if progress is acceptable, False if drifting.
        """
        delta = checkpoint.expected_progress - state.progress
        return delta <= self.replanning_threshold

    def update_progress(self, state: GoalState):
        """
        Simulate incremental progress.
        """
        increment = random.uniform(0.05, 0.2)
        state.progress = min(1.0, state.progress + increment)
        state.history.append(f"progress_updated:{round(state.progress,2)}")
        state.last_checkpoint_ts = time.time()

    def replan(self, state: GoalState):
        """
        Adjust confidence and log replanning.
        """
        state.confidence -= 0.1
        state.history.append("replanning_triggered")
        if state.confidence < 0.3:
            state.active = False
            state.history.append("goal_abandoned")


# -----------------------------
# Demo Runner
# -----------------------------

goal_state = GoalState(
    goal="Build and ship a production-ready agent framework"
)

checkpoints = [
    Checkpoint("Initial prototype", 0.2),
    Checkpoint("Core projects complete", 0.5),
    Checkpoint("Integrated system", 0.75),
    Checkpoint("Production readiness", 0.95),
]

planner = LongHorizonPlanner()

print("\n=== LONG-HORIZON EXECUTION ===")

for cp in checkpoints:
    if not goal_state.active:
        print("\nGoal abandoned due to low confidence.")
        break

    planner.update_progress(goal_state)
    ok = planner.evaluate_progress(goal_state, cp)

    print(f"\nCheckpoint: {cp.description}")
    print(f"Expected ≥ {cp.expected_progress}, Actual = {round(goal_state.progress,2)}")

    if not ok:
        print("⚠️ Drift detected → replanning")
        planner.replan(goal_state)
    else:
        print("✅ On track")

print("\n=== FINAL GOAL STATE ===")
print(json.dumps(goal_state.__dict__, indent=2))
