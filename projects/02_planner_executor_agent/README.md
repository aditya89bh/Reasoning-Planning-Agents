# Project 02: Planner-Executor Agent

This project extends task decomposition into an executable planning loop.

The goal is to convert subtasks into an ordered plan, simulate execution step by step, record step results, and produce an inspectable execution trace.

## Core question

```text
Can an agent turn subtasks into an executable plan and track what happened during execution?
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

## Current status

```text
Design phase
```

This project does not yet have the runnable implementation. The immediate goal is to define the plan schema, execution result schema, demo plans, tests, and result examples.

## Target loop

```text
Goal → Subtasks → Plan → Execute Steps → Step Results → Final Trace → Evaluation
```

## Components

| Component | Role |
|---|---|
| Plan model | Stores ordered execution structure |
| PlanStep model | Represents one executable step |
| Planner | Converts subtasks into an ordered plan |
| Executor | Simulates or performs each plan step |
| StepResult model | Records success, failure, output, and error |
| Evaluator | Checks plan validity and execution result |
| Trace generator | Shows the full plan-execution path |

## Plan schema

A minimal plan should include:

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
  - step_review_clarity
  - step_publish_article
status: ready
version: 1
```

## PlanStep schema

A minimal plan step should include:

```text
step_id
plan_id
subtask_id
description
expected_output
status
```

Example:

```text
step_id: step_create_outline
plan_id: plan_publish_blog_v1
subtask_id: subtask_create_outline
description: Create a structured article outline.
expected_output: outline_created
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
result_id: result_create_outline
step_id: step_create_outline
status: success
output: outline_created
error: none
notes: Outline contains introduction, argument, examples, and conclusion.
```

## Execution behavior

The first prototype should use simulated execution.

Example:

```text
step_define_audience → success → audience_defined
step_create_outline → success → outline_created
step_write_draft → success → draft_written
step_review_clarity → success → review_completed
step_publish_article → success → article_published
```

Failure examples should also be supported:

```text
step_write_draft → failure → missing_audience
```

## Trace behavior

The trace should show:

```text
Plan created
Step 1 executed
Step 2 executed
Step 3 failed or succeeded
Final plan status computed
Evaluation completed
```

Example trace:

```text
Plan created: plan_publish_blog_v1
Step executed: step_define_audience → success
Step executed: step_create_outline → success
Step executed: step_write_draft → success
Step executed: step_review_clarity → success
Step executed: step_publish_article → success
Final status: complete
```

## Evaluation metrics

| Metric | Meaning |
|---|---|
| Plan validity | Is the plan executable? |
| Step count | Number of plan steps |
| Step success rate | Ratio of successful steps |
| Failure visibility | Are failed steps explicit? |
| Final status correctness | Is the plan status computed correctly? |
| Trace clarity | Can a human inspect the execution path? |

## Planned file structure

```text
projects/02_planner_executor_agent/
├── README.md
├── src/
│   ├── plan.py
│   ├── planner.py
│   ├── executor.py
│   └── evaluator.py
├── examples/
│   └── demo_plans.json
├── tests/
│   └── test_planner_executor.py
└── results/
    └── execution_examples.md
```

## Minimum viable demo

The first demo should load a few structured plans and produce:

- ordered plan
- simulated step execution
- step results
- final plan status
- evaluation result
- trace

Run command target:

```bash
python projects/02_planner_executor_agent/run_demo.py
```

Test command target:

```bash
python -m pytest projects/02_planner_executor_agent/tests
```

## Current limitations

- No runnable implementation yet.
- No real tool execution yet.
- No external APIs yet.
- No reflection or revision yet.
- No multi-agent coordination yet.

## Next steps

1. Add `src/plan.py`.
2. Add `src/planner.py`.
3. Add `src/executor.py`.
4. Add `src/evaluator.py`.
5. Add demo plans.
6. Add runnable demo.
7. Add tests.
8. Add result examples.
9. Update this README to runnable prototype status.

## Completion target

This project reaches first milestone when it has:

- plan model
- planner
- simulated executor
- step result tracking
- final status computation
- trace output
- tests
- result artifact

At that point, Project 02 becomes the execution layer of the planning-agent stack.
