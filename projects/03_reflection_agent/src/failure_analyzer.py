"""Failure analysis for the reflection agent.

The first prototype uses deterministic mappings from observed errors to likely
causes, impacts, and recommended revisions. This keeps reflection inspectable
before adding LLM-based critique.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from .reflection import Observation, Reflection


@dataclass(frozen=True)
class FailurePattern:
    """Known failure pattern used to generate reflection."""

    observed_issue: str
    likely_cause: str
    impact: str
    recommended_revision: str
    confidence: float


class FailureAnalyzer:
    """Analyze observations and create actionable reflections."""

    PATTERNS: Dict[str, FailurePattern] = {
        "missing_audience": FailurePattern(
            observed_issue="Audience definition step failed.",
            likely_cause="The goal does not contain enough audience context.",
            impact="Drafting and review quality will be unstable without a target reader.",
            recommended_revision="add_audience_definition_step",
            confidence=0.9,
        ),
        "target_audience_missing": FailurePattern(
            observed_issue="Drafting is blocked because target audience is missing.",
            likely_cause="The plan skipped audience definition before writing.",
            impact="The article cannot choose tone, depth, or examples reliably.",
            recommended_revision="add_audience_definition_step",
            confidence=0.9,
        ),
        "outline_missing": FailurePattern(
            observed_issue="Drafting was attempted without an outline.",
            likely_cause="The plan is missing an outline step or has the wrong order.",
            impact="The draft may become unfocused or incomplete.",
            recommended_revision="add_or_reorder_outline_step",
            confidence=0.85,
        ),
        "review_skipped": FailurePattern(
            observed_issue="Publishing was attempted without review.",
            likely_cause="The plan omitted a quality-control step before publishing.",
            impact="Low-quality or unclear output may be published.",
            recommended_revision="add_review_before_publish",
            confidence=0.88,
        ),
        "tool_unavailable": FailurePattern(
            observed_issue="Execution tool was unavailable.",
            likely_cause="Required external tool or runtime was not accessible.",
            impact="The step cannot complete until the environment is fixed.",
            recommended_revision="mark_step_blocked",
            confidence=0.8,
        ),
        "blocked_dependency": FailurePattern(
            observed_issue="Step was blocked by an unmet dependency.",
            likely_cause="A prerequisite step did not complete before this step ran.",
            impact="Execution order is invalid or incomplete.",
            recommended_revision="reorder_plan_dependencies",
            confidence=0.85,
        ),
    }

    DEFAULT_PATTERN = FailurePattern(
        observed_issue="Execution did not complete successfully.",
        likely_cause="The failure is not covered by a known deterministic pattern.",
        impact="The plan may need human inspection before continuing.",
        recommended_revision="manual_review_required",
        confidence=0.5,
    )

    def analyze(self, observation: Observation) -> Reflection:
        """Create a Reflection from an Observation."""

        pattern = self.PATTERNS.get(observation.observed_error, self.DEFAULT_PATTERN)

        return Reflection(
            reflection_id=f"reflection_{observation.observation_id}",
            observation_id=observation.observation_id,
            observed_issue=pattern.observed_issue,
            likely_cause=pattern.likely_cause,
            impact=pattern.impact,
            recommended_revision=pattern.recommended_revision,
            confidence=pattern.confidence,
        )
