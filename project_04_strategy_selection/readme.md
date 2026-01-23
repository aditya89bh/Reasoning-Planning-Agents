# Project 04: Strategy Selection Agent

## Core Question
**Which strategy should an agent use in a given situation?**

---

## Problem

Most agents plan **from scratch every time**.

Even with memory and reasoning, they still:
- overthink simple situations
- fail to reuse proven approaches
- treat every task as a novel problem
- lack pattern-based judgment

Humans don’t work this way.

We recognize situations and say:
- “This needs careful debugging”
- “This is high-stakes, minimize risk”
- “This needs fast iteration”

That ability is **strategy selection**.

---

## What This Project Builds

A system that allows an agent to:

- define reusable **strategy templates**
- match **context → strategy**
- score strategies using past confidence
- select between strategies dynamically
- update strategy confidence over time

The agent no longer plans blindly.
It **chooses how to think and act**.

---

## Key Components

### 1. Strategy Template
Each strategy includes:
- name and description
- context tags it applies to
- confidence score
- usage history

Strategies are **patterns**, not plans.

---

### 2. Strategy Memory
Stores:
- all known strategies
- confidence levels
- usage counts
- last-used timestamps

This allows experience to accumulate at the **strategy level**.

---

### 3. Context Matching
Incoming situations are represented as:
- context tags (e.g. `high_stakes`, `time_pressure`, `debug`)

Strategies are scored using:
- similarity between context and strategy tags
- learned confidence from past use

---

### 4. Selection Policy
The agent selects a strategy using:
- exploitation (best-known strategy)
- exploration (occasionally try alternatives)

This prevents early lock-in and enables adaptation.

---

### 5. Confidence Update
After a strategy is chosen:
- its confidence is updated
- usage is tracked
- trust evolves over time

Strategies that work become dominant.
Strategies that fail slowly fade.

---

## Why This Matters

This is where agents start to feel **human-like**.

Instead of:
> “What steps should I generate?”

The agent asks:
> “What kind of approach fits this situation?”

This is the foundation for:
- strategic judgment
- behavioral consistency
- scalable autonomy

---

## Relationship to Other Projects

- **Project 01:** Learns from past outcomes
- **Project 02:** Reasons with evidence
- **Project 03:** Decomposes goals into structure
- **Project 04:** Chooses *how* to approach the problem

Future projects build on this:
- Project 05 → failure-aware strategy adjustment
- Project 06 → long-horizon strategy planning

---

## Mental Model

> Humans don’t plan from scratch.  
> They select patterns that have worked before.

This project gives agents that ability.

---

## Success Criteria

The agent should:
- select different strategies for different contexts
- reuse high-confidence strategies
- explore alternatives occasionally
- adapt strategy confidence over time

If this works, the agent has **judgment**, not just intelligence.

