# Study 5 (sealed before any confirmatory run): online calibration with analyst feedback

Sealed 2026-10-29, after pilot 8 (development seeds 0-4, report results/pilot8/pilot8_report.md) and before any run with seeds 500-509.
Time cap: one week from sealing; if not finished, the paper is submitted without Study 5.

## Question
Federated calibration (Studies 2-4) misses the 0.1% false-alarm target under temporal drift and costs common-attack F1 on CSE-CIC-IDS2018.
Does adaptive conformal inference (ACI) driven by analyst feedback on alarms meet the target, and at what cost in rare-class F1?

## Setting (fixed, identical to pilot 8 and Study 3 main arm)
Datasets UNSW-NB15-v3, ToN-IoT-v3, CSE-CIC-IDS2018-v3; K = 10 Dirichlet clients (alpha = 0.5), one owner per rare class, k = 20 shots, q = 0.001.
Seeds 500-509 (10 per dataset, 30 units). Code: safgt/code/pilot8_unit.py (unchanged), analysis safgt/code/analyze_study5.py.

## Methods
- SAFE-X: as in the paper (pooled federated calibration, Eq. 2).
- SAFE-X + ACI: same expert; threshold updated online on the time-ordered test stream,
  alpha_{t+1} = alpha_t + gamma (q - err_t), err_t = 1[alarm and flow is not class c] (only alarms need an analyst label),
  threshold_t = (1 - alpha_t) quantile of the federated calibration scores; gamma = 0.005 (fixed from the pilot; no other gamma is tested).
- FedOV+OC and FedOV+OC + ACI (same gamma), the better FedOV variant per unit by rare F1 as in pilot 8.

## Hypotheses (per dataset; paired bootstrap over seeds, 4000 resamples, 95% CI; all reported)
- J1 (target met): mean expert false-alarm rate of SAFE-X + ACI on non-rare test flows <= 0.0012, overall and on the second half of the stream.
- J2 (recall cost bounded): rare F1 of SAFE-X + ACI minus SAFE-X has lower CI bound > -3 points (non-inferiority).
- J3 (no harm): common-attack F1 of SAFE-X + ACI minus GB+CR has lower CI bound > -1 point.
- J4 (advantage kept): rare F1 of SAFE-X + ACI minus FedOV+OC + ACI has lower CI bound > 0.
Each is supported on a dataset only if its criterion holds there; we report the count over the three datasets.

## Not tested (dropped after pilot 8)
Frozen-encoder expert (mixed signs: CIC +4.9, UNSW -3.6, ToN -4.7) and per-group calibration (effects <= 1.5 points).

## Deviations
(none yet)
