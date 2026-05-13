# Project 04: Multi-Agent Planning

This project explores how multiple specialized agents can coordinate around a shared goal without becoming noisy or chaotic.

The goal is to define roles, inspect role contributions, detect conflicts, create a shared plan, and produce a coordination trace.

## Core question

```text
Can multiple agents coordinate around a goal while preserving role clarity, plan consistency, and traceability?
```

## Current status

```text
Runnable first prototype
```

This project now includes:

- agent role data model
- agent contribution data model
- coordination conflict data model
- shared plan data model
- deterministic conflict detector
- deterministic coordinator
- multi-agent planning evaluator
- demo roles and contributions
- command-line demo
- tests
- coordination result examples

Estimated project status:

```text
65-70% complete
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

## Target loop

```text
Goal → Roles → Agent Contributions → Conflict Detection → Shared Plan → Evaluation → Trace
```

## Components

| File | Role |
|---|---|
| `src/agent_role.py` | Defines `AgentRole`, `AgentContribution`, `CoordinationConflict`, `SharedPlan`, and `MultiAgentPlanningResult` |
| `src/conflict_detector.py` | Detects missing required steps, duplicate steps, and role-overlap issues |
| `src/coordinator.py` | Merges role contributions into a deterministic shared plan |
| `src/evaluator.py` | Evaluates role clarity, conflict resolution, shared-plan validity, and trace clarity |
| `examples/demo_roles.json` | Provides deterministic roles and agent contributions |
| `run_demo.py` | Runs the multi-agent planning demo from the command line |
| `tests/test_multi_agent_planning.py` | Regression tests for multi-agent planning behavior |
| `results/coordination_examples.md` | Documents expected coordination behavior |

## Recommended roles

The current prototype uses four roles:

| Role | Responsibility |
|---|---|
| Decomposer | Breaks the goal into subtasks |
| Planner | Orders subtasks into an executable plan |
| Critic | Detects missing steps, conflicts, or weak dependencies |
| Coordinator | Merges outputs into a shared plan |

## Agent role schema

A minimal role includes:

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
responsibility: Break the goal into clear subtasks.
inputs:
  - goal
outputs:
  - subtasks
constraints:
  - keep subtasks specific
```

## Agent contribution schema

Each role can produce a local contribution.

```text
contribution_id
role_id
goal_id
proposed_steps
assumptions
risks
confidence
```

Example:

```text
contribution_id: contrib_planner_publish_blog
role_id: role_planner
goal_id: goal_publish_blog
proposed_steps:
  - define_audience
  - create_outline
  - write_draft
  - publish_article
risks:
  - publishing may happen before review
confidence: 0.78
```

## Conflict schema

A conflict captures disagreement or inconsistency between role outputs.

```text
conflict_id
conflict_type
source_roles
description
recommended_resolution
status
```

Current conflict types:

```text
duplicate_step
missing_required_step
role_overlap
```

Example:

```text
conflict_id: conflict_duplicate_define_audience
conflict_type: duplicate_step
source_roles:
  - role_decomposer
  - role_planner
description: Step was proposed by multiple roles: define_audience
recommended_resolution: deduplicate_step:define_audience
status: open
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
shared_plan_id: shared_plan_goal_publish_blog
steps:
  - define_audience
  - create_outline
  - write_draft
  - review_clarity
  - publish_article
resolved_conflicts:
  - conflict_duplicate_define_audience
open_conflicts: []
status: valid
```

## Demo scenario

The demo coordinates roles around:

```text
goal_publish_blog
```

Required shared-plan steps:

```text
define_audience
create_outline
write_draft
review_clarity
publish_article
```

Expected shared plan:

```text
1. define_audience
2. create_outline
3. write_draft
4. review_clarity
5. publish_article
```

Expected status:

```text
valid
```

## Trace behavior

The trace shows:

```text
Goal received
Roles assigned
Agent contributions received
Conflicts detected
Conflict resolution proposed
Shared plan created
Shared plan status
Coordination completed
```

Example trace:

```text
Goal received: goal_publish_blog
Roles assigned: Decomposer, Planner, Critic, Coordinator
Agent contributions received: 4
Conflicts detected: 4
Conflict detected: duplicate_step -> Step was proposed by multiple roles: define_audience
Conflict resolution proposed: deduplicate_step:define_audience
Shared plan created: shared_plan_goal_publish_blog
Shared plan status: valid
Coordination completed
```

## Evaluation metrics

| Metric | Meaning |
|---|---|
| Role clarity | Are roles distinct and responsible for different outputs? |
| Contribution count | Did agents produce inspectable contributions? |
| Conflict count | Were coordination issues surfaced? |
| Open conflict count | Did unresolved conflicts remain? |
| Shared plan validity | Does the final plan have steps, valid roles, and correct status? |
| Trace clarity | Can a human inspect coordination decisions? |

## Run the demo

From the repository root:

```bash
python projects/04_multi_agent_planning/run_demo.py
```

The demo prints:

- goal id
- roles
- contributions
- detected conflicts
- shared plan
- evaluation result
- trace
- summary

## Run tests

From the repository root:

```bash
python -m pytest projects/04_multi_agent_planning/tests
```

## What this prototype proves

This project proves the fourth layer of the planning-agent stack:

```text
role outputs → conflict detection → deterministic coordination → shared plan → trace
```

That is the coordination layer needed before building a full integrated agent loop.

## Current limitations

- Agent roles are deterministic, not live LLM agents.
- Contributions are loaded from JSON.
- Conflict resolution is simple and rule-based.
- Duplicate conflicts are treated as resolved automatically.
- No actual agent conversation yet.
- No direct integration with Projects 01-03 yet.

## Next steps

1. Run the demo locally and capture actual output.
2. Build an integrated demo across Projects 01-04.
3. Connect Project 03 revision outputs to Project 04 critic/coordinator roles.
4. Add richer conflict types.
5. Add unresolved-conflict cases.
6. Update top-level README with Project 04 runnable status.

## Completion target

This project reaches a stronger milestone when it has:

- local demo output captured in results
- direct integration with Projects 01-03
- richer conflict detection
- unresolved-conflict examples
- integrated demo participation

At that point, Project 04 becomes a stronger coordination layer for the planning-agent stack.
