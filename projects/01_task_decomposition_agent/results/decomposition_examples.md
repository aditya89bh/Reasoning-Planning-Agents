# Decomposition Examples

This document summarizes the expected behavior of the Task Decomposition Agent prototype.

The prototype demonstrates a minimal goal-to-plan scaffold:

```text
Goal → Goal Type → Subtasks → Dependencies → Execution Order → Evaluation → Trace
```

The goal is not open-ended autonomous planning yet. The goal is to make task decomposition explicit, deterministic, inspectable, and testable.

## Demo goals

The demo uses `examples/demo_goals.json`.

| Goal | Expected goal type | Expected output |
|---|---|---|
| `goal_publish_blog` | `publishing` | article publishing subtasks |
| `goal_build_agent_demo` | `software_project` | software project subtasks |
| `goal_prepare_workshop` | `generic` | generic work plan subtasks |

## Example 1: Publish blog post

Input goal:

```text
Publish a technical blog post about planning agents for AI builders.
```

Expected goal type:

```text
publishing
```

Expected subtasks:

```text
subtask_define_audience → audience_defined
subtask_create_outline → outline_created
subtask_write_draft → draft_written
subtask_review_clarity → review_completed
subtask_publish_article → article_published
```

Expected dependencies:

```text
subtask_define_audience → subtask_create_outline
subtask_create_outline → subtask_write_draft
subtask_write_draft → subtask_review_clarity
subtask_review_clarity → subtask_publish_article
```

Expected execution order:

```text
1. subtask_define_audience
2. subtask_create_outline
3. subtask_write_draft
4. subtask_review_clarity
5. subtask_publish_article
```

Expected evaluation:

```text
success: true
goal_clarity: clear
subtask_count: 5
dependency_count: 4
dependency_valid: true
execution_order_valid: true
trace_clarity: high
```

## Example 2: Build agent demo

Input goal:

```text
Build and deploy a small software agent demo for task planning.
```

Expected goal type:

```text
software_project
```

Expected subtasks:

```text
subtask_define_requirements → requirements_defined
subtask_design_architecture → architecture_defined
subtask_implement_core_logic → core_logic_implemented
subtask_run_tests → tests_completed
subtask_deploy_project → deployment_completed
```

Expected dependencies:

```text
subtask_define_requirements → subtask_design_architecture
subtask_design_architecture → subtask_implement_core_logic
subtask_implement_core_logic → subtask_run_tests
subtask_run_tests → subtask_deploy_project
```

Expected evaluation:

```text
success: true
goal_clarity: clear
dependency_valid: true
execution_order_valid: true
trace_clarity: high
```

## Example 3: Prepare workshop

Input goal:

```text
Prepare a workshop on reasoning and planning agents.
```

Expected goal type:

```text
generic
```

Expected subtasks:

```text
subtask_analyze_goal → goal_analyzed
subtask_plan_execution → execution_plan_created
subtask_execute_plan → work_completed
subtask_review_results → results_reviewed
```

Expected dependencies:

```text
subtask_analyze_goal → subtask_plan_execution
subtask_plan_execution → subtask_execute_plan
subtask_execute_plan → subtask_review_results
```

## Expected trace shape

Each decomposition should produce a trace like:

```text
Goal received: <goal description>
Goal classified as: <goal type>
Generated <n> subtasks
Generated <n> dependencies
Execution order created
Decomposition completed
```

## Evaluation dimensions

| Metric | Meaning |
|---|---|
| Goal clarity | Is the goal specific enough to decompose? |
| Subtask count | How many subtasks were generated? |
| Dependency validity | Do dependencies reference valid subtasks? |
| Execution order validity | Does order contain all subtasks and respect dependencies? |
| Trace clarity | Does the trace expose major decomposition steps? |

## What this prototype proves

This project proves the first layer of the planning-agent stack:

```text
high-level goal → structured subtasks → valid execution order → inspectable trace
```

That is the foundation required before planner-executor, reflection, and multi-agent coordination layers.

## Run command

From the repository root:

```bash
python projects/01_task_decomposition_agent/run_demo.py
```

## Test command

From the repository root:

```bash
python -m pytest projects/01_task_decomposition_agent/tests
```

## Current limitations

- Goal classification is keyword-based.
- Decomposition is template-based.
- No LLM integration yet.
- No open-ended decomposition yet.
- No execution or reflection yet.
- Dependencies are linear for the first prototype.

## Next improvement

The next useful step is to update this project README from design phase to runnable first prototype, then update the top-level repository README with Project 01 status.
