#!/usr/bin/env bash
# Study 1 (plan preregistration/study_plan_hybrid_v1_SEALED.md): 90 units, seeds 100-109.
# Each line of study1_jobs.txt is: DATASET ARM SEED ALPHA K. Set WORKERS to the number of parallel runs.
set -euo pipefail
cd "$(dirname "$0")/../src"
export OPENBLAS_NUM_THREADS=1
OUT=../runs/study1; mkdir -p "$OUT"
xargs -P "${WORKERS:-4}" -L 1 bash -c 'python3 conf_fl.py "$0" "$1" "$2" "$3" "$4" '"$OUT"' >> '"$OUT"'/run.log 2>&1' < ../scripts/study1_jobs.txt
python3 analyze_conf.py "$OUT" > ../results/study1/conf_report.md
