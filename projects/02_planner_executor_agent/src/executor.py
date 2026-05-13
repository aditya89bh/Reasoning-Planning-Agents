"""Executor for the planner-executor agent.

The first prototype uses deterministic simulated execution. It executes plan
steps in order, checks dependencies, records step results, and produces a trace.
"""

from __future__ import annotations

from typing import Dict, List, Set

from .plan import ExecutionResult, Plan, StepResult


class PlanExecutor:
    """Execute a plan through deterministic simulation."""

    FAILURE_OUTPUTS = {
        "missing_audience",
        "tool_unavailable",
        "blocked_dependency",
        "draft_blocked",
    }

    def execute(self, plan: Plan, forced_failures: Dict[str, str] | None = None) -> ExecutionResult:
        """Execute all steps in a plan.

        Args:
            plan: Plan to execute.
            forced_failures: Optional mapping from step_id to error string.
        """

        forced_failures = forced_failures or {}
        completed_steps: Set[str] = set()
        step_results: List[StepResult] = []
        trace: List[str] = [f"Execution started: {plan.plan_id}"]

        for step in plan.steps:
            missing_dependencies = [
                dependency for dependency in step.dependencies if dependency not in completed_steps
            ]

            if missing_dependencies:
                result = StepResult(
                    result_id=f"result_{step.step_id}",
                    step_id=step.step_id,
                    status="blocked",
                    output="",
                    error="missing_dependencies:" + ",".join(missing_dependencies),
                    notes="Step blocked because dependencies were not completed.",
                )
                trace.append(
                    f"Step blocked: {step.step_id} missing dependencies {missing_dependencies}"
                )
                step_results.append(result)
                continue

            if step.step_id in forced_failures:
                error = forced_failures[step.step_id]
                result = StepResult(
                    result_id=f"result_{step.step_id}",
                    step_id=step.step_id,
                    status="failure",
                    output="",
                    error=error,
                    notes="Forced failure used for deterministic demo.",
                )
                trace.append(f"Step failed: {step.step_id} error={error}")
                step_results.append(result)
                continue

            result = StepResult(
                result_id=f"result_{step.step_id}",
                step_id=step.step_id,
                status="success",
                output=step.expected_output,
                error="",
                notes="Step completed successfully.",
            )
            completed_steps.add(step.step_id)
            trace.append(f"Step executed: {step.step_id} -> success -> {step.expected_output}")
            step_results.append(result)

        final_status = self._final_status(plan, step_results)
        trace.append(f"Final status: {final_status}")
        trace.append("Execution completed")

        return ExecutionResult(
            plan_id=plan.plan_id,
            goal_id=plan.goal_id,
            step_results=step_results,
            final_status=final_status,
            trace=trace,
        )

    def _final_status(self, plan: Plan, step_results: List[StepResult]) -> str:
        """Compute final plan status from step results."""

        if not plan.steps:
            return "empty"

        statuses = [result.status for result in step_results]
        if all(status == "success" for status in statuses) and len(step_results) == len(plan.steps):
            return "complete"
        if any(status == "failure" for status in statuses):
            return "failed"
        if any(status == "blocked" for status in statuses):
            return "blocked"
        return "partial"
