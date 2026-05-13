# Trace Schema

This document defines the trace schema for the Reasoning Planning Agents repository.

A trace is the inspectable record of an agent run. It should show how a goal became subtasks, how those subtasks became a plan, what happened during execution, what failed, what changed, and how the final result was evaluated.

## Core principle

If the agent cannot produce a trace, the agent cannot be debugged.

Every prototype in this repository should output a trace.

## Minimal trace flow

```text
Goal
→ Decomposition
→ Plan
→ Execution Results
→ Observations
→ Reflections
→ Revisions
→ Evaluation
```

## Trace object

A minimal trace should include:

```text
trace_id
goal_id
project
steps
summary
status
```

Example:

```text
trace_id: trace_goal_publish_blog
goal_id: goal_publish_blog
project: task_decomposition_agent
status: success
summary: Goal decomposed into 6 subtasks with valid dependencies.
```

## Trace step

Each trace step should be explicit.

Minimal fields:

```text
step_id
stage
input
output
status
notes
```

Example:

```text
step_id: trace_step_001
stage: decomposition
input: goal_publish_blog
output: 6 subtasks generated
status: success
notes: Subtasks include outline, draft, review, and publish.
```

## Supported stages

```text
goal_received
goal_validation
decomposition
planning
execution
observation
reflection
revision
evaluation
final_summary
```

## Status values

```text
success
failure
partial
blocked
skipped
not_run
```

## Trace quality levels

| Level | Meaning |
|---|---|
| none | No trace is produced |
| low | Trace exists but misses major stages |
| medium | Trace includes major stages but lacks detail |
| high | Trace shows inputs, outputs, status, and reasoning at each stage |

## Project 01 trace

Task Decomposition Agent should produce:

```text
goal_received
subtasks_generated
dependencies_created
execution_order_created
evaluation_completed
```

Example:

```text
Goal: publish technical blog post
Generated subtasks: define audience, research, outline, draft, review, publish
Dependencies: outline before draft, draft before review, review before publish
Execution order: define audience → research → outline → draft → review → publish
Evaluation: valid decomposition
```

## Project 02 trace

Planner-Executor Agent should produce:

```text
plan_created
step_executed
step_result_recorded
final_plan_status
```

Example:

```text
Plan created with 5 steps
Step 1 executed: success
Step 2 executed: success
Step 3 executed: failure
Final status: partial
```

## Project 03 trace

Reflection Agent should produce:

```text
failure_observed
cause_analyzed
reflection_generated
revision_proposed
revision_applied
```

Example:

```text
Failure observed: draft blocked
Cause: target audience missing
Reflection: add audience definition before outline
Revision: inserted new step
Status: revised plan created
```

## Project 04 trace

Multi-Agent Planning should produce:

```text
goal_received
roles_assigned
agent_plans_created
conflicts_detected
shared_plan_created
coordination_summary
```

Example:

```text
Roles assigned: decomposer, planner, critic, coordinator
Conflict detected: planner skipped review step
Coordinator revision: added review step before publish
Shared plan status: valid
```

## Integrated trace

The integrated demo should produce:

```text
Goal
→ Decomposition trace
→ Planning trace
→ Execution trace
→ Reflection trace
→ Revision trace
→ Coordination trace
→ Evaluation trace
```

The final trace should show how the system moved from goal to revised plan.

## Failure traces

Failures should be first-class trace events.

A failure trace should include:

```text
failure_id
stage
expected
actual
likely_cause
recommended_fix
status
```

Example:

```text
failure_id: failure_missing_audience
stage: execution
expected: draft_created
actual: draft_blocked
likely_cause: audience undefined
recommended_fix: add audience definition step before drafting
status: revision_needed
```

## Trace output formats

Early prototypes can output traces as:

```text
plain text
JSON
Markdown result file
```

Recommended local output:

```text
results/<project>_trace.md
```

Recommended structured output:

```text
results/<project>_trace.json
```

## Evaluation link

Traces should feed evaluation.

Evaluation should inspect:

- missing stages
- failed steps
- vague reflections
- invalid revisions
- incomplete outputs
- unclear final status

## Design rule

The trace should be useful to a human reader.

A good trace answers:

```text
What was the goal?
What did the agent decide?
Why did it decide that?
What happened?
What changed?
Was the outcome acceptable?
```

If the trace does not answer those questions, the agent is not yet inspectable.
