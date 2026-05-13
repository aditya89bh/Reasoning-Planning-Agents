"""Evaluation utilities for the multi-agent planning prototype.

The evaluator checks whether roles are distinct, contributions exist, conflicts
are handled, the shared plan is valid, and the coordination trace is inspectable.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Set

from .agent_role import MultiAgentPlanningResult


@dataclass(frozen=True)
class MultiAgentPlanningEvaluation:
    """Evaluation result for one multi-agent planning run."""

    goal_id: str
    success: bool
    role_count: int
    contribution_count: int
    role_clarity: bool
    conflict_count: int
    open_conflict_count: int
    shared_plan_valid: bool
    trace_clarity: str
    errors: List[str]
    warnings: List[str]

    def to_dict(self) -> Dict:
        """Serialize evaluation to dictionary."""

        return {
            "goal_id": self.goal_id,
            "success": self.success,
            "role_count": self.role_count,
            "contribution_count": self.contribution_count,
            "role_clarity": self.role_clarity,
            "conflict_count": self.conflict_count,
            "open_conflict_count": self.open_conflict_count,
            "shared_plan_valid": self.shared_plan_valid,
            "trace_clarity": self.trace_clarity,
            "errors": list(self.errors),
            "warnings": list(self.warnings),
        }


class MultiAgentPlanningEvaluator:
    """Evaluate multi-agent planning output."""

    def evaluate(self, result: MultiAgentPlanningResult) -> MultiAgentPlanningEvaluation:
        """Evaluate a multi-agent planning result."""

        errors: List[str] = []
        warnings: List[str] = []

        role_clarity = self._role_clarity(result, errors)
        if not result.contributions:
            errors.append("no_agent_contributions")

        contribution_role_ids = {contribution.role_id for contribution in result.contributions}
        role_ids = {role.role_id for role in result.roles}
        missing_contribution_roles = sorted(role_ids - contribution_role_ids)
        if missing_contribution_roles:
            warnings.append("roles_without_contributions:" + ",".join(missing_contribution_roles))

        open_conflict_count = len(result.shared_plan.open_conflicts)
        if open_conflict_count:
            errors.append("open_conflicts_remaining")

        shared_plan_valid = self._shared_plan_valid(result, errors)
        trace_clarity = self._trace_clarity(result)
        if trace_clarity == "low":
            warnings.append("trace_low_clarity")

        success = not errors

        return MultiAgentPlanningEvaluation(
            goal_id=result.goal_id,
            success=success,
            role_count=len(result.roles),
            contribution_count=len(result.contributions),
            role_clarity=role_clarity,
            conflict_count=len(result.conflicts),
            open_conflict_count=open_conflict_count,
            shared_plan_valid=shared_plan_valid,
            trace_clarity=trace_clarity,
            errors=errors,
            warnings=warnings,
        )

    def _role_clarity(self, result: MultiAgentPlanningResult, errors: List[str]) -> bool:
        """Check that roles have unique IDs and responsibilities."""

        role_ids = [role.role_id for role in result.roles]
        if len(role_ids) != len(set(role_ids)):
            errors.append("duplicate_role_ids")
            return False

        responsibilities = [role.responsibility.strip().lower() for role in result.roles]
        if len(responsibilities) != len(set(responsibilities)):
            errors.append("duplicate_role_responsibilities")
            return False

        if any(not role.responsibility.strip() for role in result.roles):
            errors.append("missing_role_responsibility")
            return False

        return True

    def _shared_plan_valid(self, result: MultiAgentPlanningResult, errors: List[str]) -> bool:
        """Check shared plan structure."""

        if not result.shared_plan.steps:
            errors.append("shared_plan_has_no_steps")
            return False

        if result.shared_plan.status not in {"valid", "needs_review"}:
            errors.append("invalid_shared_plan_status")
            return False

        if result.shared_plan.goal_id != result.goal_id:
            errors.append("shared_plan_goal_mismatch")
            return False

        role_ids: Set[str] = {role.role_id for role in result.roles}
        if not set(result.shared_plan.roles_used).issubset(role_ids):
            errors.append("shared_plan_uses_unknown_roles")
            return False

        return True

    def _trace_clarity(self, result: MultiAgentPlanningResult) -> str:
        """Classify coordination trace clarity."""

        trace_text = "\n".join(result.trace).lower()
        required_markers = [
            "goal received",
            "roles assigned",
            "agent contributions received",
            "conflicts detected",
            "shared plan created",
            "coordination completed",
        ]
        matched = sum(1 for marker in required_markers if marker in trace_text)

        if matched >= 6:
            return "high"
        if matched >= 3:
            return "medium"
        return "low"
