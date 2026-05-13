"""Core reflection data models for the reflection agent.

The reflection prototype turns failed or blocked execution observations into
specific reflections, recommended revisions, and an inspectable trace.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass(frozen=True)
class Observation:
    """Grounded record of an execution outcome."""

    observation_id: str
    step_id: str
    status: str
    observed_output: str = ""
    observed_error: str = ""
    state_change: str = ""
    notes: str = ""

    @classmethod
    def from_dict(cls, data: Dict) -> "Observation":
        """Create an observation from dictionary data."""

        return cls(
            observation_id=data["observation_id"],
            step_id=data["step_id"],
            status=data["status"],
            observed_output=data.get("observed_output", ""),
            observed_error=data.get("observed_error", ""),
            state_change=data.get("state_change", ""),
            notes=data.get("notes", ""),
        )

    def to_dict(self) -> Dict:
        """Serialize observation to dictionary."""

        return {
            "observation_id": self.observation_id,
            "step_id": self.step_id,
            "status": self.status,
            "observed_output": self.observed_output,
            "observed_error": self.observed_error,
            "state_change": self.state_change,
            "notes": self.notes,
        }


@dataclass(frozen=True)
class Reflection:
    """Actionable analysis of an observation."""

    reflection_id: str
    observation_id: str
    observed_issue: str
    likely_cause: str
    impact: str
    recommended_revision: str
    confidence: float = 0.5

    def to_dict(self) -> Dict:
        """Serialize reflection to dictionary."""

        return {
            "reflection_id": self.reflection_id,
            "observation_id": self.observation_id,
            "observed_issue": self.observed_issue,
            "likely_cause": self.likely_cause,
            "impact": self.impact,
            "recommended_revision": self.recommended_revision,
            "confidence": self.confidence,
        }


@dataclass(frozen=True)
class Revision:
    """Plan modification proposed from a reflection."""

    revision_id: str
    reflection_id: str
    revision_type: str
    old_plan_id: str
    new_plan_id: str
    change_summary: str
    status: str = "proposed"

    def to_dict(self) -> Dict:
        """Serialize revision to dictionary."""

        return {
            "revision_id": self.revision_id,
            "reflection_id": self.reflection_id,
            "revision_type": self.revision_type,
            "old_plan_id": self.old_plan_id,
            "new_plan_id": self.new_plan_id,
            "change_summary": self.change_summary,
            "status": self.status,
        }


@dataclass(frozen=True)
class ReflectionResult:
    """Full output of reflection and revision generation."""

    observation: Observation
    reflection: Reflection
    revision: Revision
    trace: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict:
        """Serialize reflection result to dictionary."""

        return {
            "observation": self.observation.to_dict(),
            "reflection": self.reflection.to_dict(),
            "revision": self.revision.to_dict(),
            "trace": list(self.trace),
        }
