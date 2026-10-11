# Confirmatory results, plan v2 (SAFE-X: shared owner experts + federated calibration), runs finished 2026-10-11

Seeds 200-209, both datasets, k = 5/20/100, alpha = 0.5; 120/120 jobs. Full output: conf2_report.md; scores: conf2_scores.csv.

| Rule | NF-UNSW-NB15-v3 | NF-ToN-IoT-v3 |
|---|---|---|
| M1 SAFE-X - FedOV+OC (rare F1, pooled over k) | SUPPORTED +3.5 [+2.5, +4.3] | NOT supported +3.8 [-0.6, +7.7] |
| M2 vs best baseline per k (claimed only if CI > 0) | k=20 +3.4, k=100 +4.9 claimed; k=5 +2.2 (CI spans 0) | -1.9, +1.1, +2.1 (all CIs span 0) |
| M3 false alarms: owner-only minus federated calibration | SUPPORTED: 0.36% -> 0.15% (worst 4.6% -> 0.34%) | SUPPORTED: 0.60% -> 0.26% (worst 7.2% -> 1.2%) |
| M4 no harm (benign recall, common F1) | pass at every k | FAIL at every k (benign recall -0.007 to -0.009) |

Main claim (M1 on both datasets): NOT supported.
Target false-alarm rate 0.1% is not met by either calibration (federated: 1.5x on UNSW, 2.6x on ToN).
Descriptive: SAFE-X equals or beats the owner alone at k=20/100 on UNSW and at k=100 on ToN; federated calibration also gives higher rare F1 than owner-only calibration in all 6 settings (+0.6 to +6.7 points).
