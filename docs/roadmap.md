# Roadmap

This document defines the staged roadmap for the Reasoning Planning Agents repository.

The repo should grow from simple, deterministic prototypes into more capable reasoning and planning agents. The goal is to avoid jumping into complex multi-agent systems before the core loop is inspectable and testable.

## Current status

```text
Foundation phase
```

The repository currently needs structure, shared interfaces, project-level specifications, and the first runnable prototype.

Estimated status:

```text
15-20% complete after foundation docs
```

## Build principle

Build in this order:

```text
clarity → structure → prototype → tests → traces → integration
```

Do not start with agent frameworks. Start with deterministic loops that can be inspected.

## Phase 1: Foundation scaffold

Goal: make the repository understandable and credible.

Files:

```text
README.md
docs/agent_architecture.md
docs/planning_loop.md
docs/evaluation.md
docs/roadmap.md
shared/interfaces.md
shared/trace_schema.md
references/reading_list.md
```

Completion criteria:

- repo thesis is clear
- project map is defined
- evaluation standard is defined
- shared interfaces are documented
- roadmap is explicit

Expected repo status after Phase 1:

```text
35-40% complete
```

## Phase 2: Project specifications

Goal: define four project modules before implementation.

Project README files:

```text
projects/01_task_decomposition_agent/README.md
projects/02_planner_executor_agent/README.md
projects/03_reflection_agent/README.md
projects/04_multi_agent_planning/README.md
```

Project focus:

| Project | Focus | Prototype target |
|---|---|---|
| 01 Task Decomposition Agent | Goal to subtasks | Goal → subtasks → dependencies → trace |
| 02 Planner-Executor Agent | Ordered execution | Plan → step results → final trace |
| 03 Reflection Agent | Failure recovery | Failure → reflection → revised plan |
| 04 Multi-Agent Planning | Role coordination | Goal → roles → shared plan → coordination trace |

Expected repo status after Phase 2:

```text
50-55% complete
```

## Phase 3: Project 01 runnable prototype

Goal: implement the first deterministic task decomposition agent.

Minimum loop:

```text
Goal → Subtasks → Dependencies → Execution Order → Trace → Evaluation
```

Files:

```text
projects/01_task_decomposition_agent/src/task.py
projects/01_task_decomposition_agent/src/decomposer.py
projects/01_task_decomposition_agent/src/evaluator.py
projects/01_task_decomposition_agent/examples/demo_goals.json
projects/01_task_decomposition_agent/run_demo.py
projects/01_task_decomposition_agent/tests/test_decomposition.py
projects/01_task_decomposition_agent/results/decomposition_examples.md
```

Completion criteria:

- structured goal input
- deterministic decomposition
- dependency output
- ordered plan output
- trace output
- basic tests
- result artifact

Expected repo status after Phase 3:

```text
65-70% complete
```

## Phase 4: Project 02 runnable prototype

Goal: implement a planner-executor loop.

Minimum loop:

```text
Goal → Plan → Execute Steps → Step Results → Final Trace
```

Files:

```text
projects/02_planner_executor_agent/src/plan.py
projects/02_planner_executor_agent/src/planner.py
projects/02_planner_executor_agent/src/executor.py
projects/02_planner_executor_agent/src/evaluator.py
projects/02_planner_executor_agent/examples/demo_plans.json
projects/02_planner_executor_agent/run_demo.py
projects/02_planner_executor_agent/tests/test_planner_executor.py
projects/02_planner_executor_agent/results/execution_examples.md
```

Completion criteria:

- ordered plan creation
- step execution simulation
- step result tracking
- failure visibility
- final trace
- tests and result examples

Expected repo status after Phase 4:

```text
75-80% complete
```

## Phase 5: Project 03 runnable prototype

Goal: implement reflection and revision.

Minimum loop:

```text
Failed Step → Observation → Reflection → Revised Plan → Evaluation
```

Files:

```text
projects/03_reflection_agent/src/reflection.py
projects/03_reflection_agent/src/failure_analyzer.py
projects/03_reflection_agent/src/reviser.py
projects/03_reflection_agent/src/evaluator.py
projects/03_reflection_agent/examples/failure_cases.json
projects/03_reflection_agent/run_demo.py
projects/03_reflection_agent/tests/test_reflection.py
projects/03_reflection_agent/results/reflection_examples.md
```

Completion criteria:

- failure case input
- cause analysis
- actionable reflection
- revised plan output
- trace output
- tests and result examples

Expected repo status after Phase 5:

```text
85% complete
```

## Phase 6: Project 04 runnable prototype

Goal: implement a small multi-agent planning scaffold.

Minimum loop:

```text
Goal → Role Assignment → Agent Plans → Coordination → Shared Plan → Trace
```

Files:

```text
projects/04_multi_agent_planning/src/agent_role.py
projects/04_multi_agent_planning/src/coordinator.py
projects/04_multi_agent_planning/src/conflict_detector.py
projects/04_multi_agent_planning/src/shared_plan.py
projects/04_multi_agent_planning/examples/demo_roles.json
projects/04_multi_agent_planning/run_demo.py
projects/04_multi_agent_planning/tests/test_multi_agent_planning.py
projects/04_multi_agent_planning/results/coordination_examples.md
```

Completion criteria:

- role definitions
- role assignment
- basic conflict detection
- shared plan output
- coordination trace
- tests and result examples

Expected repo status after Phase 6:

```text
90% complete
```

## Phase 7: Integrated demo

Goal: connect the four prototypes.

Integrated loop:

```text
Goal → Decomposition → Planning → Execution → Failure → Reflection → Revision → Multi-Agent Coordination → Evaluation
```

Files:

```text
integrated_demo/README.md
integrated_demo/run_integrated_demo.py
integrated_demo/results/integrated_trace.md
```

Completion criteria:

- all project outputs connect through shared interfaces
- integrated trace exists
- local output is captured
- tests cover scaffold or execution path

Expected repo status after Phase 7:

```text
90-95% complete as a portfolio-grade scaffold
```

## What makes this repo credible

The repo becomes credible when it has:

- clear thesis
- explicit architecture
- four runnable prototypes
- result artifacts
- tests
- traces
- integrated demo
- honest limitations

## What this repo should avoid

Avoid:

- calling a README-only repo complete
- adding many agents before one agent loop works
- vague claims about autonomy
- framework-first implementation
- hidden reasoning steps
- generic reflection
- no tests
- no result outputs

## Near-term next steps

Immediate next steps:

1. Finish foundation docs.
2. Add shared interfaces and trace schema.
3. Add project READMEs.
4. Build Project 01 runnable prototype.
5. Update README with real status.

## Long-term direction

Long-term, this repository can evolve into a general architecture for planning agents that can later connect to:

- LLM planners
- tool-using agents
- robotics workflows
- business automation agents
- multi-agent orchestration systems
- memory-backed reasoning systems

The immediate goal is not maximum complexity. The immediate goal is a clean, inspectable, tested planning-agent stack.
