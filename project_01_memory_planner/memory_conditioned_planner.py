"""
Project 01: Memory-Conditioned Planner
Single-file implementation (Colab + local friendly)

What it does:
- Generates multiple candidate plans for a goal (plan graph as ordered steps + deps)
- Scores plans using episodic memory (success/failure + decay + context similarity)
- Selects a plan (epsilon-greedy)
- Executes in a simulated environment (for end-to-end testing)
- Logs execution traces
- Updates memory

Files created:
- data/episodic_memory.jsonl
- data/execution_traces.jsonl
"""

from __future__ import annotations

import json
import os
import random
import time
import hashlib
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Tuple


# -----------------------------
# Utilities
# -----------------------------

def now_ts() -> float:
    return time.time()

def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)

def stable_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]

def normalize_step(step: str) -> str:
    # Normalize step text to reduce dependence on phrasing
    s = step.strip().lower()
    # Very light normalization; you can extend later
    s = " ".join(s.split())
    return s

def jaccard_similarity(a: List[str], b: List[str]) -> float:
    sa, sb = set(a), set(b)
    if not sa and not sb:
        return 1.0
    if not sa or not sb:
        return 0.0
    return len(sa & sb) / len(sa | sb)

# -----------------------------
# Data models
# -----------------------------

@dataclass
class Plan:
    """
    Plan graph representation:
    - steps: ordered list of actions
    - deps: dependencies between steps represented as edges (i -> j) meaning step j depends on step i
      For simple linear plans, deps are (0->1, 1->2, ...)
    """
    goal: str
    context_tags: List[str]
    steps: List[str]
    deps: List[Tuple[int, int]]
    fingerprint: str

@dataclass
class EpisodicRecord:
    fingerprint: str
    goal: str
    context_tags: List[str]
    steps: List[str]
    outcome: str  # "success" | "failure" | "partial"
    score_delta: float
    confidence_after: float
    ts: float
    notes: str = ""

@dataclass
class PlanScoreBreakdown:
    base_confidence: float
    memory_evidence: float
    similarity: float
    recency_weight: float
    final_score: float


# -----------------------------
# Episodic Memory Store (JSONL)
# -----------------------------

class EpisodicMemory:
    """
    JSONL store of episodic outcomes keyed by plan fingerprint.
    Keeps an in-memory index for fast scoring.
    """

    def __init__(self, path: str):
        self.path = path
        ensure_dir(os.path.dirname(path) or ".")
        self.records: List[EpisodicRecord] = []
        # Stats per fingerprint
        self.confidence: Dict[str, float] = {}
        self.successes: Dict[str, int] = {}
        self.failures: Dict[str, int] = {}
        self.partials: Dict[str, int] = {}
        self.last_ts: Dict[str, float] = {}
        self.context_history: Dict[str, List[List[str]]] = {}
        self._load()

    def _load(self) -> None:
        if not os.path.exists(self.path):
            return
        with open(self.path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                obj = json.loads(line)
                rec = EpisodicRecord(**obj)
                self.records.append(rec)
                self._index_record(rec)
