"""Run the task decomposition agent demo.

Usage:
    python projects/01_task_decomposition_agent/run_demo.py

The demo loads structured goals, decomposes them into subtasks and dependencies,
creates an execution order, evaluates the result, and prints an inspectable trace.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List

from src.decomposer import TaskDecomposer
from src.evaluator import DecompositionEvaluator
from src.task import Goal


PROJECT_DIR = Path(__file__).resolve().parent
GOALS_PATH = PROJECT_DIR / "examples" / "demo_goals.json"


def load_goals(path: Path = GOALS_PATH) -> List[Goal]:
    """Load demo goals from JSON."""

    with path.open("r", encoding="utf-8") as file:
        raw_goals = json.load(file)
    return [Goal.from_dict(item) for item in raw_goals]


def run_goal(goal: Goal, decomposer: TaskDecomposer, evaluator: DecompositionEvaluator) -> Dict:
    """Run one goal through decomposition and evaluation."""

    result = decomposer.decompose(goal)
    evaluation = evaluator.evaluate(result)

    print("\n" + "=" * 72)
    print(f"Goal: {goal.goal_id}")
    print(f"Description: {goal.description}")
    print(f"Goal type: {result.goal_type}")

    print("\nSubtasks:")
    for subtask in result.subtasks:
        dependencies = ", ".join(subtask.dependencies) if subtask.dependencies else "none"
        print(
            f" - {subtask.subtask_id}: {subtask.description} "
            f"-> {subtask.expected_output} | dependencies={dependencies}"
        )

    print("\nDependencies:")
    for dependency in result.dependencies:
        print(
            f" - {dependency.before_subtask_id} -> {dependency.after_subtask_id}: "
            f"{dependency.reason}"
        )

    print("\nExecution order:")
    for index, subtask_id in enumerate(result.execution_order, start=1):
        print(f" {index}. {subtask_id}")

    print("\nEvaluation:")
    print(evaluation.to_dict())

    print("\nTrace:")
    for step in result.trace:
        print(f" - {step}")

    row = evaluation.to_dict()
    row["goal_type"] = result.goal_type
    return row


def print_summary(rows: List[Dict]) -> None:
    """Print compact summary for all demo goals."""

    print("\n" + "=" * 72)
    print("Summary")
    print("=" * 72)

    for row in rows:
        print(
            f"{row['goal_id']:<26} | "
            f"type={row['goal_type']:<16} | "
            f"success={str(row['success']):<5} | "
            f"subtasks={row['subtask_count']} | "
            f"deps_valid={row['dependency_valid']} | "
            f"order_valid={row['execution_order_valid']} | "
            f"trace={row['trace_clarity']}"
        )

    if rows:
        success_rate = sum(row["success"] for row in rows) / len(rows)
        print(f"\ndecomposition_success_rate={success_rate:.3f}")


def main() -> None:
    """Run all task decomposition demo goals."""

    goals = load_goals()
    decomposer = TaskDecomposer()
    evaluator = DecompositionEvaluator()
    rows = [run_goal(goal, decomposer, evaluator) for goal in goals]
    print_summary(rows)


if __name__ == "__main__":
    main()
