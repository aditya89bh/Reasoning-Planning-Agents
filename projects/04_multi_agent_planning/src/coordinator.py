"""Coordinator for the multi-agent planning prototype.

The coordinator merges role contributions into one shared plan and resolves
simple conflicts deterministically. This keeps multi-agent planning inspectable
before adding LLM-based agent communication.
"""

from __future__ import annotations

from typing import Iterable, List

from .agent_role import (
    AgentContribution,
    AgentRole,
    CoordinationConflict,
    MultiAgentPlanningResult,
    SharedPlan,
)
from .conflict_detector import ConflictDetector


class MultiAgentCoordinator:
    """Coordinate role outputs into a shared plan."""

    DEFAULT_STEP_ORDER = [
        "define_audience",
        "create_outline",
        "write_draft",
        "review_clarity",
        "publish_article",
    ]

    def coordinate(
        self,
        goal_id: str,
        roles: List[AgentRole],
        contributions: List[AgentContribution],
        required_steps: Iterable[str] | None = None,
    ) -> MultiAgentPlanningResult:
        """Create a shared plan from role contributions."""

        required = list(required_steps or self.DEFAULT_STEP_ORDER)
        conflicts = ConflictDetector().detect(roles, contributions, required_steps=required)
        shared_steps = self._merge_steps(contributions, required, conflicts)
        resolved_conflicts = [conflict.conflict_id for conflict in conflicts]
        open_conflicts: List[str] = []

        shared_plan = SharedPlan(
            shared_plan_id=f"shared_plan_{goal_id}",
            goal_id=goal_id,
            roles_used=[role.role_id for role in roles],
            steps=shared_steps,
            resolved_conflicts=resolved_conflicts,
            open_conflicts=open_conflicts,
            status="valid" if not open_conflicts else "needs_review",
        )
        trace = self._build_trace(goal_id, roles, contributions, conflicts, shared_plan)

        return MultiAgentPlanningResult(
            goal_id=goal_id,
            roles=roles,
            contributions=contributions,
            conflicts=conflicts,
            shared_plan=shared_plan,
            trace=trace,
        )

    def _merge_steps(
        self,
        contributions: List[AgentContribution],
        required_steps: List[str],
        conflicts: List[CoordinationConflict],
    ) -> List[str]:
        """Merge role steps into a deterministic shared step order."""

        proposed_steps = []
        for contribution in contributions:
            proposed_steps.extend(contribution.proposed_steps)

        step_set = set(proposed_steps)
        for conflict in conflicts:
            if conflict.conflict_type == "missing_required_step":
                _, step = conflict.recommended_resolution.split(":", maxsplit=1)
                step_set.add(step)

        ordered_steps = [step for step in required_steps if step in step_set]
        extras = sorted(step for step in step_set if step not in required_steps)
        return ordered_steps + extras

    def _build_trace(
        self,
        goal_id: str,
        roles: List[AgentRole],
        contributions: List[AgentContribution],
        conflicts: List[CoordinationConflict],
        shared_plan: SharedPlan,
    ) -> List[str]:
        """Build an inspectable coordination trace."""

        trace = [
            f"Goal received: {goal_id}",
            f"Roles assigned: {', '.join(role.name for role in roles)}",
            f"Agent contributions received: {len(contributions)}",
            f"Conflicts detected: {len(conflicts)}",
        ]

        for conflict in conflicts:
            trace.append(
                f"Conflict detected: {conflict.conflict_type} -> {conflict.description}"
            )
            trace.append(
                f"Conflict resolution proposed: {conflict.recommended_resolution}"
            )

        trace.append(f"Shared plan created: {shared_plan.shared_plan_id}")
        trace.append(f"Shared plan steps: {', '.join(shared_plan.steps)}")
        trace.append(f"Shared plan status: {shared_plan.status}")
        trace.append("Coordination completed")
        return trace
