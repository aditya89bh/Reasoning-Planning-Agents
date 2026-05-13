"""Tests for the task decomposition agent.

Run from the repository root with:
    python -m pytest projects/01_task_decomposition_agent/tests
"""

from pathlib import Path
import sys

PROJECT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_DIR))

from src.decomposer import TaskDecomposer
from src.evaluator import DecompositionEvaluator
from src.task import DecompositionResult, Dependency, Goal, Subtask


def blog_goal():
    return Goal(
        goal_id="goal_publish_blog",
        description="Publish a technical blog post about planning agents for AI builders.",
        success_criteria=[
            "audience_defined",
            "outline_created",
            "draft_written",
            "review_completed",
            "article_published",
        ],
        constraints=["technical_but_readable"],
        context={"audience": "AI builders"},
    )


def software_goal():
    return Goal(
        goal_id="goal_build_agent_demo",
        description="Build and deploy a small software agent demo for task planning.",
        success_criteria=["requirements_defined", "deployment_completed"],
        constraints=["deterministic_first"],
        context={"runtime": "local python"},
    )


def test_goal_serialization_roundtrip():
    goal = blog_goal()
    restored = Goal.from_dict(goal.to_dict())

    assert restored == goal
    assert restored.context["audience"] == "AI builders"


def test_decomposer_classifies_publishing_goal():
    decomposer = TaskDecomposer()

    assert decomposer.classify_goal(blog_goal()) == "publishing"


def test_decomposer_classifies_software_goal():
    decomposer = TaskDecomposer()

    assert decomposer.classify_goal(software_goal()) == "software_project"


def test_decomposer_generates_publishing_subtasks_and_dependencies():
    result = TaskDecomposer().decompose(blog_goal())

    assert result.goal_type == "publishing"
    assert len(result.subtasks) == 5
    assert len(result.dependencies) == 4
    assert result.execution_order == [
        "subtask_define_audience",
        "subtask_create_outline",
        "subtask_write_draft",
        "subtask_review_clarity",
        "subtask_publish_article",
    ]
    assert result.subtasks[0].expected_output == "audience_defined"
    assert any(
        dependency.before_subtask_id == "subtask_create_outline"
        and dependency.after_subtask_id == "subtask_write_draft"
        for dependency in result.dependencies
    )


def test_decomposer_generates_software_subtasks():
    result = TaskDecomposer().decompose(software_goal())

    assert result.goal_type == "software_project"
    assert len(result.subtasks) == 5
    assert result.execution_order[0] == "subtask_define_requirements"
    assert result.execution_order[-1] == "subtask_deploy_project"


def test_evaluator_accepts_valid_decomposition():
    result = TaskDecomposer().decompose(blog_goal())
    evaluation = DecompositionEvaluator().evaluate(result)

    assert evaluation.success is True
    assert evaluation.goal_clarity == "clear"
    assert evaluation.subtask_count == 5
    assert evaluation.dependency_count == 4
    assert evaluation.dependency_valid is True
    assert evaluation.execution_order_valid is True
    assert evaluation.trace_clarity == "high"
    assert evaluation.errors == []


def test_evaluator_flags_unclear_goal():
    goal = Goal(goal_id="goal_bad", description="Do it")
    result = TaskDecomposer().decompose(goal)
    evaluation = DecompositionEvaluator().evaluate(result)

    assert evaluation.success is False
    assert evaluation.goal_clarity == "unclear"
    assert "goal_unclear" in evaluation.errors


def test_evaluator_detects_invalid_dependency_reference():
    goal = blog_goal()
    result = DecompositionResult(
        goal=goal,
        goal_type="publishing",
        subtasks=[
            Subtask(
                subtask_id="subtask_create_outline",
                goal_id=goal.goal_id,
                description="Create outline.",
                expected_output="outline_created",
            )
        ],
        dependencies=[
            Dependency(
                dependency_id="dep_missing",
                before_subtask_id="subtask_missing",
                after_subtask_id="subtask_create_outline",
                reason="Missing dependency should fail.",
            )
        ],
        execution_order=["subtask_create_outline"],
        trace=["Goal received", "Goal classified", "Generated subtasks"],
    )

    evaluation = DecompositionEvaluator().evaluate(result)

    assert evaluation.success is False
    assert evaluation.dependency_valid is False
    assert "dependency_before_missing:subtask_missing" in evaluation.errors


def test_evaluator_detects_invalid_execution_order():
    goal = blog_goal()
    result = TaskDecomposer().decompose(goal)
    bad_result = DecompositionResult(
        goal=result.goal,
        goal_type=result.goal_type,
        subtasks=result.subtasks,
        dependencies=result.dependencies,
        execution_order=list(reversed(result.execution_order)),
        trace=result.trace,
    )

    evaluation = DecompositionEvaluator().evaluate(bad_result)

    assert evaluation.success is False
    assert evaluation.execution_order_valid is False
    assert any(error.startswith("dependency_order_invalid") for error in evaluation.errors)


def test_result_serialization_contains_expected_keys():
    result = TaskDecomposer().decompose(blog_goal())
    data = result.to_dict()

    assert data["goal"]["goal_id"] == "goal_publish_blog"
    assert data["goal_type"] == "publishing"
    assert len(data["subtasks"]) == 5
    assert len(data["dependencies"]) == 4
    assert data["execution_order"]
    assert data["trace"]
