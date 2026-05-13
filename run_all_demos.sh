#!/usr/bin/env bash
set -euo pipefail

python projects/01_task_decomposition_agent/run_demo.py
python projects/02_planner_executor_agent/run_demo.py
python projects/03_reflection_agent/run_demo.py
python projects/04_multi_agent_planning/run_demo.py
python integrated_demo/run_integrated_demo.py
