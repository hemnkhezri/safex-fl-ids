#!/usr/bin/env bash
# Study 3 (plan preregistration/study_plan_robustness_v3_SEALED.md): 130 units, seeds 300-309.
# Parts A-E: unsw/ton main, ton ip, unsw/ton big; Part F: cic main.
set -euo pipefail
cd "$(dirname "$0")/../src"
export OPENBLAS_NUM_THREADS=1
mkdir -p ../runs/study3
xargs -P "${WORKERS:-4}" -L 1 bash -c 'python3 s3_unit.py "$0" "$1" "$2" "$3" ../runs/study3 >> ../runs/study3/run.log 2>&1' < ../scripts/study3_jobs.txt
python3 analyze_s3.py ../runs/study3 ../results/study3/s3_scores.csv > ../results/study3/study3_report.md
