"""Evaluation utilities for the reflection agent.

The evaluator checks whether a reflection is grounded, specific, actionable,
and whether the proposed revision addresses the observed failure.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

from .reflection import ReflectionResult


@dataclass(frozen=True)
class ReflectionEvaluation:
    """Evaluation result for one reflection run."""

    observation_id: str
    success: bool
    failure_detected: bool
    cause_specificity: str
    reflection_quality: str
    revision_useful: bool
    trace_clarity: str
    errors: List[str]
    warnings: List[str]

    def to_dict(self) -> Dict:
        """Serialize evaluation to dictionary."""

        return {
            "observation_id": self.observation_id,
            "success": self.success,
            "failure_detected": self.failure_detected,
            "cause_specificity": self.cause_specificity,
            "reflection_quality": self.reflection_quality,
            "revision_useful": self.revision_useful,
            "trace_clarity": self.trace_clarity,
            "errors": list(self.errors),
            "warnings": list(self.warnings),
        }


class ReflectionEvaluator:
    """Evaluate reflection and revision quality."""

    def evaluate(self, result: ReflectionResult) -> ReflectionEvaluation:
        """Evaluate a reflection result."""

        errors: List[str] = []
        warnings: List[str] = []

        failure_detected = result.observation.status in {"failure", "blocked"}
        if not failure_detected:
            warnings.append("observation_not_failure_or_blocked")

        cause_specificity = self._cause_specificity(result)
        if cause_specificity == "low":
            warnings.append("low_cause_specificity")

        reflection_quality = self._reflection_quality(result)
        if reflection_quality in {"none", "generic"}:
            errors.append("reflection_not_actionable")

        revision_useful = self._revision_useful(result)
        if not revision_useful:
            errors.append("revision_not_useful")

        trace_clarity = self._trace_clarity(result)
        if trace_clarity == "low":
            warnings.append("trace_low_clarity")

        success = not errors and failure_detected

        return ReflectionEvaluation(
            observation_id=result.observation.observation_id,
            success=success,
            failure_detected=failure_detected,
            cause_specificity=cause_specificity,
            reflection_quality=reflection_quality,
            revision_useful=revision_useful,
            trace_clarity=trace_clarity,
            errors=errors,
            warnings=warnings,
        )

    def _cause_specificity(self, result: ReflectionResult) -> str:
        """Classify likely-cause specificity."""

        cause = result.reflection.likely_cause.strip().lower()
        if not cause:
            return "none"
        generic_markers = ["unknown", "not covered", "manual inspection"]
        if any(marker in cause for marker in generic_markers):
            return "low"
        if len(cause.split()) >= 6:
            return "high"
        return "medium"

    def _reflection_quality(self, result: ReflectionResult) -> str:
        """Classify reflection quality."""

        reflection = result.reflection
        if not reflection.observed_issue or not reflection.recommended_revision:
            return "none"
        if reflection.recommended_revision == "manual_review_required":
            return "generic"
        if reflection.confidence >= 0.8:
            return "actionable"
        return "specific"

    def _revision_useful(self, result: ReflectionResult) -> bool:
        """Return True if the revision appears to address the reflection."""

        revision = result.revision
        if revision.status not in {"proposed", "applied"}:
            return False
        if not revision.change_summary:
            return False
        if revision.revision_type not in {
            "add_step",
            "remove_step",
            "reorder_step",
            "replace_step",
            "mark_blocked",
        }:
            return False
        return True

    def _trace_clarity(self, result: ReflectionResult) -> str:
        """Classify trace clarity."""

        trace_text = "\n".join(result.trace).lower()
        required_markers = [
            "failure observed",
            "cause identified",
            "reflection generated",
            "revision proposed",
        ]
        matched = sum(1 for marker in required_markers if marker in trace_text)

        if matched >= 4:
            return "high"
        if matched >= 2:
            return "medium"
        return "low"
