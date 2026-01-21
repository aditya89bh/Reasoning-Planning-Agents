# ============================================
# Project 02: Explicit Reasoning Loop Agent
# Full end-to-end minimal implementation
# ============================================

import json
import os
import time
import hashlib
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
import random

# ---------- Utilities ----------

def now_ts():
    return time.time()

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def stable_hash(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()[:16]

def normalize(text: str) -> str:
    return " ".join(text.lower().strip().split())

def jaccard(a: List[str], b: List[str]) -> float:
    sa, sb = set(a), set(b)
    if not sa or not sb:
        return 0.0
    return len(sa & sb) / len(sa | sb)

# ---------- Data Models ----------
