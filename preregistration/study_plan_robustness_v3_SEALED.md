# Confirmatory study plan v3 (SEALED 2026-10-12): robustness of the findings

Code: code/s3_unit.py (one unit) and code/analyze_s3.py (rules), smoke-tested on seed 0 with 2 rounds before sealing.
Purpose: answer the weaknesses a reviewer is expected to raise about Studies 1-2 (plans v1, v2), with fresh seeds 300-309 (never used before). Studies 1-2 and their outcomes are not changed by this study; it is reported as Study 3. Development and smoke tests use seeds 0-1 only.

## 1. Common setting (unless a part says otherwise)
As plan v2 section 1: K = 10, alpha = 0.5 Dirichlet skew for common classes, k in {5, 20, 100} labelled flows per rare class at one owner, benign subsampling, ToN cap of 20,000 training flows per common class, same 45-64-32 MLP, Adam, E = 5, R = 60, q = 0.001. SAFE-X exactly as plan v2 section 2. Metrics: rare F1 (primary), rare precision/recall, common F1, benign recall, macro-F1, multiclass MCC, expert false-alarm rate. CIs: 95% seed-cluster bootstrap, 4,000 resamples.

## 2. Parts, runs and decision rules

### Part A. Full FedOV baseline (both datasets, all k, seeds 300-309)
FedOV-full adds to FedOV-tab the two outlier generators of FedOV that were omitted before: (i) adversarial unknowns: FGSM perturbations x + 0.5 sign(grad_x CE) of a random 25% of local flows, regenerated every local epoch from the current local model; (ii) mixup unknowns: convex mixes (lambda ~ U(0.3, 0.7)) of random pairs of local flows from different classes, 25% of local size, regenerated every epoch (input-level mixup; FedOV's PROSER applies it at a hidden layer; stated as a remaining difference). Destroyed copies as in FedOV-tab are kept. Each local model trains for 60 epochs.
- A1 (primary). SAFE-X minus the better of FedOV-full+OC and FedOV-tab+OC (better = higher seed-mean rare F1 per dataset, pooled over k), rare F1 pooled over k: > 0 with CI excluding 0. Reported per dataset; supported on a dataset if so.
- A2. SAFE-X minus FedOV-full+OC per (dataset, k): reported with CIs.

### Part B. Realistic sites on NF-ToN-IoT-v3 (all k, seeds 300-309)
Clients are sites defined by destination hosts instead of Dirichlet sampling: every distinct IPV4_DST_ADDR in the training period is assigned to one of 10 sites by a seeded greedy assignment that balances training-flow counts (hosts shuffled with the seed, each host goes to the currently smallest site). All training flows to a host belong to its site (benign subsampled to 150,000 overall first; common classes capped as in section 1). The owner of each rare class is the site holding most of its training flows; its k labelled flows are drawn from that site's flows of the class; rare flows at all other sites are removed from training. If the owner holds fewer than k flows, all are used and the count is reported. NF-UNSW-NB15-v3 is not used in Part B: its attacks target 10 hosts evenly and its benign traffic 10 other hosts, so destination sites would separate benign from attack traffic artificially.
- B1. Gap: Central-bal argmax minus best global FL argmax (GB+CR, FedProx-bal, CCVR, per-seed max) in rare F1 > 0 with CI excluding 0 for at least 2 of 3 k.
- B2. SAFE-X minus FedOV-tab+OC, rare F1 pooled over k, > 0 with CI excluding 0.
- B3. Expert false-alarm rate: owner-only minus federated calibration > 0, CI excluding 0.

### Part C. Privacy of shared experts (both datasets, all k, seeds 300-309, from the Part A runs)
- C1 (descriptive). Membership inference on each shared expert: members = the owner's k labelled rare flows; non-members = k flows of the same class from the training period that were never used; attack score = the expert's margin s_c; AUC per (class, seed), pooled over classes and seeds, reported per (dataset, k) with CI. No direction claimed.
- C2. DP experts: each expert is also trained with DP-SGD (Poisson sampling rate 256/N_owner, per-example clipping norm 1.0, Gaussian noise sigma calibrated by an RDP accountant (dp-accounting) to epsilon in {1, 8} at delta = 1e-5 over 60 epochs; plain SGD learning rate 0.05). SAFE-X-DP uses the DP experts with federated calibration. Reported: rare F1, false-alarm rate and C1 AUC for epsilon = 1, 8 and non-private. Rule C2: SAFE-X-DP (epsilon = 8) minus FedOV-tab+OC in rare F1 pooled over k reported with CI; claimed only if CI excludes 0.

### Part D. Recalibration under drift (both datasets, all k, seeds 300-309, from the Part A runs)
Test flows are ordered by FLOW_START_MILLISECONDS. The earliest 25% form a recalibration window; all metrics in Part D are computed on the remaining 75%. Static: thresholds as in SAFE-X. Recalibrated: each expert's threshold is the (1 - q) quantile of its score on all flows of the window (label-free: no labels used; the window may contain rare flows).
- D1. Expert false-alarm rate on the evaluation part: static minus recalibrated > 0 with CI excluding 0, per dataset.
- D2 (descriptive). Rare F1 and benign recall of SAFE-X static vs recalibrated, and whether the 0.1% target is met.

### Part E. Larger model (both datasets, k = 20, seeds 300-304)
45-256-128 MLP for every method in Part A. E1 (descriptive): SAFE-X, FedOV-tab+OC, FedOV-full+OC, GB+CR, CCVR+OC, Central-bal rare F1 and MCC; the paper states whether the ranking of SAFE-X vs FedOV+OC matches the 45-64-32 results.

### Part F. Third dataset: NF-CSE-CIC-IDS2018-v3 (all k, seeds 300-309), only if the user provides the file
Before any run: a leakage audit as for ToN (identifiers, single-feature balanced accuracy, duplicates), with the same dropped features plus any feature whose single-feature balanced accuracy for benign vs attack exceeds 0.99. Class choice by rule: using the Attack labels in the file, the four attack classes with the fewest flows (at least 100 flows each) are rare and up to five of the remaining classes with the most flows are common. Split: per-class chronological 70/10/20 if any attack class spans fewer than half of the capture days, otherwise global chronological. A fixed seed-0 pool as for ToN (common classes up to 200,000 train / 50,000 test, benign 1,000,000 / 500,000, all rare flows) and the 20,000 per-run common cap.
- F1. Gap as B1. F2. SAFE-X minus the better FedOV+OC (as A1), pooled over k. F3. False-alarm rate as B3. F4. No-harm as plan v2 M4.

## 3. Methods per run
GB+CR, FedProx-bal, CCVR (each argmax and +OC), FedOV-tab and FedOV-full (each argmax and +OC), SAFE-X (federated and owner-only calibration), SAFE-X-DP (epsilon 1, 8), Owner alone, Central-bal. PROTEAN is not re-run (it was the weakest baseline in Study 2); stated in the paper.

## 4. Cost reporting
Communication per client (parameters sent and received) and median CPU training time per method, from the run logs.

## 5. Reporting
All parts and all conditions are reported regardless of outcome. Any change after sealing goes in a dated Deviations section.

## Deviations
- 2026-10-12 (before any Part F run; Parts A-E runs were already in progress and are unaffected). The user provided NF-CSE-CIC-IDS2018-v3 (20,115,529 flows, 41 Parquet parts, merged unchanged). Part F was executed exactly by its rules: audit in results/audit_cic2018_v3.md; no feature exceeded the 0.99 single-feature rule, so the dropped features are those of ToN; every attack class spans at most 2 of 11 capture days, so the split is per-class chronological 70/10/20; rare = SQL_Injection, Brute_Force_-XSS, Brute_Force_-Web, DDOS_attack-LOIC-UDP; common = DDOS_attack-HOIC, FTP-BruteForce, DDoS_attacks-LOIC-HTTP, Bot, SSH-Bruteforce (other classes excluded). Pool built by code/prep_cic.py with the section-2 caps. Code changes after sealing, needed to run Part F and made without looking at any Part F result: conf_fl.py gains the "cic" class lists and CIC_POOL; s3_unit.py reads CIC_POOL for ds == "cic" and applies the 20,000 common cap to CIC as to ToN (ToN and UNSW behaviour unchanged); analyze_s3.py gains the Part F block (F1 as B1, F2 as A1, F3 as B3, F4 as plan v2 M4) and reports CIC only in Part F. The sealed versions of both scripts are kept in code/sealed_v3/ (hashes match the .sha256 file). Known limitation of the audit table: its n_src column counts all IPs in the file, not per class (categorical dtype); top-share columns are correct. One smoke unit with development seed 0 and 2 rounds checked that the code runs; its numbers are not used.

