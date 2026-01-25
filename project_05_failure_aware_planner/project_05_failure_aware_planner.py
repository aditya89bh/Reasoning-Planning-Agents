# ============================================
# Project 05: Failure-Aware Planner
# Full end-to-end minimal implementation
# ============================================

import time
import random
from dataclasses import dataclass, asdict, field
from typing import List, Dict, Optional
import json


# -----------------------------
# Data Models
# -----------------------------

@dataclass
class FailureRecord:
    action: str
    cause: str
    ts: float


@dataclass
class Plan:
    goal: str
    actions: List[str]
    constraints: List[str] = field(default_factory=list)


# -----------------------------
# Failure Memory
# -----------------------------

