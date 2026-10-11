# Confirmatory study plan v2 (SEALED 2026-10-11): shared owner experts with federated calibration

Sealed before any confirmatory run of this method; SHA-256 in study_plan_experts_v2_SEALED.sha256. Later changes go only in the dated "Deviations" section.
Development: pilots 5-6 (seeds 0-4; results/pilot5_report.md, pilot6_report.md). Confirmatory seeds: 200-209 (never used before).

## 1. Setting (unchanged from plan v1)
Datasets, splits, dropped features, rare classes, K = 10 clients, alpha = 0.5, benign subsampling, ToN common-class cap of 20,000 training flows: exactly as study_plan_hybrid_v1_SEALED.md sections 1, 3 and its deviation. k in {5, 20, 100}.

## 2. Method (fixed)
SAFE-X (working name): for each rare class c, its owner trains a local model on its own data (45-64-32 MLP, class-balanced CE, 60 epochs) and shares the parameters. Score s_c(x) = logit_c - max_{j != c} logit_j of that expert. Threshold tau_c = (1 - q) quantile of s_c over the non-rare training flows of ALL clients (federated calibration; in deployment computed by secure aggregation of score histograms), q = 0.001. Prediction: if some rare c has s_c >= tau_c, predict the one with the largest s_c - tau_c; otherwise the global GB+CR model's argmax over non-rare classes. Code: code/pilot5_expert.py (method "Experts[fed] + GB+CR" in analyze_pilot5.py).

## 3. Baselines (fixed, same seeds and test sets)
GB+CR, FedProx-bal, CCVR (each argmax and +OC with validation calibration, q = 0.001), PROTEAN (argmax and +OC), FedOV-tab (argmax and +OC) as in code/pilot6_baselines.py; Owner alone (owner view); Central-bal (reference). Ablation: SAFE-X with owner-only calibration ("Experts[own]").

## 4. Hypotheses and decision rules (rare F1 = mean over the four rare classes; 95% seed-cluster bootstrap, 4,000 resamples)
- M1 (primary). SAFE-X minus FedOV+OC in rare F1, pooled over k (per-seed mean over the three k values), > 0 with CI excluding 0. Supported on a dataset if so; the paper's main claim requires both datasets.
- M2. SAFE-X minus the best baseline of section 3 (excluding Central-bal and Owner alone), the best chosen per (dataset, k) by its seed mean on these confirmatory runs: reported per (dataset, k) with CIs; claimed only where the CI excludes 0.
- M3 (calibration). False-alarm rate of the shared experts on non-rare test flows (fraction of non-rare test flows on which expert c fires, averaged over the four classes): owner-only minus federated > 0 with CI excluding 0, per dataset. The achieved rate is reported against the target q = 0.001 without claiming the target is met.
- M4 (no harm). SAFE-X benign recall >= GB+CR argmax benign recall - 0.002 and common-attack F1 >= GB+CR argmax - 1 point, seed means, per dataset and k.
- M5 (descriptive). SAFE-X vs Owner alone and vs Central-bal.
All conditions reported regardless of outcome.

## Deviations
(none yet)
