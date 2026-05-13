# Project 04: Multi-Agent Planning

This project explores how multiple specialized agents can coordinate around a shared goal without becoming noisy or chaotic.

The goal is to define roles, assign responsibilities, detect conflicts, create a shared plan, and produce a coordination trace.

## Core question

```text
Can multiple agents coordinate around a goal while preserving role clarity, plan consistency, and traceability?
```

## Why this matters

Multi-agent systems are easy to demo and hard to trust.

Adding more agents does not automatically improve reasoning. It often creates:

- duplicated work
- conflicting plans
- unclear responsibility
- circular discussion
- hidden assumptions
- weak coordination
- fake collaboration

A useful multi-agent planning system needs explicit roles, shared state, conflict detection, and a final coordinated plan.

## Current status

```text
Design phase
```

This project does not yet have the runnable implementation. The immediate goal is to define role schema, coordination logic, conflict detection, shared plan output, tests, and result examples.

## Target loop

```text
Goal → Role Assignment → Agent Plans → Conflict Detection → Shared Plan → Coordination Trace → Evaluation
```

## Components

| Component | Role |
|---|---|
| AgentRole model | Defines each agent's responsibility |
| Role assigner | Maps goal requirements to agent roles |
| Agent plan model | Stores each agent's proposed plan |
| Conflict detector | Finds contradictions or duplicate work |
| Coordinator | Merges agent plans into one shared plan |
| SharedPlan model | Represents the final coordinated plan |
| Evaluator | Checks role clarity, conflicts, and plan validity |
| Trace generator | Shows role assignment, conflicts, and coordination decisions |

## Agent role schema

A minimal role should include:

```text
role_id
name
responsibility
inputs
outputs
constraints
```

Example:

```text
role_id: role_decomposer
name: Decomposer
responsibility: Break the goal into subtasks.
inputs:
  - goal
outputs:
  - subtasks
constraints:
  - keep subtasks specific and testable
```

## Recommended roles

The first prototype should use four roles:

| Role | Responsibility |
|---|---|
| Decomposer | Breaks the goal into subtasks |
| Planner | Orders subtasks into an executable plan |
| Critic | Detects missing steps, conflicts, or weak dependencies |
| Coordinator | Merges outputs into a shared plan |

## Agent plan schema

Each agent can produce a local plan or contribution.

```text
agent_plan_id
role_id
goal_id
proposed_steps
assumptions
risks
confidence
```

Example:

```text
agent_plan_id: planner_plan_001
role_id: role_planner
goal_id: goal_publish_blog
proposed_steps:
  - define audience
  - create outline
  - write draft
  - review
  - publish
assumptions:
  - goal is article publishing
risks:
  - audience may be undefined
confidence: 0.85
```

## Conflict schema

A conflict captures disagreement or inconsistency between agent outputs.

```text
conflict_id
conflict_type
source_roles
description
recommended_resolution
status
```

Conflict types:

```text
duplicate_step
missing_dependency
contradictory_order
missing_required_step
role_overlap
unresolved_assumption
```

Example:

```text
conflict_id: conflict_review_missing
conflict_type: missing_required_step
source_roles:
  - role_critic
description: Planner skipped review before publish.
recommended_resolution: Insert review step before publish.
status: resolved
```

## Shared plan schema

The coordinator outputs a shared plan.

```text
shared_plan_id
goal_id
roles_used
steps
resolved_conflicts
open_conflicts
status
```

Example:

```text
shared_plan_id: shared_plan_publish_blog
roles_used:
  - decomposer
  - planner
  - critic
  - coordinator
steps:
  - define audience
  - create outline
  - write draft
  - review clarity
  - publish article
resolved_conflicts:
  - conflict_review_missing
open_conflicts: []
status: valid
```

## Coordination behavior

The first prototype should be deterministic.

Expected behavior:

1. Load a goal.
2. Assign roles.
3. Generate role-specific outputs.
4. Detect conflicts.
5. Apply coordinator decisions.
6. Produce shared plan.
7. Evaluate role clarity and plan validity.
8. Print trace.

## Trace behavior

The trace should show:

```text
Goal received
Roles assigned
Agent plans generated
Conflicts detected
Conflicts resolved
Shared plan created
Evaluation completed
```

Example trace:

```text
Goal received: publish technical blog post
Roles assigned: decomposer, planner, critic, coordinator
Planner proposed 4 steps
Critic detected missing review step
Coordinator inserted review before publish
Shared plan status: valid
```

## Evaluation metrics

| Metric | Meaning |
|---|---|
| Role clarity | Does each agent have a distinct responsibility? |
| Plan contribution quality | Are role outputs useful? |
| Conflict detection | Were conflicts surfaced? |
| Conflict resolution | Were conflicts handled correctly? |
| Shared plan validity | Is the final plan executable? |
| Trace clarity | Can a human inspect coordination decisions? |

## Planned file structure

```text
projects/04_multi_agent_planning/
├── README.md
├── src/
│   ├── agent_role.py
│   ├── coordinator.py
│   ├── conflict_detector.py
│   └── shared_plan.py
├── examples/
│   └── demo_roles.json
├── tests/
│   └── test_multi_agent_planning.py
└── results/
    └── coordination_examples.md
```

## Minimum viable demo

The first demo should load a goal and predefined agent roles, then produce:

- role assignments
- agent contributions
- detected conflicts
- resolved conflicts
- shared plan
- evaluation result
- trace

Run command target:

```bash
python projects/04_multi_agent_planning/run_demo.py
```

Test command target:

```bash
python -m pytest projects/04_multi_agent_planning/tests
```

## Current limitations

- No runnable implementation yet.
- No LLM agent roles yet.
- No real agent communication yet.
- No dynamic role assignment yet.
- No tool execution yet.
- No integration with Projects 01-03 yet.

## Next steps

1. Add `src/agent_role.py`.
2. Add `src/shared_plan.py`.
3. Add `src/conflict_detector.py`.
4. Add `src/coordinator.py`.
5. Add demo roles.
6. Add runnable demo.
7. Add tests.
8. Add result examples.
9. Update this README to runnable prototype status.

## Completion target

This project reaches first milestone when it has:

- role schema
- deterministic role assignment
- local agent plan outputs
- conflict detection
- conflict resolution
- shared plan output
- trace output
- tests
- result artifact

At that point, Project 04 becomes the coordination layer of the planning-agent stack.
