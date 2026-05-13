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
- coordinate specialized roles
- produce an inspectable trace

This repository treats agents as reasoning systems, not just wrappers around language models.

## Core thesis

Reasoning agents should not only generate answers.

They should transform goals into plans, execute those plans through explicit steps, evaluate progress, revise behavior when the plan fails, and coordinate specialized roles when planning becomes complex.

The working assumption is:

```text
A useful agent is a loop: goal → plan → action → observation → reflection → revision → coordination.
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
Goal → Task Decomposition → Planning → Execution → Observation → Reflection → Revision → Coordination → Evaluation
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
| Coordination | Merges specialized role outputs into a shared plan |
| Evaluation | Measures correctness, progress, and trace quality |

## Project map

| Project | Goal | Status | Output |
|---|---|---:|---|
| 01 Task Decomposition Agent | Break goals into structured subtasks | Runnable first prototype | Demo, tests, result examples |
| 02 Planner-Executor Agent | Convert structured plans into executed step results | Runnable first prototype | Demo, tests, execution examples |
| 03 Reflection Agent | Analyze failures and propose plan revisions | Runnable first prototype | Demo, tests, reflection examples |
| 04 Multi-Agent Planning | Coordinate specialized agents around shared goals | Runnable first prototype | Demo, tests, coordination examples |

## Current status

This repository has moved from foundation-only scaffold to four runnable prototypes.

Current state:

1. Top-level README is documented.
2. Agent architecture is documented.
3. Planning loop is documented.
4. Evaluation framework is documented.
5. Roadmap is documented.
6. Shared interfaces and trace schema are documented.
7. Project READMEs are added for all four modules.
8. Project 01 has a runnable task decomposition prototype.
9. Project 02 has a runnable planner-executor prototype.
10. Project 03 has a runnable reflection prototype.
11. Project 04 has a runnable multi-agent planning prototype.

Estimated repository status:

```text
85-90% complete
```

This is not yet a production planning-agent system. It is now a structured repo with four runnable modules and a clear path toward integration.

## Repository structure

Current structure:

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
│   │   ├── README.md
│   │   ├── run_demo.py
│   │   ├── src/
│   │   ├── examples/
│   │   ├── tests/
│   │   └── results/
│   ├── 02_planner_executor_agent/
│   │   ├── README.md
│   │   ├── run_demo.py
│   │   ├── src/
│   │   ├── examples/
│   │   ├── tests/
│   │   └── results/
│   ├── 03_reflection_agent/
│   │   ├── README.md
│   │   ├── run_demo.py
│   │   ├── src/
│   │   ├── examples/
│   │   ├── tests/
│   │   └── results/
│   └── 04_multi_agent_planning/
│       ├── README.md
│       ├── run_demo.py
│       ├── src/
│       ├── examples/
│       ├── tests/
│       └── results/
├── shared/
│   ├── interfaces.md
│   └── trace_schema.md
└── references/
    └── reading_list.md
```

## Runnable prototypes

## Project 01: Task Decomposition Agent

Run from the repository root:

```bash
python projects/01_task_decomposition_agent/run_demo.py
```

Run tests:

```bash
python -m pytest projects/01_task_decomposition_agent/tests
```

What it demonstrates:

```text
Goal → Subtasks → Dependencies → Execution Order → Trace → Evaluation
```

## Project 02: Planner-Executor Agent

Run from the repository root:

```bash
python projects/02_planner_executor_agent/run_demo.py
```

Run tests:

```bash
python -m pytest projects/02_planner_executor_agent/tests
```

What it demonstrates:

```text
Plan Spec → Plan Object → Execute Steps → Step Results → Final Status → Evaluation → Trace
```

## Project 03: Reflection Agent

Run from the repository root:

```bash
python projects/03_reflection_agent/run_demo.py
```

Run tests:

```bash
python -m pytest projects/03_reflection_agent/tests
```

What it demonstrates:

```text
Observation → Failure Analysis → Reflection → Revision → Evaluation → Trace
```

## Project 04: Multi-Agent Planning

Run from the repository root:

```bash
python projects/04_multi_agent_planning/run_demo.py
```

Run tests:

```bash
python -m pytest projects/04_multi_agent_planning/tests
```

What it demonstrates:

```text
Goal → Roles → Agent Contributions → Conflict Detection → Shared Plan → Evaluation → Trace
```

## How to use this repository

Start with:

1. `docs/agent_architecture.md`
2. `docs/planning_loop.md`
3. `docs/evaluation.md`
4. `shared/interfaces.md`
5. `shared/trace_schema.md`
6. `projects/01_task_decomposition_agent/README.md`
7. `projects/02_planner_executor_agent/README.md`
8. `projects/03_reflection_agent/README.md`
9. `projects/04_multi_agent_planning/README.md`

Then run all four project demos.

## Evaluation criteria

Each project should be evaluated on:

| Metric | Meaning |
|---|---|
| Decomposition quality | Are subtasks clear and useful? |
| Dependency correctness | Are prerequisite relationships valid? |
| Execution order | Can the plan be followed? |
| Traceability | Can a human inspect the reasoning path? |
| Failure recovery | Can the system revise after failure? |
| Coordination quality | Can multiple role outputs become one shared plan? |
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

1. Run all four project demos locally and capture actual output.
2. Add a unified test command and dependency file.
3. Connect Project 01 decomposition output to Project 02 execution input.
4. Connect Project 02 failure outputs to Project 03 reflection input.
5. Connect Project 03 revision outputs to Project 04 critic/coordinator roles.
6. Build an integrated demo across decomposition, planning, execution, reflection, and multi-agent coordination.
