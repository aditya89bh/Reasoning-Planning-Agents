# Project 01: Task Decomposition Agent

This project builds the first runnable prototype in the Reasoning Planning Agents repository.

The goal is to convert a high-level goal into structured subtasks, dependencies, an execution order, and an inspectable trace.

## Core question

```text
Can an agent convert a goal into useful subtasks and a valid execution order?
```

## Current status

```text
Runnable first prototype
```

This project now includes:

- goal data model
- subtask data model
- dependency data model
- deterministic decomposer
- decomposition evaluator
- demo goals
- command-line demo
- tests
- decomposition result examples

Estimated project status:

```text
65-70% complete
```

## Why this matters

Planning fails when decomposition is weak.

If an agent cannot break a goal into clear subtasks, every later stage becomes unstable:

- planning becomes vague
- execution becomes brittle
- reflection becomes generic
- multi-agent coordination becomes chaos

Task decomposition is the first layer of a useful planning agent.

## Target loop

```text
Goal → Subtasks → Dependencies → Execution Order → Trace → Evaluation
```

## Components

| File | Role |
|---|---|
| `src/task.py` | Defines `Goal`, `Subtask`, `Dependency`, and `DecompositionResult` |
| `src/decomposer.py` | Converts goals into subtasks, dependencies, execution order, and trace |
| `src/evaluator.py` | Evaluates goal clarity, dependency validity, execution order, and trace clarity |
| `examples/demo_goals.json` | Provides structured demo goals |
| `run_demo.py` | Runs the decomposition demo from the command line |
| `tests/test_decomposition.py` | Regression tests for decomposition behavior |
| `results/decomposition_examples.md` | Documents expected output behavior |

## Goal schema

A minimal goal includes:

```text
goal_id
description
success_criteria
constraints
context
```

Example:

```text
goal_id: goal_publish_blog
description: Publish a technical blog post about planning agents.
success_criteria:
  - outline_created
  - draft_written
  - review_completed
  - article_published
constraints:
  - technical but readable
  - under 1200 words
context:
  audience: AI builders
```

## Decomposition behavior

The first prototype uses deterministic templates.

Current goal types:

| Goal type | Trigger examples | Template output |
|---|---|---|
| `publishing` | article, blog, publish, writing, newsletter | audience, outline, draft, review, publish |
| `software_project` | software, system, application, agent, platform, deploy | requirements, architecture, implementation, tests, deployment |
| `generic` | fallback | analyze, plan, execute, review |

## Example: publishing goal

Input goal:

```text
Publish a technical blog post about planning agents for AI builders.
```

Expected subtasks:

```text
1. subtask_define_audience
2. subtask_create_outline
3. subtask_write_draft
4. subtask_review_clarity
5. subtask_publish_article
```

Expected dependencies:

```text
subtask_define_audience → subtask_create_outline
subtask_create_outline → subtask_write_draft
subtask_write_draft → subtask_review_clarity
subtask_review_clarity → subtask_publish_article
```

## Trace behavior

The trace shows:

```text
Goal received
Goal classified
Subtasks generated
Dependencies created
Execution order created
Decomposition completed
```

Example trace:

```text
Goal received: publish technical blog post
Goal classified as: publishing
Generated 5 subtasks
Generated 4 dependencies
Execution order created
Decomposition completed
```

## Evaluation metrics

| Metric | Meaning |
|---|---|
| Goal clarity | Is the goal specific enough to decompose? |
| Subtask count | Number of generated subtasks |
| Dependency validity | Are prerequisite relationships valid? |
| Execution order validity | Can subtasks be executed in order? |
| Trace clarity | Is the decomposition process inspectable? |

## Run the demo

From the repository root:

```bash
python projects/01_task_decomposition_agent/run_demo.py
```

The demo prints:

- goal id
- goal type
- subtasks
- dependencies
- execution order
- evaluation result
- trace
- summary

## Run tests

From the repository root:

```bash
python -m pytest projects/01_task_decomposition_agent/tests
```

## What this prototype proves

This project proves the first layer of the planning-agent stack:

```text
high-level goal → structured subtasks → valid execution order → inspectable trace
```

That is the foundation required before planner-executor, reflection, and multi-agent coordination layers.

## Current limitations

- Goal classification is keyword-based.
- Decomposition is template-based.
- No LLM integration yet.
- No open-ended goal parsing yet.
- No execution layer yet.
- No reflection or revision yet.
- Dependencies are linear for the first prototype.

## Next steps

1. Run the demo locally and capture actual output.
2. Add more goal templates.
3. Add ambiguous-goal handling.
4. Add non-linear dependencies.
5. Connect this output to Project 02 planner-executor.
6. Update top-level README with Project 01 runnable status.

## Completion target

This project reaches a stronger milestone when it has:

- more goal templates
- local demo output captured in results
- non-linear dependency examples
- connection to Project 02

At that point, Project 01 becomes a stronger decomposition layer for the planning-agent stack.
