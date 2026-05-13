"""Run the multi-agent planning demo.

Usage:
    python projects/04_multi_agent_planning/run_demo.py

The demo loads deterministic agent roles and contributions, detects conflicts,
coordinates a shared plan, evaluates the result, and prints an inspectable trace.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict

from src.agent_role import AgentContribution, AgentRole
from src.coordinator import MultiAgentCoordinator
from src.evaluator import MultiAgentPlanningEvaluator


PROJECT_DIR = Path(__file__).resolve().parent
ROLES_PATH = PROJECT_DIR / "examples" / "demo_roles.json"


def load_demo(path: Path = ROLES_PATH) -> Dict:
    """Load demo role and contribution data."""

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def main() -> None:
    """Run the multi-agent planning demo."""

    demo = load_demo()
    goal_id = demo["goal_id"]
    required_steps = demo.get("required_steps", [])
    roles = [AgentRole.from_dict(item) for item in demo.get("roles", [])]
    contributions = [
        AgentContribution.from_dict(item) for item in demo.get("contributions", [])
    ]

    result = MultiAgentCoordinator().coordinate(
        goal_id=goal_id,
        roles=roles,
        contributions=contributions,
        required_steps=required_steps,
    )
    evaluation = MultiAgentPlanningEvaluator().evaluate(result)

    expected_shared_steps = demo.get("expected_shared_steps", [])
    expected_status = demo.get("expected_status", "unknown")
    matched_steps = result.shared_plan.steps == expected_shared_steps
    matched_status = result.shared_plan.status == expected_status

    print("=" * 72)
    print("Multi-Agent Planning Demo")
    print("=" * 72)
    print(f"Goal: {goal_id}")

    print("\nRoles:")
    for role in roles:
        print(f" - {role.role_id}: {role.name} -> {role.responsibility}")

    print("\nContributions:")
    for contribution in contributions:
        steps = ", ".join(contribution.proposed_steps) or "none"
        print(
            f" - {contribution.role_id}: steps=[{steps}], "
            f"confidence={contribution.confidence}"
        )

    print("\nConflicts:")
    if result.conflicts:
        for conflict in result.conflicts:
            print(
                f" - {conflict.conflict_id}: type={conflict.conflict_type}, "
                f"resolution={conflict.recommended_resolution}, status={conflict.status}"
            )
    else:
        print(" - none")

    print("\nShared plan:")
    print(result.shared_plan.to_dict())
    print(f"Matched expected steps: {matched_steps}")
    print(f"Matched expected status: {matched_status}")

    print("\nEvaluation:")
    print(evaluation.to_dict())

    print("\nTrace:")
    for step in result.trace:
        print(f" - {step}")

    print("\nSummary")
    print("=" * 72)
    print(
        f"goal={goal_id} | roles={len(roles)} | contributions={len(contributions)} | "
        f"conflicts={len(result.conflicts)} | status={result.shared_plan.status} | "
        f"success={evaluation.success} | trace={evaluation.trace_clarity}"
    )


if __name__ == "__main__":
    main()
