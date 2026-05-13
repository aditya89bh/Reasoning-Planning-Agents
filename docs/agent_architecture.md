# Agent Architecture

This document defines the core architecture for the Reasoning Planning Agents repository.

The repository treats agents as structured reasoning systems. The goal is not to build chatbots with extra tools. The goal is to build agents that can decompose goals, plan actions, execute steps, observe outcomes, reflect on failures, and revise strategy.

## Core loop

The basic agent loop is:

```text
Goal → Task Decomposition → Planning → Execution → Observation → Reflection → Revision → Evaluation
```

Each layer should produce explicit artifacts that can be inspected and tested.

## Why explicit architecture matters

Many agent systems fail because the internal process is hidden.

Common failure modes:

- the goal is vague
- subtasks are poorly defined
- dependencies are missing
- execution steps are unordered
- failures are ignored
- reflection is generic
- revision does not change behavior
- traces are too vague to debug

This repository focuses on making each part visible.

## Architecture layers

| Layer | Input | Output | Role |
|---|---|---|---|
| Goal | User objective | Goal object | Defines desired outcome |
| Decomposition | Goal object | Subtasks | Breaks goal into smaller work units |
| Planning | Subtasks | Ordered plan | Creates executable sequence with dependencies |
| Execution | Plan step | Step result | Performs or simulates work |
| Observation | Step result | Observation | Records outcome, error, or state change |
| Reflection | Observations | Reflection note | Explains what worked or failed |
| Revision | Reflection note | Revised plan | Changes plan or strategy |
| Evaluation | Trace | Score/report | Measures quality and completion |

## Goal

A goal should describe what the agent is trying to accomplish.

Minimal fields:

```text
goal_id
description
success_criteria
constraints
context
```

Example:

```text
goal_id: goal_launch_blog
description: Publish a technical blog post about memory-backed agents.
success_criteria:
  - outline created
  - draft written
  - reviewed
  - published
constraints:
  - under 1200 words
  - technical but readable
```

## Task decomposition

Task decomposition breaks a goal into smaller subtasks.

A useful subtask should be:

- specific
- necessary
- testable
- ordered or dependency-aware
- small enough to execute

Example subtasks:

```text
research topic
create outline
write draft
review clarity
publish article
```

## Planning

Planning turns subtasks into an ordered sequence.

A plan should define:

```text
plan_id
goal_id
steps
dependencies
assumptions
risks
success_criteria
```

Planning is not just listing tasks. It should explain what must happen first, what can happen in parallel, and what can fail.

## Execution

Execution performs or simulates a plan step.

In early prototypes, execution can be deterministic and simulated.

Example:

```text
step_id: step_create_outline
status: success
output: outline_created
```

Later versions can connect to tools, APIs, code execution, or robotics workflows.

## Observation

Observation records what happened during execution.

Minimal fields:

```text
observation_id
step_id
status
output
error
notes
```

Observation is important because reflection should be grounded in actual outcomes, not generic reasoning.

## Reflection

Reflection analyzes the gap between expected and actual outcomes.

A reflection should answer:

- What happened?
- What failed?
- Why did it fail?
- What should change?
- Should the plan continue, revise, or stop?

Bad reflection:

```text
The task failed. Try again.
```

Better reflection:

```text
The outline step failed because the goal had no defined audience. Add an audience clarification step before drafting.
```

## Revision

Revision changes the plan or strategy based on reflection.

Revision types:

| Type | Meaning |
|---|---|
| Add step | Insert missing prerequisite |
| Remove step | Delete unnecessary action |
| Reorder step | Fix dependency issue |
| Replace step | Change strategy |
| Stop plan | Mark goal as blocked |

## Evaluation

Evaluation measures whether the agent loop worked.

Useful metrics:

| Metric | Meaning |
|---|---|
| Goal completion | Was the goal achieved? |
| Decomposition quality | Were subtasks useful and complete? |
| Plan validity | Were dependencies correct? |
| Execution success | Did steps complete? |
| Reflection quality | Did reflection identify real causes? |
| Revision usefulness | Did changes improve the plan? |
| Trace clarity | Can a human inspect the loop? |

## Trace-first design

Every agent run should produce a trace.

A trace should show:

```text
goal
subtasks
plan
executed steps
observations
reflections
revisions
evaluation
```

Without traces, agent failures become guesswork.

## Single-agent architecture

The first runnable prototypes should use a single-agent loop:

```text
Goal → Decomposer → Planner → Executor → Observer → Reflector → Evaluator
```

This is easier to inspect and test than multi-agent orchestration.

## Multi-agent architecture

Multi-agent planning should come later.

A multi-agent system should only be introduced when roles are clearly separable.

Possible roles:

| Agent | Role |
|---|---|
| Decomposer | Breaks goal into subtasks |
| Planner | Creates ordered plan |
| Executor | Executes steps |
| Critic | Finds flaws |
| Reflector | Revises strategy |
| Coordinator | Resolves conflicts and manages shared state |

The risk is fake collaboration: multiple agents talking without improving the outcome.

## Design principle

Start deterministic.

Do not begin with LLM tool orchestration, frameworks, or multi-agent swarms.

Build the loop first:

```text
input → structured artifacts → trace → evaluation
```

Then add language models or tool use once the architecture is inspectable.

## Integration target

The long-term integrated loop should look like this:

```text
Goal
→ Decomposition
→ Plan
→ Execution
→ Observation
→ Reflection
→ Revision
→ Final evaluation
```

The repository should grow from working loops, not agent theater.
