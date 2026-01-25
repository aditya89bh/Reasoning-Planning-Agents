# Project 05: Failure-Aware Planner

## Core Question
**How does an agent avoid repeating the same mistakes?**

---

## Problem

Most agents fail in a loop:

fail → retry → fail → retry → fail

They may reason correctly, plan well, and even choose the right strategy,
but once something goes wrong, they often:
- repeat the same failed actions
- retry blindly without adaptation
- lack an explicit memory of *why* something failed

Humans don’t work this way.

We say:
- “That failed because of X”
- “Don’t do that again”
- “Try a safer alternative”

This project gives agents that capability.

---

## What This Project Builds

A planner that can:

- detect execution failures
- classify *why* an action failed
- store failures as first-class memory
- mutate future plans to avoid known failures
- inject preventive constraints automatically

The agent learns not just *what worked*,  
but more importantly, *what should not be repeated*.

---

## Key Components

### 1. Failure Record
Each failure captures:
- the action that failed
- the cause of failure
- a timestamp

Failures are explicit data, not implicit signals.

---
