"""Evaluation utilities for the planner-executor agent.

The evaluator checks whether a plan is structurally valid and whether execution
results are complete, visible, and traceable.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

from .plan import ExecutionResult, Plan
from .planner import Planner


@dataclass(frozen=True)
class PlanExecutionEvaluation:
    """Evaluation result for a plan execution run."""

    plan_id: str
    success: bool
    plan_valid: bool
    step_count: int
    successful_steps: int
    failed_steps: int
    blocked_steps: int
    final_status: str
    trace_clarity: str
    errors: List[str]
    warnings: List[str]

    def to_dict(self) -> Dict:
        """Serialize evaluation to dictionary."""

        return {
            "plan_id": self.plan_id,
            "success": self.success,
            "plan_valid": self.plan_valid,
            "step_count": self.step_count,
            "successful_steps": self.successful_steps,
            "failed_steps": self.failed_steps,
            "blocked_steps": self.blocked_steps,
            "final_status": self.final_status,
            "trace_clarity": self.trace_clarity,
            "errors": list(self.errors),
            "warnings": list(self.warnings),
        }


class PlanExecutionEvaluator:
    """Evaluate plan structure and execution results."""

    def evaluate(self, plan: Plan, execution: ExecutionResult) -> PlanExecutionEvaluation:
        """Evaluate a plan and its execution result."""

        errors: List[str] = []
        warnings: List[str] = []

        structure_errors = Planner().validate_plan_structure(plan)
        errors.extend(structure_errors)
        plan_valid = not structure_errors

        if execution.plan_id != plan.plan_id:
            errors.append("execution_plan_id_mismatch")
        if execution.goal_id != plan.goal_id:
            errors.append("execution_goal_id_mismatch")

        step_ids = {step.step_id for step in plan.steps}
        result_step_ids = [result.step_id for result in execution.step_results]

        if set(result_step_ids) != step_ids:
            errors.append("execution_results_do_not_match_plan_steps")

        if len(result_step_ids) != len(set(result_step_ids)):
            errors.append("duplicate_step_results")

        successful_steps = sum(1 for result in execution.step_results if result.status == "success")
        failed_steps = sum(1 for result in execution.step_results if result.status == "failure")
        blocked_steps = sum(1 for result in execution.step_results if result.status == "blocked")

        if failed_steps and execution.final_status != "failed":
            errors.append("final_status_should_be_failed")
        if blocked_steps and not failed_steps and execution.final_status != "blocked":
            errors.append("final_status_should_be_blocked")
        if successful_steps == len(plan.steps) and execution.final_status != "complete":
            errors.append("final_status_should_be_complete")

        trace_clarity = self._trace_clarity(execution)
        if trace_clarity == "low":
            warnings.append("trace_low_clarity")

        success = not errors and execution.final_status == "complete"

        return PlanExecutionEvaluation(
            plan_id=plan.plan_id,
            success=success,
            plan_valid=plan_valid,
            step_count=len(plan.steps),
            successful_steps=successful_steps,
            failed_steps=failed_steps,
            blocked_steps=blocked_steps,
            final_status=execution.final_status,
            trace_clarity=trace_clarity,
            errors=errors,
            warnings=warnings,
        )

    def _trace_clarity(self, execution: ExecutionResult) -> str:
        """Classify execution trace clarity."""

        trace_text = "\n".join(execution.trace).lower()
        required_markers = [
            "execution started",
            "step executed",
            "final status",
            "execution completed",
        ]
        matched = sum(1 for marker in required_markers if marker in trace_text)

        if matched >= 4:
            return "high"
        if matched >= 2:
            return "medium"
        return "low"
