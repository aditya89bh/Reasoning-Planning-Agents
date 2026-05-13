#!/usr/bin/env bash
set -euo pipefail

python -m pytest \
  projects/01_task_decomposition_agent/tests \
  projects/02_planner_executor_agent/tests \
  projects/03_reflection_agent/tests \
  projects/04_multi_agent_planning/tests
