# Coordination Examples

This document summarizes the expected behavior of the Multi-Agent Planning prototype.

The prototype demonstrates a minimal coordination loop:

```text
Goal → Roles → Agent Contributions → Conflict Detection → Shared Plan → Evaluation → Trace
```

The goal is not open-ended multi-agent autonomy yet. The goal is to make role coordination explicit, deterministic, inspectable, and testable.

## Demo scenario

The demo uses `examples/demo_roles.json`.

Goal:

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

## Roles

The demo uses four roles:

| Role | Responsibility |
|---|---|
| `role_decomposer` | Break the goal into clear subtasks |
| `role_planner` | Order subtasks into an executable plan |
| `role_critic` | Detect missing steps, weak dependencies, and plan risks |
| `role_coordinator` | Merge agent contributions into one shared plan |

## Agent contributions

Expected contribution shape:

```text
role_decomposer → define_audience, create_outline, write_draft, publish_article
role_planner → define_audience, create_outline, write_draft, publish_article
role_critic → review_clarity
role_coordinator → no local steps, merges contributions
```

The decomposer and planner both propose some overlapping steps. The critic contributes the missing review step.

## Expected conflicts

The conflict detector should identify duplicate steps when multiple roles propose the same step.

Expected duplicate conflicts include:

```text
conflict_duplicate_define_audience
conflict_duplicate_create_outline
conflict_duplicate_write_draft
conflict_duplicate_publish_article
```

Each duplicate conflict should recommend:

```text
deduplicate_step:<step_name>
```

If a required step is missing from all contributions, the conflict detector should create:

```text
conflict_missing_<step_name>
```

with recommended resolution:

```text
insert_step:<step_name>
```

In the current demo, `review_clarity` is supplied by the critic, so it should appear in the final shared plan.

## Expected shared plan

The coordinator should merge all contributions into the required order:

```text
1. define_audience
2. create_outline
3. write_draft
4. review_clarity
5. publish_article
```

Expected shared plan status:

```text
valid
```

Expected open conflicts:

```text
[]
```

Expected resolved conflicts:

```text
all detected conflicts are listed as resolved_conflicts
```

## Expected trace shape

The coordination trace should look like:

```text
Goal received: goal_publish_blog
Roles assigned: Decomposer, Planner, Critic, Coordinator
Agent contributions received: 4
Conflicts detected: <n>
Conflict detected: duplicate_step -> <description>
Conflict resolution proposed: deduplicate_step:<step_name>
Shared plan created: shared_plan_goal_publish_blog
Shared plan steps: define_audience, create_outline, write_draft, review_clarity, publish_article
Shared plan status: valid
Coordination completed
```

## Expected evaluation

Expected evaluation:

```text
success: true
role_count: 4
contribution_count: 4
role_clarity: true
shared_plan_valid: true
open_conflict_count: 0
trace_clarity: high
```

## Evaluation dimensions

| Metric | Meaning |
|---|---|
| Role clarity | Are roles distinct and responsible for different outputs? |
| Contribution count | Did agents produce inspectable contributions? |
| Conflict count | Were coordination issues surfaced? |
| Open conflict count | Did any unresolved conflicts remain? |
| Shared plan validity | Does the final plan have steps, valid roles, and correct status? |
| Trace clarity | Can a human inspect coordination decisions? |

## What this prototype proves

This project proves the fourth layer of the planning-agent stack:

```text
role outputs → conflict detection → deterministic coordination → shared plan → trace
```

That is the coordination layer needed before building a full integrated agent loop.

## Run command

From the repository root:

```bash
python projects/04_multi_agent_planning/run_demo.py
```

## Test command

From the repository root:

```bash
python -m pytest projects/04_multi_agent_planning/tests
```

## Current limitations

- Agent roles are deterministic, not live LLM agents.
- Contributions are loaded from JSON.
- Conflict resolution is simple and rule-based.
- Duplicate conflicts are treated as resolved automatically.
- No actual agent conversation yet.
- No direct integration with Projects 01-03 yet.

## Next improvement

The next useful step is to update this project README from design phase to runnable first prototype, then build an integrated demo across Projects 01-04.
