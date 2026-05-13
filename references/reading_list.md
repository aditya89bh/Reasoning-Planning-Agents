# Reading List

This reading list supports the Reasoning Planning Agents repository.

The goal is not to collect every agent paper. The goal is to keep a compact research spine for task decomposition, planning loops, reflection, tool use, multi-agent coordination, and agent evaluation.

## Agent reasoning and action loops

| Resource | Why it matters |
|---|---|
| ReAct: Synergizing Reasoning and Acting in Language Models | Foundation for interleaving reasoning traces with actions |
| Reflexion: Language Agents with Verbal Reinforcement Learning | Useful reference for reflection and self-improvement loops |
| Tree of Thoughts | Relevant to search over reasoning paths and candidate plans |
| Self-Refine | Relevant to iterative improvement through feedback |

## Planning agents

| Resource | Why it matters |
|---|---|
| Plan-and-Solve Prompting | Useful for explicit plan-first reasoning |
| Least-to-Most Prompting | Relevant to decomposing hard tasks into simpler subtasks |
| Chain-of-Thought Prompting | Baseline reference for explicit intermediate reasoning |
| Program-Aided Language Models | Useful for separating reasoning from executable computation |

## Tool-using agents

| Resource | Why it matters |
|---|---|
| Toolformer | Reference for learning to use tools |
| Gorilla: Large Language Model Connected with Massive APIs | Relevant to API/tool use by agents |
| HuggingGPT | Useful reference for orchestrating specialist models/tools |
| MRKL Systems | Early framing for modular reasoning and tool routing |

## Multi-agent systems

| Resource | Why it matters |
|---|---|
| CAMEL: Communicative Agents for Mind Exploration | Reference for role-playing and multi-agent collaboration |
| AutoGen | Practical framework reference for multi-agent conversations |
| MetaGPT | Useful for role-based software-agent workflows |
| ChatDev | Reference for simulated multi-agent software teams |

## Agent memory and state

| Resource | Why it matters |
|---|---|
| Generative Agents: Interactive Simulacra of Human Behavior | Useful for memory, reflection, and behavior over time |
| Voyager | Relevant to lifelong agents with skill memory |
| MemGPT | Useful for memory management and context limits |
| Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks | Baseline for retrieval-backed agent context |

## Evaluation and benchmarks

| Resource | Why it matters |
|---|---|
| AgentBench | Useful benchmark reference for evaluating LLM agents |
| WebArena | Relevant to web-based agent task evaluation |
| SWE-bench | Reference for evaluating agents on real software tasks |
| GAIA | Useful reference for general assistant benchmark tasks |

## Robotics and embodied planning

| Resource | Why it matters |
|---|---|
| SayCan: Do As I Can, Not As I Say | Connects language planning with affordance-based action selection |
| Inner Monologue: Embodied Reasoning through Planning with Language Models | Relevant to language-mediated robot planning and feedback |
| Code as Policies | Useful for converting language goals into robot-executable policies |
| RT-2 | Relevant to vision-language-action transfer for robotics |

## Classical planning foundations

| Resource | Why it matters |
|---|---|
| STRIPS | Foundational symbolic planning representation |
| Hierarchical Task Networks | Useful for task decomposition and hierarchical planning |
| PDDL | Standard representation for planning domains and problems |
| Partial-Order Planning | Useful for reasoning about dependencies and flexible execution order |

## How to use this list

Use the list as a working reference, not as a reading marathon.

Recommended sequence for this repository:

1. Start with task decomposition and plan-first reasoning.
2. Study ReAct and Reflexion for action/reflection loops.
3. Study tool-using agents after the deterministic loop works.
4. Study multi-agent systems only after the single-agent loop is inspectable.
5. Study planning foundations to improve decomposition and dependency logic.
6. Map each idea back into runnable prototypes.

## Near-term reading priority

For Project 01, prioritize:

1. Least-to-Most Prompting
2. Plan-and-Solve Prompting
3. Hierarchical Task Networks
4. PDDL basics
5. Chain-of-Thought Prompting

For Project 02, prioritize:

1. ReAct
2. Program-Aided Language Models
3. Toolformer
4. MRKL Systems
5. SayCan

For Project 03, prioritize:

1. Reflexion
2. Self-Refine
3. Generative Agents
4. Voyager
5. Inner Monologue

For Project 04, prioritize:

1. CAMEL
2. AutoGen
3. MetaGPT
4. ChatDev
5. Multi-agent evaluation examples from AgentBench

## Rule for adding references

A reference should only be added if it supports at least one of these:

- task decomposition
- planning loops
- execution tracking
- reflection
- revision
- tool use
- multi-agent coordination
- agent evaluation
- embodied planning

Do not turn this into a generic AI paper dump.
