#!/usr/bin/env bash
# Study 5 (plan preregistration/study_plan_aci_v5_SEALED.md): 30 units, seeds 500-509, K = 10, k = 20.
# Online recalibration (ACI) with analyst feedback on alarms, for SAFE-X and the better calibrated FedOV.
set -euo pipefail
cd "$(dirname "$0")/../src"
export OPENBLAS_NUM_THREADS=1
mkdir -p ../runs/study5
xargs -P "${WORKERS:-4}" -L 1 bash -c 'python3 pilot8_unit.py "$0" "$1" ../runs/study5 >> ../runs/study5/run.log 2>&1' < ../scripts/study5_jobs.txt
python3 analyze_study5.py ../runs/study5 ../results/study5/s5 > ../results/study5/study5_report.md
