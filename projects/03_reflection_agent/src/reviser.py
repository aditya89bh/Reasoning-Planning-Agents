"""Revision generation for the reflection agent.

The reviser converts a reflection recommendation into a concrete Revision object.
It does not yet mutate a full plan. The first prototype focuses on producing
explicit revision actions that can later be connected to the planner-executor.
"""

from __future__ import annotations

from .reflection import Reflection, Revision


class PlanReviser:
    """Create plan revisions from reflections."""

    REVISION_MAP = {
        "add_audience_definition_step": {
            "revision_type": "add_step",
            "change_summary": "Add an audience-definition step before outline or drafting.",
        },
        "add_or_reorder_outline_step": {
            "revision_type": "add_step",
            "change_summary": "Add or move outline creation before drafting.",
        },
        "add_review_before_publish": {
            "revision_type": "add_step",
            "change_summary": "Insert a review step before publishing.",
        },
        "mark_step_blocked": {
            "revision_type": "mark_blocked",
            "change_summary": "Mark the failed step as blocked until the required tool or environment is available.",
        },
        "reorder_plan_dependencies": {
            "revision_type": "reorder_step",
            "change_summary": "Reorder the plan so prerequisite steps complete before dependent steps.",
        },
        "manual_review_required": {
            "revision_type": "mark_blocked",
            "change_summary": "Pause the plan and request manual review because the failure type is unknown.",
        },
    }

    def revise(self, reflection: Reflection, old_plan_id: str) -> Revision:
        """Create a revision from a reflection."""

        revision_spec = self.REVISION_MAP.get(
            reflection.recommended_revision,
            self.REVISION_MAP["manual_review_required"],
        )
        new_plan_id = f"{old_plan_id}_revised"

        return Revision(
            revision_id=f"revision_{reflection.reflection_id}",
            reflection_id=reflection.reflection_id,
            revision_type=revision_spec["revision_type"],
            old_plan_id=old_plan_id,
            new_plan_id=new_plan_id,
            change_summary=revision_spec["change_summary"],
            status="proposed",
        )
