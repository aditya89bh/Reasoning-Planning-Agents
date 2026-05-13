"""Tests for the planner-executor agent.

Run from the repository root with:
    python -m pytest projects/02_planner_executor_agent/tests
"""

from pathlib import Path
import sys

PROJECT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_DIR))

from src.evaluator import PlanExecutionEvaluator
from src.executor import PlanExecutor
from src.plan import Plan, PlanStep
from src.planner import Planner


def sample_plan_spec():
    return {
        "plan_id": "plan_publish_blog_v1",
        "goal_id": "goal_publish_blog",
        "description": "Execute a publishing workflow.",
        "assumptions": ["audience_can_be_defined"],
        "risks": ["draft_may_need_review"],
        "status": "ready",
        "version": 1,
        "steps": [
            {
                "step_id": "step_define_audience",
                "description": "Define the target audience.",
                "expected_output": "audience_defined",
                "dependencies": [],
            },
            {
                "step_id": "step_create_outline",
                "description": "Create the outline.",
                "expected_output": "outline_created",
                "dependencies": ["step_define_audience"],
            },
            {
                "step_id": "step_write_draft",
                "description": "Write the draft.",
                "expected_output": "draft_written",
                "dependencies": ["step_create_outline"],
            },
        ],
    }


def test_planner_builds_plan_from_spec():
    plan = Planner().build_plan(sample_plan_spec())

    assert isinstance(plan, Plan)
    assert plan.plan_id == "plan_publish_blog_v1"
    assert plan.goal_id == "goal_publish_blog"
    assert len(plan.steps) == 3
    assert plan.steps[0].step_id == "step_define_audience"
    assert plan.steps[1].dependencies == ["step_define_audience"]


def test_plan_serialization_roundtrip():
    plan = Planner().build_plan(sample_plan_spec())
    restored = Plan.from_dict(plan.to_dict())

    assert restored == plan
    assert restored.steps[2].expected_output == "draft_written"


def test_planner_validates_valid_plan_structure():
    plan = Planner().build_plan(sample_plan_spec())
    errors = Planner().validate_plan_structure(plan)

    assert errors == []


def test_planner_detects_missing_dependency():
    spec = sample_plan_spec()
    spec["steps"][1]["dependencies"] = ["step_missing"]
    plan = Planner().build_plan(spec)

    errors = Planner().validate_plan_structure(plan)

    assert "missing_step_dependency:step_create_outline:step_missing" in errors


def test_executor_completes_valid_plan():
    plan = Planner().build_plan(sample_plan_spec())
    execution = PlanExecutor().execute(plan)

    assert execution.final_status == "complete"
    assert len(execution.step_results) == 3
    assert all(result.status == "success" for result in execution.step_results)
    assert execution.step_results[-1].output == "draft_written"
    assert any("Execution completed" in step for step in execution.trace)


def test_executor_handles_forced_failure():
    plan = Planner().build_plan(sample_plan_spec())
    execution = PlanExecutor().execute(
        plan,
        forced_failures={"step_define_audience": "missing_audience"},
    )

    assert execution.final_status == "failed"
    assert execution.step_results[0].status == "failure"
    assert execution.step_results[0].error == "missing_audience"
    assert execution.step_results[1].status == "blocked"


def test_executor_blocks_missing_dependency_if_order_is_wrong():
    plan = Plan(
        plan_id="plan_bad_order",
        goal_id="goal_bad_order",
        description="Plan with wrong step order.",
        steps=[
            PlanStep(
                step_id="step_write_draft",
                plan_id="plan_bad_order",
                description="Write draft.",
                expected_output="draft_written",
                dependencies=["step_create_outline"],
            ),
            PlanStep(
                step_id="step_create_outline",
                plan_id="plan_bad_order",
                description="Create outline.",
                expected_output="outline_created",
                dependencies=[],
            ),
        ],
    )

    execution = PlanExecutor().execute(plan)

    assert execution.final_status == "blocked"
    assert execution.step_results[0].status == "blocked"
    assert "missing_dependencies" in execution.step_results[0].error


def test_evaluator_accepts_complete_execution():
    plan = Planner().build_plan(sample_plan_spec())
    execution = PlanExecutor().execute(plan)
    evaluation = PlanExecutionEvaluator().evaluate(plan, execution)

    assert evaluation.success is True
    assert evaluation.plan_valid is True
    assert evaluation.step_count == 3
    assert evaluation.successful_steps == 3
    assert evaluation.failed_steps == 0
    assert evaluation.blocked_steps == 0
    assert evaluation.final_status == "complete"
    assert evaluation.trace_clarity == "high"
    assert evaluation.errors == []


def test_evaluator_reports_failed_execution():
    plan = Planner().build_plan(sample_plan_spec())
    execution = PlanExecutor().execute(
        plan,
        forced_failures={"step_define_audience": "missing_audience"},
    )
    evaluation = PlanExecutionEvaluator().evaluate(plan, execution)

    assert evaluation.success is False
    assert evaluation.final_status == "failed"
    assert evaluation.failed_steps == 1
    assert evaluation.blocked_steps == 2


def test_evaluator_detects_plan_execution_mismatch():
    plan = Planner().build_plan(sample_plan_spec())
    execution = PlanExecutor().execute(plan)
    wrong_execution = type(execution)(
        plan_id="other_plan",
        goal_id=execution.goal_id,
        step_results=execution.step_results,
        final_status=execution.final_status,
        trace=execution.trace,
    )

    evaluation = PlanExecutionEvaluator().evaluate(plan, wrong_execution)

    assert evaluation.success is False
    assert "execution_plan_id_mismatch" in evaluation.errors
