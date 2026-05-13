# Integrated Demo

This folder connects the four runnable prototypes into one end-to-end reasoning and planning loop.

The goal is to show how a high-level goal can move through decomposition, planning/execution, failure reflection, revision, and multi-agent coordination.

## Integrated loop

```text
Goal
→ Task Decomposition
→ Planner-Executor
→ Failure Observation
→ Reflection + Revision
→ Multi-Agent Coordination
→ Final Trace
```

## What this demo should prove

The integrated demo should prove that the repository is not just four disconnected prototypes.

It should show:

1. A goal can be decomposed into subtasks.
2. A structured plan can be executed step by step.
3. A failure can be surfaced as an observation.
4. The failure can produce a specific reflection.
5. The reflection can produce a revision proposal.
6. The revision signal can be used by a coordinator/critic layer.
7. The full chain can produce an inspectable trace.

## Target scenario

Use a publishing workflow because all four modules currently support that domain.

Input goal:

```text
Publish a technical blog post about planning agents for AI builders.
```

Expected path:

```text
Project 01 decomposes the goal.
Project 02 executes a publishing plan with one forced failure.
Project 03 reflects on that failure and proposes a revision.
Project 04 coordinates role contributions into a final shared plan.
```

## Planned files

```text
integrated_demo/
├── README.md
├── run_integrated_demo.py
└── results/
    └── integrated_trace.md
```

## Planned run command

From the repository root:

```bash
python integrated_demo/run_integrated_demo.py
```

## Current status

```text
Scaffold added
```

The next step is to implement `run_integrated_demo.py`.
