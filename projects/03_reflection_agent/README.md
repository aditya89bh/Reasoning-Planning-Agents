# Project 03: Reflection Agent

This project adds failure analysis, reflection, and plan revision to the reasoning-planning stack.

The goal is to inspect failed or blocked execution steps, identify likely causes, propose useful revisions, and generate a trace explaining what changed.

## Core question

```text
Can an agent reflect on execution failure and revise the plan in a useful way?
```

## Current status

```text
Runnable first prototype
```

This project now includes:

- observation data model
- reflection data model
- revision data model
- deterministic failure analyzer
- deterministic plan reviser
- reflection evaluator
- failure-case examples
- command-line demo
- tests
- reflection result examples

Estimated project status:

```text
65-70% complete
```

## Why this matters

Planning agents fail in the real world.

A useful agent should not just stop when a step fails. It should be able to:

- detect the failure
- understand what went wrong
- identify the likely cause
- recommend a revision
- update the plan
- explain the change

Reflection turns execution failure into correction.

## Target loop

```text
Observation → Failure Analysis → Reflection → Revision → Evaluation → Trace
```

## Components

| File | Role |
|---|---|
| `src/reflection.py` | Defines `Observation`, `Reflection`, `Revision`, and `ReflectionResult` |
| `src/failure_analyzer.py` | Maps observed errors to likely causes and recommended revisions |
| `src/reviser.py` | Converts recommended revisions into concrete `Revision` objects |
| `src/evaluator.py` | Evaluates reflection specificity, revision usefulness, and trace clarity |
| `examples/failure_cases.json` | Provides deterministic failure observations |
| `run_demo.py` | Runs the reflection demo from the command line |
| `tests/test_reflection.py` | Regression tests for reflection behavior |
| `results/reflection_examples.md` | Documents expected reflection and revision behavior |

## Observation schema

A minimal observation includes:

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
step_id: step_define_audience
status: failure
observed_error: missing_audience
state_change: draft_blocked
notes: The article workflow cannot proceed because the target audience was not defined.
```

## Reflection schema

A reflection includes:

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
reflection_id: reflection_obs_missing_audience
observation_id: obs_missing_audience
observed_issue: Audience definition step failed.
likely_cause: The goal does not contain enough audience context.
impact: Drafting and review quality will be unstable without a target reader.
recommended_revision: add_audience_definition_step
confidence: 0.9
```

## Revision schema

A revision modifies or blocks a plan.

```text
revision_id
reflection_id
revision_type
old_plan_id
new_plan_id
change_summary
status
```

Supported revision types:

```text
add_step
remove_step
reorder_step
replace_step
mark_blocked
```

## Demo failure cases

| Case | Observed error | Expected revision |
|---|---|---|
| `case_missing_audience` | `missing_audience` | `add_audience_definition_step` |
| `case_outline_missing` | `outline_missing` | `add_or_reorder_outline_step` |
| `case_review_skipped` | `review_skipped` | `add_review_before_publish` |
| `case_tool_unavailable` | `tool_unavailable` | `mark_step_blocked` |
| `case_blocked_dependency` | `blocked_dependency` | `reorder_plan_dependencies` |

## Reflection behavior

The current prototype uses deterministic mappings from failure type to revision.

Examples:

| Failure | Likely cause | Revision type |
|---|---|---|
| `missing_audience` | Goal lacks audience context | `add_step` |
| `outline_missing` | Draft attempted before outline | `add_step` |
| `review_skipped` | Publish attempted without review | `add_step` |
| `tool_unavailable` | Required tool unavailable | `mark_blocked` |
| `blocked_dependency` | Prerequisite missing | `reorder_step` |

Unknown failures are routed to manual review.

## Trace behavior

The trace shows:

```text
Failure observed
Observed error
Cause identified
Reflection generated
Revision proposed
Case completed
```

Example trace:

```text
Failure observed: step_define_audience status=failure
Observed error: missing_audience
Cause identified: The goal does not contain enough audience context.
Reflection generated: add_audience_definition_step
Revision proposed: add_step -> Add an audience-definition step before outline or drafting.
Case completed: case_missing_audience
```

## Evaluation metrics

| Metric | Meaning |
|---|---|
| Failure detection | Was the observation marked as failure or blocked? |
| Cause specificity | Did the system identify a concrete likely cause? |
| Reflection quality | Was the reflection actionable? |
| Revision usefulness | Did the proposed revision address the failure? |
| Trace clarity | Can a human inspect failure-to-revision behavior? |

## Run the demo

From the repository root:

```bash
python projects/03_reflection_agent/run_demo.py
```

The demo prints:

- failure case id
- observation details
- reflection object
- revision object
- evaluation result
- trace
- summary metrics

## Run tests

From the repository root:

```bash
python -m pytest projects/03_reflection_agent/tests
```

## What this prototype proves

This project proves the third layer of the planning-agent stack:

```text
execution failure → specific reflection → proposed plan revision → trace
```

That is required before building multi-agent coordination in Project 04.

## Current limitations

- Reflection is deterministic and pattern-based.
- Revisions are proposed as objects but do not yet mutate full plans.
- No LLM-based critique yet.
- No learned reflection loop yet.
- No direct Project 02 execution-result ingestion yet.
- Unknown failures route to manual review.

## Next steps

1. Run the demo locally and capture actual output.
2. Connect Project 02 failed step results to Project 03 observations.
3. Add revised-plan mutation.
4. Add richer failure cases.
5. Add Project 04 multi-agent planning.
6. Update top-level README with Project 03 runnable status.

## Completion target

This project reaches a stronger milestone when it has:

- local demo output captured in results
- direct Project 02 failure ingestion
- actual plan mutation from revisions
- integration with Project 04 critic/coordinator roles

At that point, Project 03 becomes a stronger recovery layer of the planning-agent stack.
