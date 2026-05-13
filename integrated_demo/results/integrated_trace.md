# Integrated Trace

This document summarizes the expected behavior of the integrated reasoning-planning demo.

The integrated demo connects all four project prototypes:

```text
Project 01: Task Decomposition
Project 02: Planner-Executor
Project 03: Reflection Agent
Project 04: Multi-Agent Planning
```

## Integrated flow

```text
Goal
→ Decomposition
→ Plan creation
→ Forced execution failure
→ Failure observation
→ Reflection
→ Revision proposal
→ Multi-agent coordination
→ Final shared plan
```

## Input goal

```text
Publish a technical blog post about planning agents for AI builders.
```

## Expected Project 01 output

The goal should be classified as:

```text
publishing
```

Expected subtasks:

```text
subtask_define_audience
subtask_create_outline
subtask_write_draft
subtask_review_clarity
subtask_publish_article
```

## Expected Project 02 output

The integrated demo converts the decomposition output into a planner-executor plan.

The demo intentionally forces this failure:

```text
step_define_audience → missing_audience
```

Expected final execution status:

```text
failed
```

This creates a failure observation for Project 03.

## Expected Project 03 output

Expected observation:

```text
observed_error: missing_audience
status: failure
```

Expected reflection recommendation:

```text
add_audience_definition_step
```

Expected revision:

```text
revision_type: add_step
change_summary: Add an audience-definition step before outline or drafting.
```

## Expected Project 04 output

The reflection/revision signal is passed into the critic/coordinator layer.

Expected shared plan steps:

```text
1. define_audience
2. create_outline
3. write_draft
4. review_clarity
5. publish_article
```

Expected shared plan status:

```text
valid
```

## Expected trace shape

The integrated demo should print:

```text
Integrated demo started
Goal decomposed as: publishing
Subtasks generated: 5
Plan executed with final status: failed
Failure observed: missing_audience
Reflection recommendation: add_audience_definition_step
Revision proposed: add_step -> Add an audience-definition step before outline or drafting.
Shared plan status: valid
Shared plan steps: define_audience, create_outline, write_draft, review_clarity, publish_article
Integrated demo completed
```

## What this proves

The integrated demo proves that the repository is not only a set of disconnected examples.

It connects:

```text
decomposition → execution → failure observation → reflection → revision → coordination
```

This is the first end-to-end planning-agent loop in the repository.

## Run command

From the repository root:

```bash
python integrated_demo/run_integrated_demo.py
```

## Current limitations

- The integration is deterministic.
- The execution failure is forced.
- The revision is proposed but does not mutate the original Project 02 plan.
- The coordinator uses the revision signal indirectly through critic contribution.
- No LLM or external tools are used yet.

## Next improvement

The next useful step is to run this locally, capture actual output, and add it as a local output artifact.
