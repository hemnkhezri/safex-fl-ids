# Confirmatory study plan v4 (SEALED 2026-10-13): sensitivity to q, number of clients, and number of owners

Code: code/s4_unit.py (one unit) and code/analyze_s4.py (rules), smoke-tested before sealing with 2 rounds on development seeds 0-1 (and one Study 3 unit with seed 0 for Part I); no smoke number is used.
Purpose: answer three reviewer questions about Studies 1-3: (i) does the result depend on the false-alarm budget q = 0.001; (ii) does it hold with more, smaller clients; (iii) does it hold when a rare class is held by a few clients rather than exactly one. Fresh seeds 400-409 for Parts G and H. Studies 1-3 and their outcomes are not changed; this is reported as Study 4.

## 1. Common setting (unless a part says otherwise)
As plan v3 section 1 and Part A: Dirichlet alpha = 0.5 for common classes, 45-64-32 MLP, Adam, E = 5, R = 60, q = 0.001, ToN/CIC 20,000 per-run common cap, the same pools and splits. Datasets: NF-UNSW-NB15-v3, NF-ToN-IoT-v3, NF-CSE-CIC-IDS2018-v3. k = 20 labelled flows per rare class per owner. Methods per run: GB+CR, FedProx-bal, CCVR, FedOV-tab, FedOV-full (each argmax and +OC), Central-bal, Owner alone, SAFE-X (federated and owner-only calibration). DP experts are not trained. Metrics and CIs as plan v3 (95% seed-cluster bootstrap, 4,000 resamples).

## 2. Parts, runs and decision rules

### Part G. More clients (K = 20 and K = 50, one owner per rare class; 3 datasets x 2 K x 10 seeds = 60 units)
Identical to Study 3 Part A except the number of clients.
- G1. Gap: Central-bal argmax minus best global FL argmax (per-seed max of GB+CR, FedProx-bal, CCVR) in rare F1, CI excluding 0 in at least 4 of the 6 (dataset, K) cells.
- G2. SAFE-X minus the better of FedOV-tab+OC and FedOV-full+OC (higher seed mean in that cell) in rare F1, CI excluding 0 in at least 4 of 6 cells.
- G3. Expert false-alarm rate on non-rare test flows, owner-only minus federated calibration, CI excluding 0 in at least 4 of 6 cells.
- Reported descriptively per cell: SAFE-X minus the best of CCVR+OC, GB+CR+OC, FedProx-bal+OC; common-attack F1 of SAFE-X minus GB+CR; MCC.

### Part H. Several owners (K = 10; each rare class at m = 2 or 3 distinct clients chosen at random, each owner with k = 20 disjoint labelled flows; 3 datasets x 2 m x 10 seeds = 60 units)
SAFE-X with m owners: every owner trains its own expert; each expert's threshold is the federated (1 - q/m) quantile of its margin over all clients' non-rare training flows (so the class's false-alarm budget stays about q); a class fires if any of its experts exceeds its threshold, and its excess is the largest over its experts; fusion otherwise as in plan v2. Owner-only calibration uses each owner's own non-rare flows.
- H (descriptive, no claim of support required): per (dataset, m), the gap as G1, SAFE-X minus the better FedOV+OC, SAFE-X minus the best global+OC, false-alarm rates, common-F1 change and MCC. The paper states how the gap and the SAFE-X advantage change from m = 1 (Study 3 Part A/F) to m = 2, 3, and claims an advantage only where the CI excludes 0.

### Part I. Sensitivity to q (no new runs: the 90 Study 3 main-arm runs, seeds 300-309, k in {5, 20, 100}, three datasets)
q in {0.0001, 0.0003, 0.001, 0.003, 0.01}, applied to SAFE-X (federated calibration) and to CCVR+OC, FedOV-tab+OC and FedOV-full+OC.
- I1 (descriptive): per dataset and q, rare F1 of each method; for SAFE-X, expert false-alarm rate, rare precision and recall and common-F1 change vs GB+CR; SAFE-X minus the better FedOV+OC with CI. The paper reports the q range over which SAFE-X's sign against FedOV+OC is unchanged, and does not choose a new q.

## 3. Reporting
All parts and cells are reported regardless of outcome. Any change after sealing goes in a dated Deviations section.

## Deviations
(none yet)
