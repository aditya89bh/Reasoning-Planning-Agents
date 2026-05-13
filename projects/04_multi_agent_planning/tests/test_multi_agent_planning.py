"""Tests for the multi-agent planning prototype.

Run from the repository root with:
    python -m pytest projects/04_multi_agent_planning/tests
"""

from pathlib import Path
import sys

PROJECT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_DIR))

from src.agent_role import AgentContribution, AgentRole
from src.conflict_detector import ConflictDetector
from src.coordinator import MultiAgentCoordinator
from src.evaluator import MultiAgentPlanningEvaluator


def sample_roles():
    return [
        AgentRole(
            role_id="role_decomposer",
            name="Decomposer",
            responsibility="Break the goal into clear subtasks.",
            inputs=["goal"],
            outputs=["subtasks"],
            constraints=["keep subtasks specific"],
        ),
        AgentRole(
            role_id="role_planner",
            name="Planner",
            responsibility="Order subtasks into an executable plan.",
            inputs=["subtasks"],
            outputs=["ordered_plan"],
            constraints=["respect dependencies"],
        ),
        AgentRole(
            role_id="role_critic",
            name="Critic",
            responsibility="Detect missing steps and weak dependencies.",
            inputs=["ordered_plan"],
            outputs=["conflict_report"],
            constraints=["surface missing quality checks"],
        ),
        AgentRole(
            role_id="role_coordinator",
            name="Coordinator",
            responsibility="Merge outputs into one shared plan.",
            inputs=["subtasks", "ordered_plan", "conflict_report"],
            outputs=["shared_plan"],
            constraints=["resolve conflicts explicitly"],
        ),
    ]


def sample_contributions_missing_review():
    return [
        AgentContribution(
            contribution_id="contrib_decomposer",
            role_id="role_decomposer",
            goal_id="goal_publish_blog",
            proposed_steps=["define_audience", "create_outline", "write_draft", "publish_article"],
            confidence=0.82,
        ),
        AgentContribution(
            contribution_id="contrib_planner",
            role_id="role_planner",
            goal_id="goal_publish_blog",
            proposed_steps=["define_audience", "create_outline", "write_draft", "publish_article"],
            confidence=0.78,
        ),
        AgentContribution(
            contribution_id="contrib_critic",
            role_id="role_critic",
            goal_id="goal_publish_blog",
            proposed_steps=["review_clarity"],
            confidence=0.9,
        ),
        AgentContribution(
            contribution_id="contrib_coordinator",
            role_id="role_coordinator",
            goal_id="goal_publish_blog",
            proposed_steps=[],
            confidence=0.86,
        ),
    ]


def test_agent_role_serialization_roundtrip():
    role = sample_roles()[0]
    restored = AgentRole.from_dict(role.to_dict())

    assert restored == role
    assert restored.role_id == "role_decomposer"


def test_agent_contribution_serialization_roundtrip():
    contribution = sample_contributions_missing_review()[0]
    restored = AgentContribution.from_dict(contribution.to_dict())

    assert restored == contribution
    assert restored.proposed_steps[0] == "define_audience"


def test_conflict_detector_detects_duplicate_steps():
    conflicts = ConflictDetector().detect(
        roles=sample_roles(),
        contributions=sample_contributions_missing_review(),
        required_steps=[
            "define_audience",
            "create_outline",
            "write_draft",
            "review_clarity",
            "publish_article",
        ],
    )

    conflict_types = {conflict.conflict_type for conflict in conflicts}
    assert "duplicate_step" in conflict_types
    assert any(conflict.conflict_id == "conflict_duplicate_define_audience" for conflict in conflicts)


def test_conflict_detector_detects_missing_required_step():
    contributions = [
        AgentContribution(
            contribution_id="contrib_planner",
            role_id="role_planner",
            goal_id="goal_publish_blog",
            proposed_steps=["define_audience", "create_outline", "write_draft"],
        )
    ]

    conflicts = ConflictDetector().detect(
        roles=sample_roles(),
        contributions=contributions,
        required_steps=["define_audience", "create_outline", "write_draft", "review_clarity"],
    )

    assert any(conflict.conflict_id == "conflict_missing_review_clarity" for conflict in conflicts)
    assert any(conflict.recommended_resolution == "insert_step:review_clarity" for conflict in conflicts)


def test_coordinator_creates_valid_shared_plan():
    result = MultiAgentCoordinator().coordinate(
        goal_id="goal_publish_blog",
        roles=sample_roles(),
        contributions=sample_contributions_missing_review(),
        required_steps=[
            "define_audience",
            "create_outline",
            "write_draft",
            "review_clarity",
            "publish_article",
        ],
    )

    assert result.shared_plan.status == "valid"
    assert result.shared_plan.steps == [
        "define_audience",
        "create_outline",
        "write_draft",
        "review_clarity",
        "publish_article",
    ]
    assert result.shared_plan.open_conflicts == []
    assert result.trace


def test_evaluator_accepts_valid_multi_agent_result():
    result = MultiAgentCoordinator().coordinate(
        goal_id="goal_publish_blog",
        roles=sample_roles(),
        contributions=sample_contributions_missing_review(),
        required_steps=[
            "define_audience",
            "create_outline",
            "write_draft",
            "review_clarity",
            "publish_article",
        ],
    )
    evaluation = MultiAgentPlanningEvaluator().evaluate(result)

    assert evaluation.success is True
    assert evaluation.role_count == 4
    assert evaluation.contribution_count == 4
    assert evaluation.role_clarity is True
    assert evaluation.shared_plan_valid is True
    assert evaluation.trace_clarity == "high"
    assert evaluation.errors == []


def test_evaluator_detects_duplicate_role_ids():
    roles = sample_roles()
    roles = roles + [roles[0]]
    result = MultiAgentCoordinator().coordinate(
        goal_id="goal_publish_blog",
        roles=roles,
        contributions=sample_contributions_missing_review(),
    )
    evaluation = MultiAgentPlanningEvaluator().evaluate(result)

    assert evaluation.success is False
    assert evaluation.role_clarity is False
    assert "duplicate_role_ids" in evaluation.errors


def test_multi_agent_result_serialization_contains_expected_keys():
    result = MultiAgentCoordinator().coordinate(
        goal_id="goal_publish_blog",
        roles=sample_roles(),
        contributions=sample_contributions_missing_review(),
    )
    data = result.to_dict()

    assert data["goal_id"] == "goal_publish_blog"
    assert len(data["roles"]) == 4
    assert len(data["contributions"]) == 4
    assert data["shared_plan"]["status"] == "valid"
    assert data["trace"]
