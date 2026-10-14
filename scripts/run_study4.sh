#!/usr/bin/env bash
# Study 4 (plan preregistration/study_plan_scale_v4_SEALED.md): 120 units, seeds 400-409.
# Parts G (K = 20, 50) and H (2 or 3 owners) on unsw/ton/cic, k = 20; Part I reuses the Study 3 main-arm runs.
set -euo pipefail
cd "$(dirname "$0")/../src"
export OPENBLAS_NUM_THREADS=1
mkdir -p ../runs/study4
xargs -P "${WORKERS:-4}" -L 1 bash -c 'python3 s4_unit.py "$0" "$1" "$2" "$3" ../runs/study4 >> ../runs/study4/run.log 2>&1' < ../scripts/study4_jobs.txt
python3 analyze_s4.py ../runs/study4 ../runs/study3 ../results/study4/s4 > ../results/study4/study4_report.md
