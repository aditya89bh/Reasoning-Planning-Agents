# Reflection Examples

This document summarizes the expected behavior of the Reflection Agent prototype.

The prototype demonstrates a minimal failure-recovery loop:

```text
Observation → Failure Analysis → Reflection → Revision → Evaluation → Trace
```

The goal is not open-ended self-improvement yet. The goal is to make failure analysis and revision explicit, deterministic, inspectable, and testable.

## Demo failure cases

The demo uses `examples/failure_cases.json`.

| Case | Observed error | Expected revision |
|---|---|---|
| `case_missing_audience` | `missing_audience` | `add_audience_definition_step` |
| `case_outline_missing` | `outline_missing` | `add_or_reorder_outline_step` |
| `case_review_skipped` | `review_skipped` | `add_review_before_publish` |
| `case_tool_unavailable` | `tool_unavailable` | `mark_step_blocked` |
| `case_blocked_dependency` | `blocked_dependency` | `reorder_plan_dependencies` |

## Example 1: Missing audience

Input observation:

```text
observation_id: obs_missing_audience
step_id: step_define_audience
status: failure
observed_error: missing_audience
state_change: draft_blocked
```

Expected reflection:

```text
observed_issue: Audience definition step failed.
likely_cause: The goal does not contain enough audience context.
impact: Drafting and review quality will be unstable without a target reader.
recommended_revision: add_audience_definition_step
confidence: 0.9
```

Expected revision:

```text
revision_type: add_step
change_summary: Add an audience-definition step before outline or drafting.
status: proposed
```

## Example 2: Outline missing

Input observation:

```text
observation_id: obs_outline_missing
step_id: step_write_draft
status: failure
observed_error: outline_missing
```

Expected reflection:

```text
observed_issue: Drafting was attempted without an outline.
likely_cause: The plan is missing an outline step or has the wrong order.
recommended_revision: add_or_reorder_outline_step
```

Expected revision:

```text
revision_type: add_step
change_summary: Add or move outline creation before drafting.
```

## Example 3: Review skipped

Input observation:

```text
observation_id: obs_review_skipped
step_id: step_publish_article
status: failure
observed_error: review_skipped
```

Expected reflection:

```text
observed_issue: Publishing was attempted without review.
likely_cause: The plan omitted a quality-control step before publishing.
recommended_revision: add_review_before_publish
```

Expected revision:

```text
revision_type: add_step
change_summary: Insert a review step before publishing.
```

## Example 4: Tool unavailable

Input observation:

```text
observation_id: obs_tool_unavailable
step_id: step_deploy_project
status: blocked
observed_error: tool_unavailable
```

Expected reflection:

```text
observed_issue: Execution tool was unavailable.
likely_cause: Required external tool or runtime was not accessible.
recommended_revision: mark_step_blocked
```

Expected revision:

```text
revision_type: mark_blocked
change_summary: Mark the failed step as blocked until the required tool or environment is available.
```

## Example 5: Blocked dependency

Input observation:

```text
observation_id: obs_blocked_dependency
step_id: step_write_draft
status: blocked
observed_error: blocked_dependency
```

Expected reflection:

```text
observed_issue: Step was blocked by an unmet dependency.
likely_cause: A prerequisite step did not complete before this step ran.
recommended_revision: reorder_plan_dependencies
```

Expected revision:

```text
revision_type: reorder_step
change_summary: Reorder the plan so prerequisite steps complete before dependent steps.
```

## Expected trace shape

Each reflection run should produce a trace like:

```text
Failure observed: <step_id> status=<failure|blocked>
Observed error: <error>
Cause identified: <likely cause>
Reflection generated: <recommended revision>
Revision proposed: <revision type> -> <change summary>
Case completed: <case_id>
```

## Evaluation dimensions

| Metric | Meaning |
|---|---|
| Failure detection | Was the observation marked as failure or blocked? |
| Cause specificity | Did the system identify a concrete likely cause? |
| Reflection quality | Was the reflection actionable? |
| Revision usefulness | Did the proposed revision address the failure? |
| Trace clarity | Can a human inspect failure-to-revision behavior? |

## What this prototype proves

This project proves the third layer of the planning-agent stack:

```text
execution failure → specific reflection → proposed plan revision → trace
```

That is required before building multi-agent coordination in Project 04.

## Run command

From the repository root:

```bash
python projects/03_reflection_agent/run_demo.py
```

## Test command

From the repository root:

```bash
python -m pytest projects/03_reflection_agent/tests
```

## Current limitations

- Reflection is deterministic and pattern-based.
- Revisions are proposed as objects but do not yet mutate full plans.
- No LLM-based critique yet.
- No learned reflection loop yet.
- No direct Project 02 execution-result ingestion yet.
- Unknown failures route to manual review.

## Next improvement

The next useful step is to update this project README from design phase to runnable first prototype, then connect Project 02 failed step results to Project 03 observations.
