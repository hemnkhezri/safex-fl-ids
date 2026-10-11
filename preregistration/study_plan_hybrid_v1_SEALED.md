# Confirmatory study plan v1 (SEALED 2026-10-10): client-exclusive rare attacks in federated IDS

Sealed before any confirmatory run. The SHA-256 of this file is recorded in study_plan_hybrid_v1_SEALED.sha256. Any later change goes in a dated "Deviations" section at the end, never by editing the text above it.
Development history: pilots 1-4 on NF-UNSW-NB15-v3 (results/pilot*_report.md). Those runs are development only; confirmatory runs use fresh seeds 100-109.

## 1. Setting
K = 10 clients. Common classes are spread over clients by Dirichlet(alpha) label skew. Each rare class gets k labelled training flows, all at one randomly chosen client (its owner); the remaining training flows of that class are unused. Benign training traffic is subsampled to 150,000 flows per run; benign test traffic to 100,000 flows.

## 2. Hypotheses and decision rules (rare F1 = mean F1 over the four rare classes; CIs = 95% seed-cluster bootstrap, 4,000 resamples)
- H1 (gap). Central-bal (argmax) minus the best global-view FL method (argmax) in rare F1 is > 0, CI excluding 0. Supported on a dataset if this holds for at least 2 of the 3 k values at alpha = 0.5.
- H2 (under-training confound). At E=1, R=60, FedAvg-bal's common-attack F1 trails Central-bal by more than at E=5, R=60 (paired difference of the two gaps, CI excluding 0). Reported per dataset.
- H3 (failure split). Descriptive: rare precision and recall of CCVR vs GB+CR; claimed only if, on both datasets, CCVR recall > GB+CR recall and GB+CR precision > CCVR precision in seed means at every k.
- H4 (fix). Owner calibration OC (q = 0.001, validation-period calibration) raises rare F1 over the same model's argmax (CI excluding 0) for a majority of the six global-view FL models {FedAvg-bal, FedProx-bal, FedLC, FedRS, CCVR, GB+CR} on each dataset, pooled over k; and no OC model loses more than 1 point of common-attack F1 or more than 0.002 of benign recall versus its argmax.
- Primary paper claim (P). Best FL+OC (model chosen as the one with the highest mean rare F1 across both datasets and all k, i.e. a single fixed model, not per setting) minus best FL argmax (per setting) in rare F1 > 0, CI excluding 0, at alpha = 0.5 for every k on both datasets. Reported along with the share of the H1 gap it closes.
- H5 (residual). Central-bal (argmax) minus best FL+OC: reported, no direction claimed.
- If H1 fails on NF-ToN-IoT-v3, the paper reports that the gap is dataset-dependent; no claim is generalised.

## 3. Data
- NF-UNSW-NB15-v3: global time-ordered 70/10/20 split; dropped: timestamps, IPs, L4_SRC_PORT, DNS_QUERY_ID, MIN_TTL, MAX_TTL, MIN_IP_PKT_LEN; test rows duplicated in train removed. Rare: Backdoor, Shellcode, Analysis, Worms. Common: Exploits, Fuzzers, Generic, Reconnaissance, DoS.
- NF-ToN-IoT-v3: per-class chronological 70/10/20 split (attacks are scheduled by day; audit results/audit_toniot_v3.md). Same dropped features. Rare (fewest flows): ransomware, mitm, Backdoor, dos. Common: ddos, xss, password, scanning, injection. For memory, a fixed pool is drawn once (seed 0) inside each split: per common attack class up to 200,000 train / 50,000 test flows, benign 1,000,000 train / 500,000 test, all rare-class flows, validation 200,000 flows. Test rows duplicated in train removed.
- Calibration set for OC: 20,000 validation-period flows with no rare-class flows.

## 4. Methods (all: same 45-64-32 MLP + linear head unless stated, Adam lr 1e-3, batch 256, E=5 local epochs, R=60 rounds)
Global view: FedAvg, FedAvg-bal (local class-balanced loss), FedProx-bal (mu = 0.01), FedLC, FedRS (missing-class logit scale 0.5), CCVR (on FedAvg-bal), GB+CR (global class-balanced loss + class-row head aggregation).
Owner view: FedRep (shared body, personal head), Local-owner-bal (owner trains alone, 60 epochs).
Reference: Central-bal (pooled training data, 60 epochs, class-balanced loss).
OC is applied post hoc to every global-view FL model and to Central-bal.
No per-method tuning: all hyperparameters are those used in the pilots.

## 5. Runs
- Primary: both datasets, alpha = 0.5, k in {5, 20, 100}, seeds 100-109, all methods.
- Secondary: alpha = 0.3, k = 20, seeds 100-104, all methods.
- Confound arm (H2): E = 1, R = 60, k = 20, alpha = 0.5, seeds 100-104; FedAvg-bal, GB+CR, Central-bal.
- Model-size arm: 45-128-64 MLP, k = 20, alpha = 0.5, seeds 100-104; FedAvg-bal, CCVR, GB+CR, Central-bal.
All conditions are reported, whatever the outcome.

## 6. Metrics
Per class: precision, recall, F1. Rare F1 (primary), common-attack F1, benign recall, macro-F1, MCC. Sensitivity of OC: q in {1e-4, 1e-2}, and owner in-sample calibration; reported, not used for claims.

## Deviations
(none yet)

- 2026-10-10 (before any confirmatory run): NF-ToN-IoT-v3 per-run cap of 20,000 training flows per common attack class (seed-specific draw from the pool), so that total client data (~250k flows) matches NF-UNSW-NB15-v3 (~233k) and CPU time stays feasible. Normalisation statistics are computed on the capped training flows.
