"""Core plan data models for the planner-executor agent.

The planner-executor prototype converts subtasks into an ordered plan, simulates
step execution, records results, and produces an inspectable trace.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass(frozen=True)
class PlanStep:
    """Single executable step inside a plan."""

    step_id: str
    plan_id: str
    description: str
    expected_output: str
    dependencies: List[str] = field(default_factory=list)
    status: str = "pending"

    def to_dict(self) -> Dict:
        """Serialize plan step to dictionary."""

        return {
            "step_id": self.step_id,
            "plan_id": self.plan_id,
            "description": self.description,
            "expected_output": self.expected_output,
            "dependencies": list(self.dependencies),
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "PlanStep":
        """Create PlanStep from dictionary data."""

        return cls(
            step_id=data["step_id"],
            plan_id=data["plan_id"],
            description=data["description"],
            expected_output=data.get("expected_output", ""),
            dependencies=list(data.get("dependencies", [])),
            status=data.get("status", "pending"),
        )


@dataclass(frozen=True)
class Plan:
    """Executable plan with ordered steps."""

    plan_id: str
    goal_id: str
    description: str
    steps: List[PlanStep]
    assumptions: List[str] = field(default_factory=list)
    risks: List[str] = field(default_factory=list)
    status: str = "ready"
    version: int = 1

    def to_dict(self) -> Dict:
        """Serialize plan to dictionary."""

        return {
            "plan_id": self.plan_id,
            "goal_id": self.goal_id,
            "description": self.description,
            "steps": [step.to_dict() for step in self.steps],
            "assumptions": list(self.assumptions),
            "risks": list(self.risks),
            "status": self.status,
            "version": self.version,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "Plan":
        """Create Plan from dictionary data."""

        return cls(
            plan_id=data["plan_id"],
            goal_id=data["goal_id"],
            description=data.get("description", ""),
            steps=[PlanStep.from_dict(item) for item in data.get("steps", [])],
            assumptions=list(data.get("assumptions", [])),
            risks=list(data.get("risks", [])),
            status=data.get("status", "ready"),
            version=int(data.get("version", 1)),
        )


@dataclass(frozen=True)
class StepResult:
    """Result of executing a single plan step."""

    result_id: str
    step_id: str
    status: str
    output: str = ""
    error: str = ""
    notes: str = ""

    def to_dict(self) -> Dict:
        """Serialize step result to dictionary."""

        return {
            "result_id": self.result_id,
            "step_id": self.step_id,
            "status": self.status,
            "output": self.output,
            "error": self.error,
            "notes": self.notes,
        }


@dataclass(frozen=True)
class ExecutionResult:
    """Full execution output for a plan."""

    plan_id: str
    goal_id: str
    step_results: List[StepResult]
    final_status: str
    trace: List[str]

    def to_dict(self) -> Dict:
        """Serialize execution result to dictionary."""

        return {
            "plan_id": self.plan_id,
            "goal_id": self.goal_id,
            "step_results": [result.to_dict() for result in self.step_results],
            "final_status": self.final_status,
            "trace": list(self.trace),
        }
