# Evaluation

This document defines the evaluation approach for the Reasoning Planning Agents repository.

The goal is to avoid vague claims like "the agent worked." Each prototype should define what success means, what failure looks like, and how the agent trace can be inspected.

## Core evaluation principle

A reasoning/planning agent should be evaluated on process quality, not just final output.

A useful agent should produce:

```text
clear goal → valid decomposition → executable plan → traceable execution → grounded reflection → useful revision
```

## Evaluation dimensions

| Dimension | Question |
|---|---|
| Goal clarity | Is the goal specific enough to act on? |
| Decomposition quality | Are subtasks clear, necessary, and complete? |
| Dependency correctness | Are prerequisites and ordering constraints valid? |
| Plan validity | Can the plan realistically be executed? |
| Execution tracking | Are step outcomes recorded clearly? |
| Reflection quality | Does reflection identify specific causes? |
| Revision usefulness | Does the revised plan improve the original plan? |
| Traceability | Can a human inspect the agent loop? |
| Robustness | Does the agent handle missing information or failure? |
| Completion | Did the agent reach the success criteria? |

## Goal clarity

A goal is clear when it includes:

```text
description
success_criteria
constraints
context
```

Weak goal:

```text
Build an agent.
```

Better goal:

```text
Build a deterministic task decomposition agent that converts a goal into ordered subtasks with dependencies and a trace.
```

Evaluation labels:

| Label | Meaning |
|---|---|
| unclear | Goal cannot guide planning |
| partial | Goal is usable but missing criteria or constraints |
| clear | Goal has enough detail for decomposition |

## Decomposition quality

A decomposition is useful when subtasks are:

- specific
- necessary
- non-overlapping
- small enough to execute
- linked to the original goal

Bad decomposition:

```text
1. Do research
2. Do work
3. Finish
```

Better decomposition:

```text
1. Define target audience
2. Collect source notes
3. Create outline
4. Write first draft
5. Review clarity
6. Publish
```

Metrics:

```text
subtask_count
missing_required_subtasks
duplicate_subtasks
ambiguous_subtasks
```

## Dependency correctness

Dependencies define which subtasks must happen before others.

Example:

```text
write_draft depends_on create_outline
review_clarity depends_on write_draft
publish depends_on review_clarity
```

Common failures:

- missing dependencies
- circular dependencies
- impossible ordering
- subtasks marked independent when they are not

Metrics:

```text
dependency_count
circular_dependencies=true|false
invalid_dependencies=[]
execution_order_valid=true|false
```

## Plan validity

A plan is valid when it can be executed in sequence.

A valid plan should include:

```text
plan_id
goal_id
steps
dependencies
assumptions
risks
success_criteria
```

Plan quality labels:

| Label | Meaning |
|---|---|
| invalid | Cannot be executed |
| partial | Executable but missing detail |
| valid | Clear ordered execution path |

## Execution tracking

Execution tracking records what happened at each step.

Minimum step result:

```text
step_id
status
output
error
notes
```

Useful statuses:

```text
pending
running
success
failure
blocked
skipped
```

The agent should not hide failed steps.

## Reflection quality

Reflection should explain what happened and why.

A useful reflection includes:

```text
observed_issue
likely_cause
impact
recommended_revision
confidence
```

Bad reflection:

```text
The step failed. Try again.
```

Better reflection:

```text
The draft step failed because the target audience was undefined. Add an audience definition step before drafting.
```

Reflection quality labels:

| Label | Meaning |
|---|---|
| none | No reflection generated |
| generic | Reflection exists but is vague |
| specific | Reflection identifies concrete cause |
| actionable | Reflection proposes useful revision |

## Revision usefulness

A revision is useful when it changes the plan in a way that addresses the failure.

Revision types:

```text
add_step
remove_step
reorder_step
replace_step
mark_blocked
```

Evaluation questions:

- Did the revision address the actual failure?
- Did it introduce new dependency issues?
- Did it improve the execution path?
- Is the new plan version traceable?

## Traceability

Every prototype should produce a trace.

Minimum trace fields:

```text
goal
subtasks
plan
execution_results
observations
reflections
revisions
evaluation
```

Trace clarity labels:

| Label | Meaning |
|---|---|
| none | No trace produced |
| low | Trace exists but is incomplete |
| medium | Major steps visible |
| high | Goal, plan, execution, reflection, and evaluation are inspectable |

## Robustness

Robustness measures how the agent behaves under imperfect input.

Test cases should include:

- vague goals
- missing success criteria
- impossible dependencies
- failed steps
- contradictory constraints
- blocked execution

Expected behavior:

```text
agent should surface the issue instead of hallucinating completion
```

## Project-specific evaluation

## Project 01: Task Decomposition Agent

Primary metrics:

- goal clarity
- subtask quality
- dependency correctness
- execution order validity
- trace clarity

Minimum result table:

| Goal | Subtasks | Dependencies valid | Execution order valid | Trace clarity |
|---|---:|---:|---:|---|
| publish blog post | 6 | true | true | high |

## Project 02: Planner-Executor Agent

Primary metrics:

- plan validity
- execution tracking
- step success rate
- failure visibility
- final trace clarity

Minimum result table:

| Goal | Steps | Successful steps | Failed steps | Plan status |
|---|---:|---:|---:|---|
| build demo | 5 | 5 | 0 | complete |

## Project 03: Reflection Agent

Primary metrics:

- failure detection
- reflection specificity
- revision usefulness
- revised plan validity
- trace clarity

Minimum result table:

| Failed step | Cause identified | Revision created | Revised plan valid | Reflection quality |
|---|---:|---:|---:|---|
| write draft | true | true | true | actionable |

## Project 04: Multi-Agent Planning

Primary metrics:

- role clarity
- coordination quality
- conflict detection
- shared plan consistency
- final trace clarity

Minimum result table:

| Goal | Agents | Role clarity | Conflicts | Final plan valid |
|---|---:|---:|---:|---:|
| launch article | 4 | true | 0 | true |

## EvaluationResult format

A minimal evaluation result should include:

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
evaluation_id: eval_001
target_id: goal_publish_blog
project: task_decomposition_agent
success: true
score: 0.9
trace_clarity: high
failure_modes: []
notes: Goal decomposed into valid ordered subtasks.
```

## Failure reporting

Failures should be explicit.

A failure report should include:

```text
failure_id
target_id
failure_type
failed_layer
expected
actual
likely_cause
recommended_fix
```

Failure types:

```text
vague_goal
bad_decomposition
invalid_dependency
execution_failure
generic_reflection
bad_revision
trace_missing
```

## Completion criteria

A project should not be called complete unless it has:

- runnable examples
- expected outputs
- evaluation metrics
- result table
- failure cases
- traces
- basic tests

## Summary

The evaluation standard for this repository is:

```text
structured goal handling + valid plan + visible execution + useful reflection + inspectable trace
```

That is the bar for every agent prototype.
