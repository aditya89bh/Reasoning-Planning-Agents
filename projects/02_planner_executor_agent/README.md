# Project 02: Planner-Executor Agent

This project extends task decomposition into an executable planning loop.

The goal is to convert structured plan specs into ordered plans, simulate execution step by step, record step results, and produce an inspectable execution trace.

## Core question

```text
Can an agent turn subtasks into an executable plan and track what happened during execution?
```

## Current status

```text
Runnable first prototype
```

This project now includes:

- plan data model
- plan step data model
- step result data model
- execution result data model
- deterministic planner
- simulated executor
- execution evaluator
- demo plans
- command-line demo
- tests
- execution result examples

Estimated project status:

```text
65-70% complete
```

## Why this matters

A plan is not useful unless it can be executed and inspected.

Many agent systems generate plausible plans but fail to track:

- which step is currently running
- which steps succeeded
- which steps failed
- what output each step produced
- whether the plan is complete, partial, blocked, or failed

The planner-executor loop gives the agent operational structure.

## Target loop

```text
Plan Spec → Plan Object → Execute Steps → Step Results → Final Status → Evaluation → Trace
```

## Components

| File | Role |
|---|---|
| `src/plan.py` | Defines `Plan`, `PlanStep`, `StepResult`, and `ExecutionResult` |
| `src/planner.py` | Builds plan objects from structured specs and validates structure |
| `src/executor.py` | Simulates plan execution, dependency checks, failures, and final status |
| `src/evaluator.py` | Evaluates plan validity, execution results, and trace clarity |
| `examples/demo_plans.json` | Provides successful and failure-case demo plans |
| `run_demo.py` | Runs the planner-executor demo from the command line |
| `tests/test_planner_executor.py` | Regression tests for planner-executor behavior |
| `results/execution_examples.md` | Documents expected execution behavior |

## Plan schema

A minimal plan includes:

```text
plan_id
goal_id
description
steps
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
  - step_review_clarity
  - step_publish_article
status: ready
version: 1
```

## PlanStep schema

A minimal plan step includes:

```text
step_id
plan_id
description
expected_output
dependencies
status
```

Example:

```text
step_id: step_create_outline
plan_id: plan_publish_blog_v1
description: Create a structured article outline.
expected_output: outline_created
dependencies:
  - step_define_audience
status: pending
```

## StepResult schema

A step result records what happened when a step executed.

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
result_id: result_step_create_outline
step_id: step_create_outline
status: success
output: outline_created
error: none
notes: Step completed successfully.
```

## Demo scenarios

The current demo includes:

| Plan | Scenario | Expected final status |
|---|---|---|
| `plan_publish_blog_v1` | Successful publishing workflow | `complete` |
| `plan_publish_blog_missing_audience` | Forced failure on audience definition | `failed` |
| `plan_build_agent_demo_v1` | Successful software-agent demo workflow | `complete` |

## Execution behavior

The prototype uses simulated execution.

Success example:

```text
step_define_audience → success → audience_defined
step_create_outline → success → outline_created
step_write_draft → success → draft_written
step_review_clarity → success → review_completed
step_publish_article → success → article_published
```

Failure example:

```text
step_define_audience → failure → missing_audience
step_create_outline → blocked → missing dependency
step_write_draft → blocked → missing dependency
```

## Trace behavior

The execution trace shows:

```text
Execution started
Step executed / failed / blocked
Final status computed
Execution completed
```

Example trace:

```text
Execution started: plan_publish_blog_v1
Step executed: step_define_audience -> success -> audience_defined
Step executed: step_create_outline -> success -> outline_created
Final status: complete
Execution completed
```

## Evaluation metrics

| Metric | Meaning |
|---|---|
| Plan validity | Does the plan have valid structure and dependencies? |
| Step count | Number of plan steps |
| Successful steps | Number of successful steps |
| Failed steps | Number of explicit failures |
| Blocked steps | Number of dependency-blocked steps |
| Final status correctness | Is the plan status computed correctly? |
| Trace clarity | Can a human inspect the execution path? |

## Run the demo

From the repository root:

```bash
python projects/02_planner_executor_agent/run_demo.py
```

The demo prints:

- plan id
- goal id
- plan steps
- step results
- planning trace
- execution trace
- evaluation result
- final summary

## Run tests

From the repository root:

```bash
python -m pytest projects/02_planner_executor_agent/tests
```

## What this prototype proves

This project proves the second layer of the planning-agent stack:

```text
structured plan → deterministic execution → visible step results → final status → trace
```

That is required before adding reflection and revision in Project 03.

## Current limitations

- Execution is simulated.
- No real tool calls yet.
- No external APIs yet.
- No dynamic replanning yet.
- No reflection or revision yet.
- Plans are loaded from structured JSON instead of generated from Project 01 output.

## Next steps

1. Run the demo locally and capture actual output.
2. Connect Project 01 decomposition output to Project 02 planning input.
3. Add more failure cases.
4. Add partial execution examples.
5. Add Project 03 reflection integration.
6. Update top-level README with Project 02 runnable status.

## Completion target

This project reaches a stronger milestone when it has:

- local demo output captured in results
- connection to Project 01 output
- richer failure and blocked-step examples
- integration with Project 03 reflection

At that point, Project 02 becomes a stronger execution layer of the planning-agent stack.
