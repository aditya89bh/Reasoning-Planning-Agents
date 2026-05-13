# Execution Examples

This document summarizes the expected behavior of the Planner-Executor Agent prototype.

The prototype demonstrates a minimal execution loop:

```text
Plan Spec → Plan Object → Step Execution → Step Results → Final Status → Evaluation → Trace
```

The goal is not real tool execution yet. The goal is to make planning and execution state explicit, deterministic, inspectable, and testable.

## Demo plans

The demo uses `examples/demo_plans.json`.

| Plan | Scenario | Expected final status |
|---|---|---|
| `plan_publish_blog_v1` | Successful publishing workflow | `complete` |
| `plan_publish_blog_missing_audience` | Forced failure on audience definition | `failed` |
| `plan_build_agent_demo_v1` | Successful software-agent demo workflow | `complete` |

## Example 1: Successful publishing plan

Input plan:

```text
plan_publish_blog_v1
```

Expected steps:

```text
step_define_audience → audience_defined
step_create_outline → outline_created
step_write_draft → draft_written
step_review_clarity → review_completed
step_publish_article → article_published
```

Expected dependencies:

```text
step_define_audience → step_create_outline
step_create_outline → step_write_draft
step_write_draft → step_review_clarity
step_review_clarity → step_publish_article
```

Expected step results:

```text
step_define_audience: success
step_create_outline: success
step_write_draft: success
step_review_clarity: success
step_publish_article: success
```

Expected final status:

```text
complete
```

Expected evaluation:

```text
success: true
plan_valid: true
step_count: 5
successful_steps: 5
failed_steps: 0
blocked_steps: 0
final_status: complete
trace_clarity: high
```

## Example 2: Forced audience failure

Input plan:

```text
plan_publish_blog_missing_audience
```

Forced failure:

```text
step_define_audience → missing_audience
```

Expected step results:

```text
step_define_audience: failure
step_create_outline: blocked
step_write_draft: blocked
```

Expected final status:

```text
failed
```

Expected trace shape:

```text
Execution started: plan_publish_blog_missing_audience
Step failed: step_define_audience error=missing_audience
Step blocked: step_create_outline missing dependencies ['step_define_audience']
Step blocked: step_write_draft missing dependencies ['step_create_outline']
Final status: failed
Execution completed
```

## Example 3: Successful software-agent demo plan

Input plan:

```text
plan_build_agent_demo_v1
```

Expected steps:

```text
step_define_requirements → requirements_defined
step_design_architecture → architecture_defined
step_implement_core_logic → core_logic_implemented
step_run_tests → tests_completed
step_deploy_project → deployment_completed
```

Expected final status:

```text
complete
```

## Expected trace shape

Each execution should produce a trace like:

```text
Execution started: <plan_id>
Step executed: <step_id> -> success -> <expected_output>
...
Final status: <complete|failed|blocked|partial>
Execution completed
```

## Evaluation dimensions

| Metric | Meaning |
|---|---|
| Plan validity | Does the plan have valid structure and dependencies? |
| Step count | How many steps were executed or attempted? |
| Successful steps | How many steps completed successfully? |
| Failed steps | How many steps failed explicitly? |
| Blocked steps | How many steps were blocked by unmet dependencies? |
| Final status | Is final status computed correctly? |
| Trace clarity | Does the trace expose execution behavior? |

## What this prototype proves

This project proves the second layer of the planning-agent stack:

```text
structured plan → deterministic execution → visible step results → final status → trace
```

That is required before adding reflection and revision in Project 03.

## Run command

From the repository root:

```bash
python projects/02_planner_executor_agent/run_demo.py
```

## Test command

From the repository root:

```bash
python -m pytest projects/02_planner_executor_agent/tests
```

## Current limitations

- Execution is simulated.
- No real tool calls yet.
- No external APIs yet.
- No dynamic replanning yet.
- No reflection or revision yet.
- Plans are loaded from structured JSON instead of generated from Project 01 output.

## Next improvement

The next useful step is to update this project README from design phase to runnable first prototype, then connect Project 01 decomposition output to Project 02 planning input.
