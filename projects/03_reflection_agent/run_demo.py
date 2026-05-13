"""Run the reflection agent demo.

Usage:
    python projects/03_reflection_agent/run_demo.py

The demo loads failure observations, analyzes likely causes, generates
reflections, proposes plan revisions, evaluates results, and prints traces.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List

from src.evaluator import ReflectionEvaluator
from src.failure_analyzer import FailureAnalyzer
from src.reflection import Observation, ReflectionResult
from src.reviser import PlanReviser


PROJECT_DIR = Path(__file__).resolve().parent
FAILURE_CASES_PATH = PROJECT_DIR / "examples" / "failure_cases.json"


def load_failure_cases(path: Path = FAILURE_CASES_PATH) -> List[Dict]:
    """Load failure cases from JSON."""

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def build_trace(case_id: str, observation: Observation, reflection, revision) -> List[str]:
    """Build a trace for one reflection case."""

    return [
        f"Failure observed: {observation.step_id} status={observation.status}",
        f"Observed error: {observation.observed_error}",
        f"Cause identified: {reflection.likely_cause}",
        f"Reflection generated: {reflection.recommended_revision}",
        f"Revision proposed: {revision.revision_type} -> {revision.change_summary}",
        f"Case completed: {case_id}",
    ]


def run_case(case: Dict, analyzer: FailureAnalyzer, reviser: PlanReviser, evaluator: ReflectionEvaluator) -> Dict:
    """Run one failure case through reflection and revision."""

    observation = Observation.from_dict(case["observation"])
    reflection = analyzer.analyze(observation)
    revision = reviser.revise(reflection, old_plan_id=case["old_plan_id"])
    trace = build_trace(case["case_id"], observation, reflection, revision)
    result = ReflectionResult(
        observation=observation,
        reflection=reflection,
        revision=revision,
        trace=trace,
    )
    evaluation = evaluator.evaluate(result)

    expected_revision_type = case.get("expected_revision_type", "unknown")
    expected_recommended_revision = case.get("expected_recommended_revision", "unknown")
    matched_revision_type = revision.revision_type == expected_revision_type
    matched_recommendation = reflection.recommended_revision == expected_recommended_revision

    print("\n" + "=" * 72)
    print(f"Case: {case['case_id']}")
    print(f"Old plan: {case['old_plan_id']}")
    print(f"Observation: {observation.observation_id}")
    print(f"Observed error: {observation.observed_error}")

    print("\nReflection:")
    print(reflection.to_dict())

    print("\nRevision:")
    print(revision.to_dict())

    print("\nEvaluation:")
    print(evaluation.to_dict())
    print(f"Matched expected revision type: {matched_revision_type}")
    print(f"Matched expected recommendation: {matched_recommendation}")

    print("\nTrace:")
    for step in trace:
        print(f" - {step}")

    row = evaluation.to_dict()
    row["case_id"] = case["case_id"]
    row["observed_error"] = observation.observed_error
    row["recommended_revision"] = reflection.recommended_revision
    row["revision_type"] = revision.revision_type
    row["matched_expected_revision_type"] = matched_revision_type
    row["matched_expected_recommendation"] = matched_recommendation
    return row


def print_summary(rows: List[Dict]) -> None:
    """Print compact summary for all reflection cases."""

    print("\n" + "=" * 72)
    print("Summary")
    print("=" * 72)

    for row in rows:
        print(
            f"{row['case_id']:<28} | "
            f"error={row['observed_error']:<22} | "
            f"revision={row['revision_type']:<12} | "
            f"success={str(row['success']):<5} | "
            f"trace={row['trace_clarity']}"
        )

    if rows:
        success_rate = sum(row["success"] for row in rows) / len(rows)
        revision_match_rate = sum(row["matched_expected_revision_type"] for row in rows) / len(rows)
        recommendation_match_rate = sum(row["matched_expected_recommendation"] for row in rows) / len(rows)
        print(f"\nreflection_success_rate={success_rate:.3f}")
        print(f"revision_type_match_rate={revision_match_rate:.3f}")
        print(f"recommendation_match_rate={recommendation_match_rate:.3f}")


def main() -> None:
    """Run all reflection demo cases."""

    cases = load_failure_cases()
    analyzer = FailureAnalyzer()
    reviser = PlanReviser()
    evaluator = ReflectionEvaluator()
    rows = [run_case(case, analyzer, reviser, evaluator) for case in cases]
    print_summary(rows)


if __name__ == "__main__":
    main()
