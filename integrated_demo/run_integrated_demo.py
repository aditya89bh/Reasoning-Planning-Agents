"""Run the integrated reasoning-planning demo.

Usage:
    python integrated_demo/run_integrated_demo.py

This demo connects the four project prototypes:

1. Project 01 decomposes a goal.
2. Project 02 executes a plan with a forced failure.
3. Project 03 reflects on the failure and proposes a revision.
4. Project 04 coordinates role contributions into a shared plan.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType


REPO_ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path) -> ModuleType:
    """Load a Python module from a file path without relying on package imports."""

    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load module: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# Project 01 modules
p1_task = load_module(
    "p1_task",
    REPO_ROOT / "projects" / "01_task_decomposition_agent" / "src" / "task.py",
)
p1_decomposer = load_module(
    "p1_decomposer",
    REPO_ROOT / "projects" / "01_task_decomposition_agent" / "src" / "decomposer.py",
)

# Project 02 modules
p2_plan = load_module(
    "p2_plan",
    REPO_ROOT / "projects" / "02_planner_executor_agent" / "src" / "plan.py",
)
p2_planner = load_module(
    "p2_planner",
    REPO_ROOT / "projects" / "02_planner_executor_agent" / "src" / "planner.py",
)
p2_executor = load_module(
    "p2_executor",
    REPO_ROOT / "projects" / "02_planner_executor_agent" / "src" / "executor.py",
)

# Project 03 modules
p3_reflection = load_module(
    "p3_reflection",
    REPO_ROOT / "projects" / "03_reflection_agent" / "src" / "reflection.py",
)
p3_analyzer = load_module(
    "p3_analyzer",
    REPO_ROOT / "projects" / "03_reflection_agent" / "src" / "failure_analyzer.py",
)
p3_reviser = load_module(
    "p3_reviser",
    REPO_ROOT / "projects" / "03_reflection_agent" / "src" / "reviser.py",
)

# Project 04 modules
p4_agent_role = load_module(
    "p4_agent_role",
    REPO_ROOT / "projects" / "04_multi_agent_planning" / "src" / "agent_role.py",
)
p4_coordinator = load_module(
    "p4_coordinator",
    REPO_ROOT / "projects" / "04_multi_agent_planning" / "src" / "coordinator.py",
)


def build_goal():
    """Create the integrated demo goal."""

    return p1_task.Goal(
        goal_id="goal_publish_blog_integrated",
        description="Publish a technical blog post about planning agents for AI builders.",
        success_criteria=[
            "audience_defined",
            "outline_created",
            "draft_written",
            "review_completed",
            "article_published",
        ],
        constraints=["technical_but_readable", "under_1200_words"],
        context={"audience": "AI builders", "format": "blog post"},
    )


def build_plan_from_decomposition(decomposition):
    """Convert Project 01 decomposition output into a Project 02 plan spec."""

    steps = []
    for subtask in decomposition.subtasks:
        dependency_ids = []
        for dependency in decomposition.dependencies:
            if dependency.after_subtask_id == subtask.subtask_id:
                dependency_ids.append(dependency.before_subtask_id.replace("subtask_", "step_"))
        steps.append(
            {
                "step_id": subtask.subtask_id.replace("subtask_", "step_"),
                "description": subtask.description,
                "expected_output": subtask.expected_output,
                "dependencies": dependency_ids,
            }
        )

    return {
        "plan_id": "plan_integrated_publish_blog_v1",
        "goal_id": decomposition.goal.goal_id,
        "description": "Integrated publishing plan generated from decomposition output.",
        "assumptions": ["publishing workflow is sequential"],
        "risks": ["audience definition may fail"],
        "status": "ready",
        "version": 1,
        "steps": steps,
    }


def build_observation_from_failure(execution):
    """Convert the first failed Project 02 step result into a Project 03 observation."""

    failed = next(result for result in execution.step_results if result.status == "failure")
    return p3_reflection.Observation(
        observation_id=f"obs_{failed.step_id}",
        step_id=failed.step_id,
        status=failed.status,
        observed_output=failed.output,
        observed_error=failed.error,
        state_change="execution_failed",
        notes="Observation generated from integrated planner-executor failure.",
    )


def build_roles_and_contributions(revision):
    """Build Project 04 roles and contributions using the Project 03 revision signal."""

    roles = [
        p4_agent_role.AgentRole(
            role_id="role_decomposer",
            name="Decomposer",
            responsibility="Break the goal into clear subtasks.",
            inputs=["goal"],
            outputs=["subtasks"],
        ),
        p4_agent_role.AgentRole(
            role_id="role_planner",
            name="Planner",
            responsibility="Order subtasks into an executable plan.",
            inputs=["subtasks"],
            outputs=["ordered_plan"],
        ),
        p4_agent_role.AgentRole(
            role_id="role_critic",
            name="Critic",
            responsibility="Use reflection signals to detect missing or weak steps.",
            inputs=["reflection", "revision"],
            outputs=["conflict_report"],
        ),
        p4_agent_role.AgentRole(
            role_id="role_coordinator",
            name="Coordinator",
            responsibility="Merge role outputs into one shared plan.",
            inputs=["subtasks", "ordered_plan", "conflict_report"],
            outputs=["shared_plan"],
        ),
    ]

    critic_steps = []
    if revision.revision_type == "add_step" and "audience" in revision.change_summary.lower():
        critic_steps.append("define_audience")

    contributions = [
        p4_agent_role.AgentContribution(
            contribution_id="contrib_decomposer_integrated",
            role_id="role_decomposer",
            goal_id="goal_publish_blog_integrated",
            proposed_steps=["create_outline", "write_draft", "review_clarity", "publish_article"],
            risks=["audience definition may be missing"],
            confidence=0.8,
        ),
        p4_agent_role.AgentContribution(
            contribution_id="contrib_planner_integrated",
            role_id="role_planner",
            goal_id="goal_publish_blog_integrated",
            proposed_steps=["create_outline", "write_draft", "review_clarity", "publish_article"],
            risks=["plan may need audience prerequisite"],
            confidence=0.78,
        ),
        p4_agent_role.AgentContribution(
            contribution_id="contrib_critic_integrated",
            role_id="role_critic",
            goal_id="goal_publish_blog_integrated",
            proposed_steps=critic_steps,
            assumptions=["reflection revision should influence the shared plan"],
            confidence=0.9,
        ),
        p4_agent_role.AgentContribution(
            contribution_id="contrib_coordinator_integrated",
            role_id="role_coordinator",
            goal_id="goal_publish_blog_integrated",
            proposed_steps=[],
            confidence=0.85,
        ),
    ]
    return roles, contributions


def main() -> None:
    """Run the integrated demo."""

    goal = build_goal()
    decomposition = p1_decomposer.TaskDecomposer().decompose(goal)

    plan_spec = build_plan_from_decomposition(decomposition)
    plan = p2_planner.Planner().build_plan(plan_spec)
    execution = p2_executor.PlanExecutor().execute(
        plan,
        forced_failures={"step_define_audience": "missing_audience"},
    )

    observation = build_observation_from_failure(execution)
    reflection = p3_analyzer.FailureAnalyzer().analyze(observation)
    revision = p3_reviser.PlanReviser().revise(reflection, old_plan_id=plan.plan_id)

    roles, contributions = build_roles_and_contributions(revision)
    coordination = p4_coordinator.MultiAgentCoordinator().coordinate(
        goal_id=goal.goal_id,
        roles=roles,
        contributions=contributions,
        required_steps=[
            "define_audience",
            "create_outline",
            "write_draft",
            "review_clarity",
            "publish_article",
        ],
    )

    trace = [
        "Integrated demo started",
        f"Goal decomposed as: {decomposition.goal_type}",
        f"Subtasks generated: {len(decomposition.subtasks)}",
        f"Plan executed with final status: {execution.final_status}",
        f"Failure observed: {observation.observed_error}",
        f"Reflection recommendation: {reflection.recommended_revision}",
        f"Revision proposed: {revision.revision_type} -> {revision.change_summary}",
        f"Shared plan status: {coordination.shared_plan.status}",
        f"Shared plan steps: {', '.join(coordination.shared_plan.steps)}",
        "Integrated demo completed",
    ]

    print("=" * 72)
    print("Integrated Reasoning-Planning Demo")
    print("=" * 72)
    for item in trace:
        print(f" - {item}")

    print("\nFinal shared plan:")
    print(coordination.shared_plan.to_dict())


if __name__ == "__main__":
    main()
