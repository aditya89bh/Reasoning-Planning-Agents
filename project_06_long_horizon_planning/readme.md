# Project 06: Long-Horizon Planning Agent

## Core Question
**How does an agent pursue a goal across time without losing direction?**

---

## Problem

Most agents operate in short, isolated episodes.

They can:
- reason correctly
- plan individual tasks
- select strategies
- adapt after failures

Yet they still fail at **long-term autonomy**.

They:
- lose sight of the original goal
- replan too often or not at all
- fail to detect drift
- persist with failing objectives indefinitely

Humans don’t work this way.

We:
- commit to long-term goals
- periodically check progress
- notice when we are off track
- adapt strategy or abandon goals when necessary

This project gives agents those capabilities.

---

## What This Project Builds

A long-horizon planning layer that enables an agent to:

- maintain persistent goals over time
- track incremental progress
- evaluate progress against explicit checkpoints
- detect drift from expectations
- trigger deliberate replanning
- abandon goals when confidence collapses

This is the final step toward **true autonomy**.

---

## Key Components

### 1. Goal State
A long-lived representation of intent that includes:
- goal description
- confidence level
- progress estimate
- active or abandoned status
- execution history

The goal persists across multiple planning cycles.

---

### 2. Checkpoints
Explicit milestones that define:
- expected progress thresholds
- semantic meaning (not just time-based)

Checkpoints anchor long-term intent and make drift measurable.

---

### 3. Progress Tracking
The agent updates progress incrementally over time.
Progress is treated as a continuous signal, not a binary outcome.

This enables nuanced evaluation rather than pass/fail logic.

---

### 4. Drift Detection
At each checkpoint, the agent evaluates:
- “Am I where I expected to be by now?”

If actual progress falls outside acceptable bounds,
the agent detects **drift**.

---

### 5. Replanning Logic
When drift is detected:
- the agent reduces confidence in the current plan
- replanning is triggered intentionally
- the event is logged in execution history

Replanning is controlled, not reactive.

---

