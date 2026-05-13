"""Deterministic task decomposition engine.

The first prototype intentionally avoids LLMs. The decomposer uses lightweight
pattern matching and predefined decomposition templates so the behavior remains
inspectable and testable.
"""

from __future__ import annotations

from typing import Dict, List

from .task import DecompositionResult, Dependency, Goal, Subtask


PUBLISHING_TEMPLATE = {
    "goal_type": "publishing",
    "subtasks": [
        (
            "define_audience",
            "Define the target audience for the article.",
            "audience_defined",
        ),
        (
            "create_outline",
            "Create a structured outline for the article.",
            "outline_created",
        ),
        (
            "write_draft",
            "Write the first article draft.",
            "draft_written",
        ),
        (
            "review_clarity",
            "Review the article for clarity and flow.",
            "review_completed",
        ),
        (
            "publish_article",
            "Publish the article.",
            "article_published",
        ),
    ],
    "dependencies": [
        (
            "define_audience",
            "create_outline",
            "The outline depends on audience definition.",
        ),
        (
            "create_outline",
            "write_draft",
            "Drafting requires an outline first.",
        ),
        (
            "write_draft",
            "review_clarity",
            "Review requires a completed draft.",
        ),
        (
            "review_clarity",
            "publish_article",
            "Publishing should happen after review.",
        ),
    ],
}


SOFTWARE_TEMPLATE = {
    "goal_type": "software_project",
    "subtasks": [
        (
            "define_requirements",
            "Define project requirements and scope.",
            "requirements_defined",
        ),
        (
            "design_architecture",
            "Design the system architecture.",
            "architecture_defined",
        ),
        (
            "implement_core_logic",
            "Implement the core system logic.",
            "core_logic_implemented",
        ),
        (
            "run_tests",
            "Run tests on the implementation.",
            "tests_completed",
        ),
        (
            "deploy_project",
            "Deploy the final system.",
            "deployment_completed",
        ),
    ],
    "dependencies": [
        (
            "define_requirements",
            "design_architecture",
            "Architecture depends on requirements.",
        ),
        (
            "design_architecture",
            "implement_core_logic",
            "Implementation depends on architecture.",
        ),
        (
            "implement_core_logic",
            "run_tests",
            "Testing requires implementation.",
        ),
        (
            "run_tests",
            "deploy_project",
            "Deployment requires completed tests.",
        ),
    ],
}


DEFAULT_TEMPLATE = {
    "goal_type": "generic",
    "subtasks": [
        (
            "analyze_goal",
            "Analyze the goal and identify required work.",
            "goal_analyzed",
        ),
        (
            "plan_execution",
            "Create an execution strategy.",
            "execution_plan_created",
        ),
        (
            "execute_plan",
            "Execute the main work.",
            "work_completed",
        ),
        (
            "review_results",
            "Review the final outcome.",
            "results_reviewed",
        ),
    ],
    "dependencies": [
        (
            "analyze_goal",
            "plan_execution",
            "Execution planning requires analysis.",
        ),
        (
            "plan_execution",
            "execute_plan",
            "Execution depends on planning.",
        ),
        (
            "execute_plan",
            "review_results",
            "Review requires completed execution.",
        ),
    ],
}


class TaskDecomposer:
    """Simple deterministic decomposition engine."""

    def classify_goal(self, goal: Goal) -> str:
        """Classify the goal into a predefined template category."""

        description = goal.description.lower()

        publishing_keywords = [
            "article",
            "blog",
            "publish",
            "writing",
            "newsletter",
        ]
        software_keywords = [
            "software",
            "system",
            "application",
            "agent",
            "platform",
            "deploy",
        ]

        if any(keyword in description for keyword in publishing_keywords):
            return "publishing"
        if any(keyword in description for keyword in software_keywords):
            return "software_project"
        return "generic"

    def select_template(self, goal_type: str) -> Dict:
        """Return the decomposition template for a goal type."""

        if goal_type == "publishing":
            return PUBLISHING_TEMPLATE
        if goal_type == "software_project":
            return SOFTWARE_TEMPLATE
        return DEFAULT_TEMPLATE

    def build_subtasks(self, goal: Goal, template: Dict) -> List[Subtask]:
        """Construct subtasks from the template."""

        subtasks: List[Subtask] = []
        for subtask_name, description, expected_output in template["subtasks"]:
            subtasks.append(
                Subtask(
                    subtask_id=f"subtask_{subtask_name}",
                    goal_id=goal.goal_id,
                    description=description,
                    expected_output=expected_output,
                )
            )
        return subtasks

    def build_dependencies(self, template: Dict) -> List[Dependency]:
        """Construct dependency relationships from the template."""

        dependencies: List[Dependency] = []
        for before_step, after_step, reason in template["dependencies"]:
            dependencies.append(
                Dependency(
                    dependency_id=f"dep_{before_step}_before_{after_step}",
                    before_subtask_id=f"subtask_{before_step}",
                    after_subtask_id=f"subtask_{after_step}",
                    reason=reason,
                )
            )
        return dependencies

    def build_execution_order(self, subtasks: List[Subtask]) -> List[str]:
        """Generate a deterministic execution order."""

        return [subtask.subtask_id for subtask in subtasks]

    def build_trace(
        self,
        goal: Goal,
        goal_type: str,
        subtasks: List[Subtask],
        dependencies: List[Dependency],
    ) -> List[str]:
        """Create an inspectable decomposition trace."""

        return [
            f"Goal received: {goal.description}",
            f"Goal classified as: {goal_type}",
            f"Generated {len(subtasks)} subtasks",
            f"Generated {len(dependencies)} dependencies",
            "Execution order created",
            "Decomposition completed",
        ]

    def decompose(self, goal: Goal) -> DecompositionResult:
        """Run the full deterministic decomposition pipeline."""

        goal_type = self.classify_goal(goal)
        template = self.select_template(goal_type)
        subtasks = self.build_subtasks(goal, template)
        dependencies = self.build_dependencies(template)
        execution_order = self.build_execution_order(subtasks)
        trace = self.build_trace(goal, goal_type, subtasks, dependencies)

        return DecompositionResult(
            goal=goal,
            goal_type=goal_type,
            subtasks=subtasks,
            dependencies=dependencies,
            execution_order=execution_order,
            trace=trace,
        )
