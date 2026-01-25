# ============================================
# Project 05: Failure-Aware Planner
# Full end-to-end minimal implementation
# ============================================

import time
import random
from dataclasses import dataclass, asdict, field
from typing import List, Dict, Optional
import json


# -----------------------------
# Data Models
# -----------------------------

@dataclass
class FailureRecord:
    action: str
    cause: str
    ts: float


@dataclass
class Plan:
    goal: str
    actions: List[str]
    constraints: List[str] = field(default_factory=list)


# -----------------------------
# Failure Memory
# -----------------------------

def classify_failure(action: str) -> str:
    if "auth" in action:
        return "missing_credentials"
    if "deploy" in action:
        return "environment_mismatch"
    if "test" in action:
        return "incomplete_coverage"
    return "unknown_failure"


# -----------------------------
# Planner with Mutation
# -----------------------------

class FailureAwarePlanner:
    def __init__(self, failure_memory: FailureMemory):
        self.failure_memory = failure_memory

    def generate_plan(self, goal: str) -> Plan:
        # Base naive plan
        actions = [
            "check_logs",
            "fix_auth_issue",
            "deploy_fix",
            "run_tests"
        ]
        return Plan(goal=goal, actions=actions)

    def mutate_plan(self, plan: Plan) -> Plan:
        mutated = []
        constraints = list(plan.constraints)

        for a in plan.actions:
            if self.failure_memory.has_failed(a):
                constraints.append(f"avoid:{a}")
                # Replace with safer alternative
                mutated.append(f"review_{a}")
            else:
                mutated.append(a)

        return Plan(
            goal=plan.goal,
            actions=mutated,
            constraints=constraints
        )


# -----------------------------
# Execution Simulator
# -----------------------------

class Executor:
    def __init__(self, fail_rate: float = 0.25):
        self.fail_rate = fail_rate

    def execute(self, plan: Plan) -> Optional[FailureRecord]:
        for action in plan.actions:
            if random.random() < self.fail_rate:
                cause = classify_failure(action)
                return FailureRecord(action, cause, time.time())
        return None


# -----------------------------
# Demo Runner
# -----------------------------

failure_memory = FailureMemory()
planner = FailureAwarePlanner(failure_memory)
executor = Executor(fail_rate=0.35)

goal = "Fix API authentication bug"

print("\n--- FIRST ATTEMPT ---")
plan1 = planner.generate_plan(goal)
print("Plan:", plan1.actions)

failure = executor.execute(plan1)
if failure:
    print("Failed at:", failure.action, "| Cause:", failure.cause)
    failure_memory.record(failure.action, failure.cause)

print("\n--- SECOND ATTEMPT (FAILURE-AWARE) ---")
plan2 = planner.mutate_plan(plan1)
print("Plan:", plan2.actions)
print("Constraints:", plan2.constraints)

failure2 = executor.execute(plan2)
if failure2:
    print("Failed again at:", failure2.action, "| Cause:", failure2.cause)
else:
    print("Succeeded without repeating known failure")


