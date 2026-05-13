"""Planner for the planner-executor agent.

The first prototype loads structured plan specifications and converts them into
explicit Plan objects. Planning remains deterministic so the loop is inspectable.
"""

from __future__ import annotations

from typing import Dict, List

from .plan import Plan, PlanStep


class Planner:
    """Create executable plans from structured plan specs."""

    def build_plan(self, plan_spec: Dict) -> Plan:
        """Build a Plan from a structured dictionary."""

        plan_id = plan_spec["plan_id"]
        steps: List[PlanStep] = []

        for raw_step in plan_spec.get("steps", []):
            steps.append(
                PlanStep(
                    step_id=raw_step["step_id"],
                    plan_id=plan_id,
                    description=raw_step["description"],
                    expected_output=raw_step.get("expected_output", ""),
                    dependencies=list(raw_step.get("dependencies", [])),
                    status=raw_step.get("status", "pending"),
                )
            )

        return Plan(
            plan_id=plan_id,
            goal_id=plan_spec["goal_id"],
            description=plan_spec.get("description", ""),
            steps=steps,
            assumptions=list(plan_spec.get("assumptions", [])),
            risks=list(plan_spec.get("risks", [])),
            status=plan_spec.get("status", "ready"),
            version=int(plan_spec.get("version", 1)),
        )

    def build_trace(self, plan: Plan) -> List[str]:
        """Build a planning trace."""

        return [
            f"Plan created: {plan.plan_id}",
            f"Goal: {plan.goal_id}",
            f"Steps: {len(plan.steps)}",
            f"Assumptions: {len(plan.assumptions)}",
            f"Risks: {len(plan.risks)}",
            f"Plan status: {plan.status}",
        ]

    def validate_plan_structure(self, plan: Plan) -> List[str]:
        """Return structural validation errors for a plan."""

        errors: List[str] = []

        if not plan.plan_id:
            errors.append("missing_plan_id")
        if not plan.goal_id:
            errors.append("missing_goal_id")
        if not plan.steps:
            errors.append("no_plan_steps")

        step_ids = [step.step_id for step in plan.steps]
        if len(step_ids) != len(set(step_ids)):
            errors.append("duplicate_step_ids")

        step_id_set = set(step_ids)
        for step in plan.steps:
            for dependency in step.dependencies:
                if dependency not in step_id_set:
                    errors.append(f"missing_step_dependency:{step.step_id}:{dependency}")
            if step.step_id in step.dependencies:
                errors.append(f"self_dependency:{step.step_id}")

        return errors
