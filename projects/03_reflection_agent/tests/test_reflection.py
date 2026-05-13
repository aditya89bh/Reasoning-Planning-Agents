"""Tests for the reflection agent.

Run from the repository root with:
    python -m pytest projects/03_reflection_agent/tests
"""

from pathlib import Path
import sys

PROJECT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_DIR))

from src.evaluator import ReflectionEvaluator
from src.failure_analyzer import FailureAnalyzer
from src.reflection import Observation, ReflectionResult
from src.reviser import PlanReviser


def missing_audience_observation():
    return Observation(
        observation_id="obs_missing_audience",
        step_id="step_define_audience",
        status="failure",
        observed_error="missing_audience",
        state_change="draft_blocked",
        notes="Audience was not defined.",
    )


def build_result(observation):
    reflection = FailureAnalyzer().analyze(observation)
    revision = PlanReviser().revise(reflection, old_plan_id="plan_publish_blog_v1")
    trace = [
        f"Failure observed: {observation.step_id} status={observation.status}",
        f"Observed error: {observation.observed_error}",
        f"Cause identified: {reflection.likely_cause}",
        f"Reflection generated: {reflection.recommended_revision}",
        f"Revision proposed: {revision.revision_type} -> {revision.change_summary}",
    ]
    return ReflectionResult(
        observation=observation,
        reflection=reflection,
        revision=revision,
        trace=trace,
    )


def test_observation_serialization_roundtrip():
    observation = missing_audience_observation()
    restored = Observation.from_dict(observation.to_dict())

    assert restored == observation
    assert restored.observed_error == "missing_audience"


def test_failure_analyzer_maps_missing_audience_to_actionable_reflection():
    reflection = FailureAnalyzer().analyze(missing_audience_observation())

    assert reflection.recommended_revision == "add_audience_definition_step"
    assert "audience" in reflection.likely_cause.lower()
    assert reflection.confidence == 0.9


def test_failure_analyzer_maps_outline_missing():
    observation = Observation(
        observation_id="obs_outline_missing",
        step_id="step_write_draft",
        status="failure",
        observed_error="outline_missing",
    )

    reflection = FailureAnalyzer().analyze(observation)

    assert reflection.recommended_revision == "add_or_reorder_outline_step"
    assert "outline" in reflection.observed_issue.lower()


def test_failure_analyzer_uses_default_for_unknown_failure():
    observation = Observation(
        observation_id="obs_unknown",
        step_id="step_unknown",
        status="failure",
        observed_error="strange_error",
    )

    reflection = FailureAnalyzer().analyze(observation)

    assert reflection.recommended_revision == "manual_review_required"
    assert reflection.confidence == 0.5


def test_reviser_generates_add_step_revision():
    reflection = FailureAnalyzer().analyze(missing_audience_observation())
    revision = PlanReviser().revise(reflection, old_plan_id="plan_publish_blog_v1")

    assert revision.revision_type == "add_step"
    assert revision.old_plan_id == "plan_publish_blog_v1"
    assert revision.new_plan_id == "plan_publish_blog_v1_revised"
    assert "audience" in revision.change_summary.lower()
    assert revision.status == "proposed"


def test_reviser_generates_blocked_revision_for_tool_unavailable():
    observation = Observation(
        observation_id="obs_tool_unavailable",
        step_id="step_deploy_project",
        status="blocked",
        observed_error="tool_unavailable",
    )
    reflection = FailureAnalyzer().analyze(observation)
    revision = PlanReviser().revise(reflection, old_plan_id="plan_deploy_agent_demo")

    assert revision.revision_type == "mark_blocked"
    assert "tool" in revision.change_summary.lower()


def test_reflection_evaluator_accepts_actionable_result():
    result = build_result(missing_audience_observation())
    evaluation = ReflectionEvaluator().evaluate(result)

    assert evaluation.success is True
    assert evaluation.failure_detected is True
    assert evaluation.cause_specificity == "high"
    assert evaluation.reflection_quality == "actionable"
    assert evaluation.revision_useful is True
    assert evaluation.trace_clarity == "high"
    assert evaluation.errors == []


def test_reflection_evaluator_flags_non_failure_observation():
    observation = Observation(
        observation_id="obs_success",
        step_id="step_define_audience",
        status="success",
        observed_output="audience_defined",
    )
    result = build_result(observation)
    evaluation = ReflectionEvaluator().evaluate(result)

    assert evaluation.success is False
    assert evaluation.failure_detected is False
    assert "observation_not_failure_or_blocked" in evaluation.warnings


def test_reflection_evaluator_flags_generic_unknown_failure():
    observation = Observation(
        observation_id="obs_unknown",
        step_id="step_unknown",
        status="failure",
        observed_error="strange_error",
    )
    result = build_result(observation)
    evaluation = ReflectionEvaluator().evaluate(result)

    assert evaluation.success is False
    assert evaluation.reflection_quality == "generic"
    assert "reflection_not_actionable" in evaluation.errors


def test_reflection_result_serialization_contains_expected_keys():
    result = build_result(missing_audience_observation())
    data = result.to_dict()

    assert data["observation"]["observation_id"] == "obs_missing_audience"
    assert data["reflection"]["recommended_revision"] == "add_audience_definition_step"
    assert data["revision"]["revision_type"] == "add_step"
    assert data["trace"]
