# Shared Interfaces

This document defines the common interfaces used across the Reasoning Planning Agents repository.

The goal is to keep the agent stack modular. Each project can evolve independently, but all projects should use compatible structures for goals, subtasks, plans, execution results, observations, reflections, revisions, and evaluation.

## Core principle

Agents should communicate through explicit structures, not hidden assumptions.

```text
Goal → Subtasks → Plan → StepResult → Observation → Reflection → Revision → EvaluationResult
```

## Interface overview

| Interface | Used by | Purpose |
|---|---|---|
| `Goal` | All projects | Defines the desired outcome |
| `Subtask` | Decomposition | Represents one unit of work |
| `Dependency` | Decomposition and planning | Represents prerequisite relationships |
| `Plan` | Planner-executor | Ordered execution structure |
| `PlanStep` | Planner-executor | One step in a plan |
| `StepResult` | Executor | Result of executing one step |
| `Observation` | Reflection | Grounded record of execution outcome |
| `Reflection` | Reflection agent | Analysis of success, failure, or blocker |
| `Revision` | Reflection and planner | Plan modification based on reflection |
| `AgentTrace` | All projects | Inspectable record of the agent loop |
| `EvaluationResult` | Evaluation layer | Measures quality and completion |

## Goal

A `Goal` describes what the agent is trying to accomplish.

Minimal fields:

```text
goal_id
description
success_criteria
constraints
context
status
```

Example:

```text
goal_id: goal_publish_blog
description: Publish a 1000-word technical blog post on planning agents.
success_criteria:
  - outline_created
  - draft_written
  - review_completed
  - article_published
constraints:
  - under_1000_words
  - technical_but_readable
context:
  audience: AI builders
status: pending
```

## Subtask

A `Subtask` is a smaller unit of work derived from a goal.

Minimal fields:

```text
subtask_id
goal_id
description
expected_output
dependencies
status
```

Example:

```text
subtask_id: subtask_create_outline
goal_id: goal_publish_blog
description: Create a structured article outline.
expected_output: outline_created
dependencies: []
status: pending
```

## Dependency

A `Dependency` defines that one subtask must happen before another.

Minimal fields:

```text
dependency_id
before_subtask_id
after_subtask_id
reason
```

Example:

```text
dependency_id: dep_outline_before_draft
before_subtask_id: subtask_create_outline
after_subtask_id: subtask_write_draft
reason: Draft requires outline first.
```

## Plan

A `Plan` orders subtasks into an executable sequence.

Minimal fields:

```text
plan_id
goal_id
steps
dependencies
assumptions
risks
status
version
```

Example:

```text
plan_id: plan_publish_blog_v1
goal_id: goal_publish_blog
steps:
  - step_define_audience
  - step_create_outline
  - step_write_draft
  - step_review
  - step_publish
status: ready
version: 1
```

## PlanStep

A `PlanStep` is one executable step in a plan.

Minimal fields:

```text
step_id
plan_id
subtask_id
description
expected_output
status
```

Statuses:

```text
pending
running
success
failure
blocked
skipped
```

## StepResult

A `StepResult` records what happened when a step executed.

Minimal fields:

```text
result_id
step_id
status
output
error
notes
```

Example:

```text
result_id: result_step_outline
step_id: step_create_outline
status: success
output: outline_created
error: none
notes: Outline contains 5 sections.
```

## Observation

An `Observation` turns a step result into evidence for reflection.

Minimal fields:

```text
observation_id
step_id
status
observed_output
observed_error
state_change
notes
```

Example:

```text
observation_id: obs_missing_audience
step_id: step_write_draft
status: failure
observed_error: target_audience_missing
state_change: draft_blocked
notes: Draft could not proceed because audience was undefined.
```

## Reflection

A `Reflection` analyzes an observation.

Minimal fields:

```text
reflection_id
observation_id
observed_issue
likely_cause
impact
recommended_revision
confidence
```

Example:

```text
reflection_id: reflection_missing_audience
observation_id: obs_missing_audience
observed_issue: draft step failed
likely_cause: target audience was undefined
impact: article tone and depth cannot be chosen
recommended_revision: add audience definition step before outline
confidence: 0.9
```

## Revision

A `Revision` modifies a plan based on reflection.

Minimal fields:

```text
revision_id
reflection_id
revision_type
old_plan_id
new_plan_id
change_summary
status
```

Revision types:

```text
add_step
remove_step
reorder_step
replace_step
mark_blocked
```

Example:

```text
revision_id: rev_add_audience_step
reflection_id: reflection_missing_audience
revision_type: add_step
old_plan_id: plan_publish_blog_v1
new_plan_id: plan_publish_blog_v2
change_summary: Added audience definition before outline.
status: applied
```

## AgentTrace

An `AgentTrace` is the debugging surface for the agent loop.

Minimal fields:

```text
trace_id
goal
subtasks
plan
step_results
observations
reflections
revisions
evaluation
notes
```

A useful trace should answer:

- What was the goal?
- How was it decomposed?
- What plan was created?
- What executed successfully?
- What failed?
- What was reflected on?
- What changed?
- Was the final outcome acceptable?

## EvaluationResult

An `EvaluationResult` measures the quality of a goal, plan, execution, reflection, or full agent loop.

Minimal fields:

```text
evaluation_id
target_id
project
success
score
trace_clarity
failure_modes
notes
```

Example:

```text
evaluation_id: eval_goal_publish_blog
target_id: goal_publish_blog
project: task_decomposition_agent
success: true
score: 0.9
trace_clarity: high
failure_modes: []
notes: Goal decomposed into valid ordered subtasks.
```

## Versioning note

These interfaces are intentionally minimal. They should evolve as the projects become runnable.

The first priority is consistency, not completeness.

## Integration target

The long-term integrated loop should look like this:

```text
Goal
→ Subtasks
→ Plan
→ StepResult
→ Observation
→ Reflection
→ Revision
→ EvaluationResult
→ AgentTrace
```

This gives each project a defined role in the larger planning-agent architecture.
