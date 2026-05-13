# Planning Loop

This document defines the planning loop used across the Reasoning Planning Agents repository.

The planning loop is the operational core of the repo. It turns a vague goal into structured work, executes that work step by step, observes outcomes, reflects on failures, and revises the plan.

## Core loop

```text
Goal → Decompose → Plan → Execute → Observe → Reflect → Revise → Evaluate
```

The loop should produce explicit artifacts at every stage.

## Why planning loops matter

An agent that only generates a response is not enough.

A useful agent must manage progress across steps. It needs to know:

- what the goal is
- what subtasks are required
- what order they should happen in
- what has been completed
- what failed
- what should change next

Without a planning loop, agents become prompt responders with vague autonomy.

## Loop stages

| Stage | Question | Output |
|---|---|---|
| Goal | What are we trying to achieve? | Goal object |
| Decompose | What subtasks are required? | Subtask list |
| Plan | What order should subtasks follow? | Ordered plan |
| Execute | What happened when a step ran? | Step result |
| Observe | What state changed? | Observation |
| Reflect | What worked or failed? | Reflection note |
| Revise | What should change? | Revised plan |
| Evaluate | Did we make progress? | Evaluation result |

## Stage 1: Goal

A goal should be explicit enough to guide decomposition.

Weak goal:

```text
Make a blog post.
```

Better goal:

```text
Write and publish a 1000-word technical blog post explaining memory-backed agents to AI builders.
```

Minimal goal schema:

```text
goal_id
description
success_criteria
constraints
context
```

## Stage 2: Decomposition

Decomposition converts the goal into subtasks.

A subtask should have:

```text
subtask_id
description
expected_output
dependencies
status
```

Example:

```text
subtask_id: subtask_outline
description: Create a clear article outline.
expected_output: article_outline
dependencies: []
status: pending
```

## Stage 3: Planning

Planning orders subtasks into an executable sequence.

The planner should identify:

- dependencies
- risks
- blockers
- possible parallel work
- success criteria

Minimal plan schema:

```text
plan_id
goal_id
steps
dependencies
assumptions
risks
status
```

## Stage 4: Execution

Execution performs or simulates one plan step.

In early prototypes, execution can be deterministic.

Example:

```text
step_id: step_001
input: goal description
operation: create_outline
status: success
output: outline_created
```

Execution should produce a clear result, not just a vague message.

## Stage 5: Observation

Observation records what happened after execution.

Minimal observation schema:

```text
observation_id
step_id
status
output
error
notes
```

Observation is the evidence used by reflection.

## Stage 6: Reflection

Reflection analyzes the observation.

It should identify:

- what worked
- what failed
- likely cause
- whether the plan should continue
- what revision is needed

A useful reflection is specific.

Weak reflection:

```text
The plan failed. Try again.
```

Better reflection:

```text
The drafting step failed because no target audience was defined. Add an audience-definition step before drafting.
```

## Stage 7: Revision

Revision modifies the plan.

Revision types:

| Revision | Meaning |
|---|---|
| Add step | Add missing prerequisite |
| Remove step | Remove unnecessary action |
| Reorder step | Fix dependency order |
| Replace step | Change strategy |
| Mark blocked | Stop until missing information is available |

Revision should create a new plan version.

Example:

```text
plan_v1 → reflection → plan_v2
```

## Stage 8: Evaluation

Evaluation checks the loop outcome.

Useful evaluation questions:

- Was the goal completed?
- Were the subtasks useful?
- Were dependencies correct?
- Did execution produce expected outputs?
- Did reflection identify real causes?
- Did revision improve the plan?
- Is the trace inspectable?

## Trace requirements

Every planning loop should produce a trace.

Minimum trace:

```text
goal received
subtasks generated
plan created
steps executed
observations recorded
reflections generated
revisions applied
evaluation completed
```

The trace is the debugging surface of the agent.

## First prototype loop

Project 01 should implement the smallest useful loop:

```text
Goal → Subtasks → Dependencies → Execution Order → Trace
```

No LLM required.

The first prototype can use deterministic templates and structured examples.

## Second prototype loop

Project 02 should extend the loop:

```text
Goal → Subtasks → Plan → Execute Steps → Step Results → Final Trace
```

This introduces execution and state updates.

## Third prototype loop

Project 03 should add reflection:

```text
Failed Step → Observation → Reflection → Revised Plan
```

This tests whether the agent can improve after failure.

## Fourth prototype loop

Project 04 should add multiple roles:

```text
Goal → Decomposer Agent → Planner Agent → Executor Agent → Critic Agent → Coordinator Trace
```

Multi-agent planning should only be added after the single-agent loop is clear.

## Anti-patterns

Avoid these:

| Anti-pattern | Problem |
|---|---|
| Vague subtasks | Cannot execute or evaluate |
| No dependency tracking | Plans fail silently |
| Generic reflection | Does not improve behavior |
| Hidden state | Cannot debug agent decisions |
| Framework-first design | Creates complexity before understanding |
| Multi-agent theater | Adds agents without better results |

## Design rule

The planning loop should be:

```text
small enough to test, explicit enough to debug, structured enough to extend
```

That is the standard for this repository.
