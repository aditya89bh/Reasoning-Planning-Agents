"""Run the planner-executor agent demo.

Usage:
    python projects/02_planner_executor_agent/run_demo.py

The demo loads structured plans, builds Plan objects, simulates execution,
evaluates results, and prints an inspectable execution trace.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List

from src.evaluator import PlanExecutionEvaluator
from src.executor import PlanExecutor
from src.planner import Planner


PROJECT_DIR = Path(__file__).resolve().parent
PLANS_PATH = PROJECT_DIR / "examples" / "demo_plans.json"


def load_plan_specs(path: Path = PLANS_PATH) -> List[Dict]:
    """Load demo plan specs from JSON."""

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def run_plan(plan_spec: Dict, planner: Planner, executor: PlanExecutor, evaluator: PlanExecutionEvaluator) -> Dict:
    """Run one plan through planning, execution, and evaluation."""

    plan = planner.build_plan(plan_spec)
    planning_trace = planner.build_trace(plan)
    execution = executor.execute(plan, forced_failures=plan_spec.get("forced_failures", {}))
    evaluation = evaluator.evaluate(plan, execution)
    expected_final_status = plan_spec.get("expected_final_status", "unknown")
    matched_expected = execution.final_status == expected_final_status

    print("\n" + "=" * 72)
    print(f"Plan: {plan.plan_id}")
    print(f"Goal: {plan.goal_id}")
    print(f"Description: {plan.description}")
    print(f"Expected final status: {expected_final_status}")

    print("\nPlan steps:")
    for step in plan.steps:
        dependencies = ", ".join(step.dependencies) if step.dependencies else "none"
        print(
            f" - {step.step_id}: {step.description} -> {step.expected_output} | "
            f"dependencies={dependencies}"
        )

    print("\nStep results:")
    for result in execution.step_results:
        print(
            f" - {result.step_id}: status={result.status}, output={result.output or 'none'}, "
            f"error={result.error or 'none'}"
        )

    print("\nPlanning trace:")
    for step in planning_trace:
        print(f" - {step}")

    print("\nExecution trace:")
    for step in execution.trace:
        print(f" - {step}")

    print("\nEvaluation:")
    print(evaluation.to_dict())
    print(f"Matched expected final status: {matched_expected}")

    row = evaluation.to_dict()
    row["expected_final_status"] = expected_final_status
    row["matched_expected_final_status"] = matched_expected
    return row


def print_summary(rows: List[Dict]) -> None:
    """Print compact summary for all demo plans."""

    print("\n" + "=" * 72)
    print("Summary")
    print("=" * 72)

    for row in rows:
        print(
            f"{row['plan_id']:<36} | "
            f"status={row['final_status']:<8} | "
            f"expected={row['expected_final_status']:<8} | "
            f"matched={row['matched_expected_final_status']} | "
            f"success_steps={row['successful_steps']}/{row['step_count']} | "
            f"trace={row['trace_clarity']}"
        )

    if rows:
        match_rate = sum(row["matched_expected_final_status"] for row in rows) / len(rows)
        print(f"\nfinal_status_match_rate={match_rate:.3f}")


def main() -> None:
    """Run all planner-executor demo plans."""

    specs = load_plan_specs()
    planner = Planner()
    executor = PlanExecutor()
    evaluator = PlanExecutionEvaluator()
    rows = [run_plan(spec, planner, executor, evaluator) for spec in specs]
    print_summary(rows)


if __name__ == "__main__":
    main()
