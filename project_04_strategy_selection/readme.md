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

