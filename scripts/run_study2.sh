#!/usr/bin/env bash
# Study 2 (plan preregistration/study_plan_experts_v2_SEALED.md): 60 units x 2 scripts, seeds 200-209.
set -euo pipefail
cd "$(dirname "$0")/../src"
export OPENBLAS_NUM_THREADS=1
mkdir -p ../runs/study2/p5 ../runs/study2/p6
xargs -P "${WORKERS:-4}" -L 1 bash -c 'python3 "$0" "$1" "$2" "$3" "$4" >> ../runs/study2/run.log 2>&1' < ../scripts/study2_jobs.txt
python3 analyze_conf2.py ../runs/study2 > ../results/study2/conf2_report.md
