"""Core data models for the multi-agent planning prototype.

The first prototype keeps multi-agent planning deterministic and inspectable.
Agents are represented as roles with responsibilities, outputs, and constraints.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass(frozen=True)
class AgentRole:
    """Role assigned to an agent in a planning workflow."""

    role_id: str
    name: str
    responsibility: str
    inputs: List[str] = field(default_factory=list)
    outputs: List[str] = field(default_factory=list)
    constraints: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict) -> "AgentRole":
        """Create an AgentRole from dictionary data."""

        return cls(
            role_id=data["role_id"],
            name=data["name"],
            responsibility=data["responsibility"],
            inputs=list(data.get("inputs", [])),
            outputs=list(data.get("outputs", [])),
            constraints=list(data.get("constraints", [])),
        )

    def to_dict(self) -> Dict:
        """Serialize role to dictionary."""

        return {
            "role_id": self.role_id,
            "name": self.name,
            "responsibility": self.responsibility,
            "inputs": list(self.inputs),
            "outputs": list(self.outputs),
            "constraints": list(self.constraints),
        }


@dataclass(frozen=True)
class AgentContribution:
    """Role-specific contribution to the shared plan."""

    contribution_id: str
    role_id: str
    goal_id: str
    proposed_steps: List[str]
    assumptions: List[str] = field(default_factory=list)
    risks: List[str] = field(default_factory=list)
    confidence: float = 0.5

    @classmethod
    def from_dict(cls, data: Dict) -> "AgentContribution":
        """Create an AgentContribution from dictionary data."""

        return cls(
            contribution_id=data["contribution_id"],
            role_id=data["role_id"],
            goal_id=data["goal_id"],
            proposed_steps=list(data.get("proposed_steps", [])),
            assumptions=list(data.get("assumptions", [])),
            risks=list(data.get("risks", [])),
            confidence=float(data.get("confidence", 0.5)),
        )

    def to_dict(self) -> Dict:
        """Serialize contribution to dictionary."""

        return {
            "contribution_id": self.contribution_id,
            "role_id": self.role_id,
            "goal_id": self.goal_id,
            "proposed_steps": list(self.proposed_steps),
            "assumptions": list(self.assumptions),
            "risks": list(self.risks),
            "confidence": self.confidence,
        }


@dataclass(frozen=True)
class CoordinationConflict:
    """Conflict detected between agent contributions."""

    conflict_id: str
    conflict_type: str
    source_roles: List[str]
    description: str
    recommended_resolution: str
    status: str = "open"

    def to_dict(self) -> Dict:
        """Serialize conflict to dictionary."""

        return {
            "conflict_id": self.conflict_id,
            "conflict_type": self.conflict_type,
            "source_roles": list(self.source_roles),
            "description": self.description,
            "recommended_resolution": self.recommended_resolution,
            "status": self.status,
        }


@dataclass(frozen=True)
class SharedPlan:
    """Final coordinated plan across agent roles."""

    shared_plan_id: str
    goal_id: str
    roles_used: List[str]
    steps: List[str]
    resolved_conflicts: List[str] = field(default_factory=list)
    open_conflicts: List[str] = field(default_factory=list)
    status: str = "draft"

    def to_dict(self) -> Dict:
        """Serialize shared plan to dictionary."""

        return {
            "shared_plan_id": self.shared_plan_id,
            "goal_id": self.goal_id,
            "roles_used": list(self.roles_used),
            "steps": list(self.steps),
            "resolved_conflicts": list(self.resolved_conflicts),
            "open_conflicts": list(self.open_conflicts),
            "status": self.status,
        }


@dataclass(frozen=True)
class MultiAgentPlanningResult:
    """Full output of the multi-agent planning prototype."""

    goal_id: str
    roles: List[AgentRole]
    contributions: List[AgentContribution]
    conflicts: List[CoordinationConflict]
    shared_plan: SharedPlan
    trace: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict:
        """Serialize multi-agent planning result to dictionary."""

        return {
            "goal_id": self.goal_id,
            "roles": [role.to_dict() for role in self.roles],
            "contributions": [contribution.to_dict() for contribution in self.contributions],
            "conflicts": [conflict.to_dict() for conflict in self.conflicts],
            "shared_plan": self.shared_plan.to_dict(),
            "trace": list(self.trace),
        }
