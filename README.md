# Reasoning Planning Agents

Structured reasoning and planning agents for goal decomposition, plan execution, reflection, and multi-agent coordination.

## What this repository is

This repository is a structured research and implementation scaffold for reasoning and planning agents.

The goal is to move beyond chat-style agents that only respond to prompts. A useful reasoning agent should be able to:

- understand a goal
- decompose it into subtasks
- identify dependencies
- create an executable plan
- track step results
- reflect on failures
- revise strategy
- produce an inspectable trace

This repository treats agents as reasoning systems, not just wrappers around language models.

## Core thesis

Reasoning agents should not only generate answers.

They should transform goals into plans, execute those plans through explicit steps, evaluate progress, and revise behavior when the plan fails.

The working assumption is:

```text
A useful agent is a loop: goal → plan → action → observation → reflection → revision.
```

## Why this matters

Most agent demos look impressive but fail under real task pressure because their internal process is vague.

Common failure modes:

- unclear task decomposition
- brittle planning
- no dependency tracking
- hidden reasoning steps
- weak failure recovery
- no trace of why decisions were made
- multi-agent chaos disguised as collaboration

This repository explores agent architectures that are structured, traceable, and testable.

## Agent stack

The intended stack is:

```text
Goal → Task Decomposition → Planning → Execution → Observation → Reflection → Revision → Evaluation
```

| Layer | Role |
|---|---|
| Goal | Defines the desired outcome |
| Task Decomposition | Breaks the goal into subtasks |
| Planning | Orders subtasks and dependencies |
| Execution | Performs or simulates each step |
| Observation | Records step result or failure |
| Reflection | Reviews what worked and failed |
| Revision | Updates the plan or strategy |
| Evaluation | Measures correctness, progress, and trace quality |

## Project map

| Project | Goal | Status | Output |
|---|---|---:|---|
| 01 Task Decomposition Agent | Break goals into structured subtasks | Planned | Decomposition prototype |
| 02 Planner-Executor Agent | Convert subtasks into ordered execution loops | Planned | Runnable planner-executor loop |
| 03 Reflection Agent | Analyze failures and revise plans | Planned | Reflection trace prototype |
| 04 Multi-Agent Planning | Coordinate specialized agents around shared goals | Planned | Multi-agent planning scaffold |

## Current status

This repository is in the foundation phase.

Current priority:

```text
Build a clean scaffold first, then implement Project 01 as the first runnable prototype.
```

Estimated repository status:

```text
10-15% complete
```

## Repository structure

Target structure:

```text
Reasoning-Planning-Agents/
├── README.md
├── docs/
│   ├── agent_architecture.md
│   ├── planning_loop.md
│   ├── evaluation.md
│   └── roadmap.md
├── projects/
│   ├── 01_task_decomposition_agent/
│   ├── 02_planner_executor_agent/
│   ├── 03_reflection_agent/
│   └── 04_multi_agent_planning/
├── shared/
│   ├── interfaces.md
│   └── trace_schema.md
├── references/
│   └── reading_list.md
└── integrated_demo/
    └── README.md
```

## First milestone

The first milestone is Project 01: Task Decomposition Agent.

Minimum useful loop:

```text
Goal → Subtasks → Dependencies → Execution Order → Trace → Evaluation
```

The first prototype should be deterministic and inspectable before adding LLMs or external agent frameworks.

## Evaluation criteria

Each project should be evaluated on:

| Metric | Meaning |
|---|---|
| Decomposition quality | Are subtasks clear and useful? |
| Dependency correctness | Are prerequisite relationships valid? |
| Execution order | Can the plan be followed? |
| Traceability | Can a human inspect the reasoning path? |
| Failure recovery | Can the system revise after failure? |
| Modularity | Can components be tested independently? |

## Related direction

This repository connects to broader work on:

- planning agents
- reasoning loops
- task decomposition
- reflection agents
- multi-agent coordination
- agent evaluation
- embodied and robotics agents

## Roadmap

Near-term roadmap:

1. Add foundation docs.
2. Add project-level README files.
3. Implement Project 01 runnable prototype.
4. Add tests and result examples.
5. Implement Project 02 planner-executor loop.
6. Add reflection and revision behavior.
7. Build an integrated demo across decomposition, planning, execution, and reflection.
