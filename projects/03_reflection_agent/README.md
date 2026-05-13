# Project 03: Reflection Agent

This project adds failure analysis, reflection, and plan revision to the reasoning-planning stack.

The goal is to build an agent that can inspect failed or blocked execution steps, identify likely causes, propose useful revisions, and generate a trace explaining what changed.

## Core question

```text
Can an agent reflect on execution failure and revise the plan in a useful way?
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

Reflection turns execution failure into learning and correction.

## Current status

```text
Design phase
```

This project does not yet have the runnable implementation. The immediate goal is to define failure cases, reflection schema, revision logic, tests, and result examples.

## Target loop

```text
Failed Step → Observation → Failure Analysis → Reflection → Revised Plan → Evaluation
```

## Components

| Component | Role |
|---|---|
| Observation model | Records what happened during execution |
| Failure analyzer | Identifies the likely cause of failure |
| Reflection model | Stores analysis and recommended change |
| Reviser | Applies reflection to create a revised plan |
| Evaluator | Checks whether revision is useful |
| Trace generator | Shows failure, cause, revision, and outcome |

## Observation schema

A minimal observation should include:

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
notes: Draft could not proceed because target audience was undefined.
```

## Reflection schema

A reflection should include:

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
impact: article tone and depth cannot be selected
recommended_revision: add audience definition step before drafting
confidence: 0.9
```

## Revision schema

A revision modifies the plan.

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
change_summary: Added audience definition before outline and draft.
status: applied
```

## Reflection behavior

The first prototype should use deterministic mappings from failure type to revision.

Examples:

| Failure | Likely cause | Revision |
|---|---|---|
| `target_audience_missing` | Goal lacks audience context | Add audience definition step |
| `outline_missing` | Draft attempted before outline | Add or reorder outline step before drafting |
| `review_skipped` | Publish attempted without review | Add review step before publish |
| `tool_unavailable` | Execution tool cannot run | Mark step blocked |
| `dependency_missing` | Prerequisite not completed | Reorder plan |

## Trace behavior

The trace should show:

```text
Failure observed
Likely cause identified
Reflection generated
Revision proposed
Revised plan created
Evaluation completed
```

Example trace:

```text
Failure observed: step_write_draft failed
Observed error: target_audience_missing
Likely cause: audience was not defined
Recommended revision: add audience definition step
Revision applied: plan_publish_blog_v2 created
Evaluation: revised plan valid
```

## Evaluation metrics

| Metric | Meaning |
|---|---|
| Failure detection | Was the failure surfaced clearly? |
| Cause specificity | Was the likely cause concrete? |
| Reflection quality | Was the reflection actionable? |
| Revision usefulness | Did the revision address the failure? |
| Revised plan validity | Is the new plan executable? |
| Trace clarity | Can the failure-to-revision path be inspected? |

## Planned file structure

```text
projects/03_reflection_agent/
├── README.md
├── src/
│   ├── reflection.py
│   ├── failure_analyzer.py
│   ├── reviser.py
│   └── evaluator.py
├── examples/
│   └── failure_cases.json
├── tests/
│   └── test_reflection.py
└── results/
    └── reflection_examples.md
```

## Minimum viable demo

The first demo should load failure cases and produce:

- failure analysis
- reflection note
- recommended revision
- revised plan summary
- evaluation result
- trace

Run command target:

```bash
python projects/03_reflection_agent/run_demo.py
```

Test command target:

```bash
python -m pytest projects/03_reflection_agent/tests
```

## Current limitations

- No runnable implementation yet.
- No learned reflection yet.
- No LLM-based critique yet.
- No live planner-executor integration yet.
- No multi-agent critic yet.

## Next steps

1. Add `src/reflection.py`.
2. Add `src/failure_analyzer.py`.
3. Add `src/reviser.py`.
4. Add `src/evaluator.py`.
5. Add demo failure cases.
6. Add runnable demo.
7. Add tests.
8. Add result examples.
9. Update this README to runnable prototype status.

## Completion target

This project reaches first milestone when it has:

- structured failure cases
- deterministic failure analysis
- reflection generation
- revised plan output
- evaluation
- trace output
- tests
- result artifact

At that point, Project 03 becomes the recovery layer of the planning-agent stack.
