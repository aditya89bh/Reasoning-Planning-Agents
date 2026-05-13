"""Core task data models for the task decomposition agent.

The first prototype keeps the data structures explicit and inspectable. A goal
is decomposed into subtasks, dependencies, an execution order, and a trace.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass(frozen=True)
class Goal:
    """High-level objective supplied to the decomposition agent."""

    goal_id: str
    description: str
    success_criteria: List[str] = field(default_factory=list)
    constraints: List[str] = field(default_factory=list)
    context: Dict[str, str] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict) -> "Goal":
        """Create a Goal from dictionary data."""

        return cls(
            goal_id=data["goal_id"],
            description=data["description"],
            success_criteria=list(data.get("success_criteria", [])),
            constraints=list(data.get("constraints", [])),
            context=dict(data.get("context", {})),
        )

    def to_dict(self) -> Dict:
        """Serialize the goal to a dictionary."""

        return {
            "goal_id": self.goal_id,
            "description": self.description,
            "success_criteria": list(self.success_criteria),
            "constraints": list(self.constraints),
            "context": dict(self.context),
        }


@dataclass(frozen=True)
class Subtask:
    """Single decomposed unit of work."""

    subtask_id: str
    goal_id: str
    description: str
    expected_output: str
    dependencies: List[str] = field(default_factory=list)
    status: str = "pending"

    def to_dict(self) -> Dict:
        """Serialize the subtask to a dictionary."""

        return {
            "subtask_id": self.subtask_id,
            "goal_id": self.goal_id,
            "description": self.description,
            "expected_output": self.expected_output,
            "dependencies": list(self.dependencies),
            "status": self.status,
        }


@dataclass(frozen=True)
class Dependency:
    """Ordering relationship between two subtasks."""

    dependency_id: str
    before_subtask_id: str
    after_subtask_id: str
    reason: str

    def to_dict(self) -> Dict:
        """Serialize the dependency to a dictionary."""

        return {
            "dependency_id": self.dependency_id,
            "before_subtask_id": self.before_subtask_id,
            "after_subtask_id": self.after_subtask_id,
            "reason": self.reason,
        }


@dataclass(frozen=True)
class DecompositionResult:
    """Output of the task decomposition agent."""

    goal: Goal
    goal_type: str
    subtasks: List[Subtask]
    dependencies: List[Dependency]
    execution_order: List[str]
    trace: List[str]

    def to_dict(self) -> Dict:
        """Serialize the decomposition result to a dictionary."""

        return {
            "goal": self.goal.to_dict(),
            "goal_type": self.goal_type,
            "subtasks": [subtask.to_dict() for subtask in self.subtasks],
            "dependencies": [dependency.to_dict() for dependency in self.dependencies],
            "execution_order": list(self.execution_order),
            "trace": list(self.trace),
        }
