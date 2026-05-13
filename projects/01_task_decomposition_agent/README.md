# Project 01: Task Decomposition Agent

This project builds the first runnable prototype in the Reasoning Planning Agents repository.

The goal is to convert a high-level goal into structured subtasks, dependencies, an execution order, and an inspectable trace.

## Core question

```text
Can an agent convert a goal into useful subtasks and a valid execution order?
```

## Why this matters

Planning fails when decomposition is weak.

If an agent cannot break a goal into clear subtasks, every later stage becomes unstable:

- planning becomes vague
- execution becomes brittle
- reflection becomes generic
- multi-agent coordination becomes chaos

Task decomposition is the first layer of a useful planning agent.

## Current status

```text
Design phase
```

This project does not yet have the runnable implementation. The immediate goal is to define the schema, demo inputs, decomposition logic, tests, and result examples.

## Target loop

```text
Goal → Subtasks → Dependencies → Execution Order → Trace → Evaluation
```

## Components

| Component | Role |
|---|---|
| Goal model | Defines the desired outcome |
| Subtask model | Represents one decomposed unit of work |
| Dependency model | Captures prerequisite relationships |
| Decomposer | Converts goal templates into subtasks |
| Evaluator | Checks decomposition quality and execution order |
| Trace generator | Shows how the decomposition was created |

## Goal schema

A minimal goal should include:

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

## Subtask schema

A minimal subtask should include:

```text
subtask_id
goal_id
description
expected_output
dependencies
status
```

Example:

```text
subtask_id: subtask_create_outline
goal_id: goal_publish_blog
description: Create a structured outline for the article.
expected_output: outline_created
dependencies:
  - subtask_define_audience
status: pending
```

## Dependency schema

A dependency defines ordering between subtasks.

```text
dependency_id
before_subtask_id
after_subtask_id
reason
```

Example:

```text
dependency_id: dep_outline_before_draft
before_subtask_id: subtask_create_outline
after_subtask_id: subtask_write_draft
reason: Drafting requires an outline first.
```

## Decomposition behavior

The first prototype should use deterministic templates.

Example goal:

```text
Publish a technical blog post about planning agents.
```

Expected subtasks:

```text
1. Define target audience
2. Create outline
3. Write draft
4. Review clarity
5. Publish article
```

Expected dependencies:

```text
define audience → create outline
create outline → write draft
write draft → review clarity
review clarity → publish article
```

## Trace behavior

The trace should show:

```text
Goal received
Goal classified
Subtasks generated
Dependencies created
Execution order created
Evaluation completed
```

Example trace:

```text
Goal received: publish technical blog post
Goal type: publishing
Generated 5 subtasks
Generated 4 dependencies
Execution order valid: true
Trace clarity: high
```

## Evaluation metrics

| Metric | Meaning |
|---|---|
| Goal clarity | Is the goal specific enough to decompose? |
| Subtask count | Number of generated subtasks |
| Required subtask coverage | Were necessary steps included? |
| Dependency validity | Are prerequisite relationships valid? |
| Execution order validity | Can subtasks be executed in order? |
| Trace clarity | Is the decomposition process inspectable? |

## Planned file structure

```text
projects/01_task_decomposition_agent/
├── README.md
├── src/
│   ├── task.py
│   ├── decomposer.py
│   └── evaluator.py
├── examples/
│   └── demo_goals.json
├── tests/
│   └── test_decomposition.py
└── results/
    └── decomposition_examples.md
```

## Minimum viable demo

The first demo should load a few structured goals and produce:

- subtasks
- dependencies
- execution order
- evaluation result
- trace

Run command target:

```bash
python projects/01_task_decomposition_agent/run_demo.py
```

Test command target:

```bash
python -m pytest projects/01_task_decomposition_agent/tests
```

## Current limitations

- No runnable implementation yet.
- No LLM integration yet.
- No open-ended goal parsing yet.
- No execution layer yet.
- No reflection or revision yet.

## Next steps

1. Add `src/task.py`.
2. Add `src/decomposer.py`.
3. Add `src/evaluator.py`.
4. Add demo goals.
5. Add runnable demo.
6. Add tests.
7. Add result examples.
8. Update this README to runnable prototype status.

## Completion target

This project reaches first milestone when it has:

- structured goal model
- deterministic decomposition
- dependency generation
- execution order generation
- evaluation
- trace output
- tests
- result artifact

At that point, Project 01 becomes the foundation layer for the planning-agent stack.
