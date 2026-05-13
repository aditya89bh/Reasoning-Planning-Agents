"""Conflict detection for the multi-agent planning prototype.

The detector inspects role contributions for simple coordination issues:
missing required steps, duplicate proposed steps, and role overlap.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from typing import Dict, Iterable, List, Set

from .agent_role import AgentContribution, AgentRole, CoordinationConflict


class ConflictDetector:
    """Detect coordination conflicts across agent contributions."""

    DEFAULT_REQUIRED_STEPS = [
        "define_audience",
        "create_outline",
        "write_draft",
        "review_clarity",
        "publish_article",
    ]

    def detect(
        self,
        roles: List[AgentRole],
        contributions: List[AgentContribution],
        required_steps: Iterable[str] | None = None,
    ) -> List[CoordinationConflict]:
        """Detect conflicts in multi-agent planning output."""

        required = list(required_steps or self.DEFAULT_REQUIRED_STEPS)
        conflicts: List[CoordinationConflict] = []
        conflicts.extend(self._missing_required_steps(contributions, required))
        conflicts.extend(self._duplicate_steps(contributions))
        conflicts.extend(self._role_overlap(roles))
        return conflicts

    def _all_steps(self, contributions: List[AgentContribution]) -> Set[str]:
        """Return all proposed steps across contributions."""

        steps: Set[str] = set()
        for contribution in contributions:
            steps.update(contribution.proposed_steps)
        return steps

    def _missing_required_steps(
        self,
        contributions: List[AgentContribution],
        required_steps: List[str],
    ) -> List[CoordinationConflict]:
        """Detect required steps missing from all contributions."""

        proposed = self._all_steps(contributions)
        conflicts: List[CoordinationConflict] = []

        for step in required_steps:
            if step not in proposed:
                conflicts.append(
                    CoordinationConflict(
                        conflict_id=f"conflict_missing_{step}",
                        conflict_type="missing_required_step",
                        source_roles=[contribution.role_id for contribution in contributions],
                        description=f"Required step is missing from proposed plans: {step}",
                        recommended_resolution=f"insert_step:{step}",
                        status="open",
                    )
                )

        return conflicts

    def _duplicate_steps(self, contributions: List[AgentContribution]) -> List[CoordinationConflict]:
        """Detect steps proposed by multiple roles."""

        step_to_roles: Dict[str, List[str]] = defaultdict(list)
        for contribution in contributions:
            for step in contribution.proposed_steps:
                step_to_roles[step].append(contribution.role_id)

        conflicts: List[CoordinationConflict] = []
        for step, role_ids in step_to_roles.items():
            if len(role_ids) > 1:
                conflicts.append(
                    CoordinationConflict(
                        conflict_id=f"conflict_duplicate_{step}",
                        conflict_type="duplicate_step",
                        source_roles=role_ids,
                        description=f"Step was proposed by multiple roles: {step}",
                        recommended_resolution=f"deduplicate_step:{step}",
                        status="open",
                    )
                )

        return conflicts

    def _role_overlap(self, roles: List[AgentRole]) -> List[CoordinationConflict]:
        """Detect role output overlap."""

        output_counter = Counter()
        output_to_roles: Dict[str, List[str]] = defaultdict(list)

        for role in roles:
            for output in role.outputs:
                output_counter[output] += 1
                output_to_roles[output].append(role.role_id)

        conflicts: List[CoordinationConflict] = []
        for output, count in output_counter.items():
            if count > 1:
                conflicts.append(
                    CoordinationConflict(
                        conflict_id=f"conflict_role_overlap_{output}",
                        conflict_type="role_overlap",
                        source_roles=output_to_roles[output],
                        description=f"Multiple roles claim the same output: {output}",
                        recommended_resolution=f"clarify_owner:{output}",
                        status="open",
                    )
                )

        return conflicts
