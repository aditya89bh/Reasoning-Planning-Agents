# Project 01: Memory-Conditioned Planner

## Core Question
How should past outcomes shape future plans?

---

## Problem

Most agents generate plans in isolation.

They:
- ignore what worked before
- repeat known failures
- treat every task as a fresh problem

As a result, they **do not develop strategy**.  
They only execute.

---

## What This Project Builds

A planner that:
- generates multiple candidate plans
- scores each plan using episodic memory
- prefers plans that worked in similar contexts
- avoids plans associated with past failures

This introduces **experience-driven decision making**.

---

## High-Level Behavior

1. Agent receives a goal
2. Planner generates multiple candidate plans
3. Each plan is evaluated against past outcomes
4. A plan is selected based on memory-informed scores
5. Execution is traced and logged
6. Outcomes update memory for future planning

---

## Key Components

### 1. Plan Generator
- Produces multiple candidate plans
- Each plan consists of ordered steps and dependencies

### 2. Episodic Memory Store
- Stores past plans, contexts, and outcomes
- Tracks success, failure, and partial success

### 3. Memory → Plan Scoring
- Matches current context with past experiences
- Adjusts plan scores based on historical outcomes

### 4. Plan Selection Policy
- Chooses plans probabilistically or deterministically
- Biases toward high-confidence, high-success plans

### 5. Execution Trace Logger
- Records:
  - selected plan
  - execution steps
  - final outcome
  - confidence updates

---
## Why This Matters

This is the **first moment the agent learns strategy**, not facts.

Instead of asking:
> “What should I do?”

The agent starts asking:
> “What has worked before in situations like this?”

This is the foundation for:
- planning
- reasoning
- failure avoidance
- long-term autonomy

---

## Non-Toy Extensions

These upgrades prevent the system from becoming brittle or overconfident.

### Plan Decay
- Older experiences gradually lose influence
- Prevents overfitting to outdated strategies

### Confidence Scores
- Each plan carries a confidence value
- Updated after every execution

### Plan Fingerprints
- Plans are stored as abstract representations
- Avoids dependence on raw text or phrasing

---

## Open Questions

- How similar must contexts be to reuse a plan?
- When should a successful plan be retired?
- How do we balance exploration vs exploitation?
- Should failure always penalize, or sometimes inform?

---

## Position in the Project Set

This project is the foundation for:
- strategy selection
- failure-aware planning
- long-horizon decision making

Everything that follows **builds on this**.
