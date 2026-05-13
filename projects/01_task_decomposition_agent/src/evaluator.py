"""Evaluation utilities for the task decomposition agent.

The evaluator checks whether a decomposition is usable: clear goal, useful
subtasks, valid dependencies, valid execution order, and inspectable trace.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Set

from .task import DecompositionResult


@dataclass(frozen=True)
class DecompositionEvaluation:
    """Evaluation result for one decomposition."""

    goal_id: str
    success: bool
    goal_clarity: str
    subtask_count: int
    dependency_count: int
    dependency_valid: bool
    execution_order_valid: bool
    trace_clarity: str
    errors: List[str]
    warnings: List[str]

    def to_dict(self) -> Dict:
        """Serialize evaluation to dictionary."""

        return {
            "goal_id": self.goal_id,
            "success": self.success,
            "goal_clarity": self.goal_clarity,
            "subtask_count": self.subtask_count,
            "dependency_count": self.dependency_count,
            "dependency_valid": self.dependency_valid,
            "execution_order_valid": self.execution_order_valid,
            "trace_clarity": self.trace_clarity,
            "errors": list(self.errors),
            "warnings": list(self.warnings),
        }


class DecompositionEvaluator:
    """Evaluate decomposition quality and consistency."""

    def evaluate(self, result: DecompositionResult) -> DecompositionEvaluation:
        """Evaluate a decomposition result."""

        errors: List[str] = []
        warnings: List[str] = []

        goal_clarity = self._goal_clarity(result)
        if goal_clarity == "unclear":
            errors.append("goal_unclear")
        elif goal_clarity == "partial":
            warnings.append("goal_partially_specified")

        if not result.subtasks:
            errors.append("no_subtasks")

        dependency_valid = self._dependencies_valid(result, errors)
        execution_order_valid = self._execution_order_valid(result, errors)
        trace_clarity = self._trace_clarity(result)

        if trace_clarity == "low":
            warnings.append("trace_low_clarity")

        success = not errors

        return DecompositionEvaluation(
            goal_id=result.goal.goal_id,
            success=success,
            goal_clarity=goal_clarity,
            subtask_count=len(result.subtasks),
            dependency_count=len(result.dependencies),
            dependency_valid=dependency_valid,
            execution_order_valid=execution_order_valid,
            trace_clarity=trace_clarity,
            errors=errors,
            warnings=warnings,
        )

    def _goal_clarity(self, result: DecompositionResult) -> str:
        """Classify goal clarity."""

        goal = result.goal
        if not goal.description or len(goal.description.strip()) < 10:
            return "unclear"
        if not goal.success_criteria and not goal.context:
            return "partial"
        return "clear"

    def _dependencies_valid(self, result: DecompositionResult, errors: List[str]) -> bool:
        """Check whether dependencies reference valid subtasks."""

        subtask_ids: Set[str] = {subtask.subtask_id for subtask in result.subtasks}
        valid = True

        for dependency in result.dependencies:
            if dependency.before_subtask_id not in subtask_ids:
                errors.append(f"dependency_before_missing:{dependency.before_subtask_id}")
                valid = False
            if dependency.after_subtask_id not in subtask_ids:
                errors.append(f"dependency_after_missing:{dependency.after_subtask_id}")
                valid = False
            if dependency.before_subtask_id == dependency.after_subtask_id:
                errors.append(f"self_dependency:{dependency.before_subtask_id}")
                valid = False

        return valid

    def _execution_order_valid(self, result: DecompositionResult, errors: List[str]) -> bool:
        """Check whether execution order contains all subtasks and respects dependencies."""

        subtask_ids = [subtask.subtask_id for subtask in result.subtasks]
        order = result.execution_order

        if set(order) != set(subtask_ids):
            errors.append("execution_order_missing_or_extra_subtasks")
            return False

        if len(order) != len(set(order)):
            errors.append("execution_order_contains_duplicates")
            return False

        order_index = {subtask_id: index for index, subtask_id in enumerate(order)}
        for dependency in result.dependencies:
            before_index = order_index.get(dependency.before_subtask_id)
            after_index = order_index.get(dependency.after_subtask_id)
            if before_index is None or after_index is None:
                continue
            if before_index >= after_index:
                errors.append(f"dependency_order_invalid:{dependency.dependency_id}")
                return False

        return True

    def _trace_clarity(self, result: DecompositionResult) -> str:
        """Classify trace clarity."""

        trace_text = "\n".join(result.trace).lower()
        required_markers = [
            "goal received",
            "goal classified",
            "generated",
            "dependencies",
            "execution order",
        ]
        matched = sum(1 for marker in required_markers if marker in trace_text)

        if matched >= 5:
            return "high"
        if matched >= 3:
            return "medium"
        return "low"
