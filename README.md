# SAFE-X: calibrated expert sharing for client-exclusive rare attacks

Code, pre-registered study plans and results for the paper
**"SAFE-X: Calibrated expert sharing for detecting client-exclusive rare attacks in federated intrusion detection"**
(submitted to *Computer Networks*).

The paper studies federated intrusion detection when a rare attack is labeled at a single client with only
5, 20 or 100 flows, on NF-UNSW-NB15-v3, NF-ToN-IoT-v3 and NF-CSE-CIC-IDS2018-v3. It reports three pre-registered
studies:

- **Study 1** measures the gap between federated and centralized training on such attacks and how seven
  federated methods fail.
- **Study 2** tests **SAFE-X**: each owner's local model is shared as an expert, and its alarm threshold is set
  on all clients' traffic (federated calibration).
- **Study 3** checks robustness: the full FedOV baseline, clients defined by destination hosts, membership
  inference and DP-SGD experts, label-free recalibration under drift, a larger model, and a third dataset.
- **Study 4** checks scale and settings: 20 and 50 clients, two or three owners per rare class, and false-alarm
  budgets q from 0.0001 to 0.01.

## Main results

| | NF-UNSW-NB15-v3 | NF-ToN-IoT-v3 |
|---|---|---|
| Gap, centralized minus best federated (rare F1 points, k = 5 / 20 / 100) | +7.0 / +12.7 / +18.1 | +8.3 / +22.5 / +28.0 |
| SAFE-X minus FedOV-tab + OC (rare F1 points, pooled over k) | +3.5 [+2.5, +4.3] | +3.8 [−0.6, +7.7] (not significant) |
| Expert false-alarm rate, owner-only vs federated calibration | 0.36% → 0.15% | 0.60% → 0.26% |

Study 3 (seeds 300-309):

| | Result |
|---|---|
| SAFE-X minus the better FedOV + OC, pooled over k | UNSW +3.5 [+2.3, +4.7]; ToN +0.2 [−3.5, +3.6] (n.s.); CIC-IDS2018 +4.1 [+2.1, +5.8] |
| Gap with destination-host clients (ToN), k = 5 / 20 / 100 | +21.1 / +29.2 / +27.4, all CIs > 0 |
| Gap on CIC-IDS2018, k = 5 / 20 / 100 | +10.8 / +13.7 / +15.4, all CIs > 0 |
| Expert false alarms, owner-only vs federated (host clients; CIC-IDS2018) | 6.9% → 0.18%; 5.2% → 1.3% |
| Membership-inference AUC of non-private experts at k = 5 | UNSW 0.85, ToN 0.77; DP-SGD (ε = 1, 8) brings it to about 0.5 but rare F1 collapses |

Study 4 (seeds 400-409, k = 20):

| | Result |
|---|---|
| Gap with K = 20 / 50 clients (G1) | +14.9 to +26.4 in all six dataset-K cells, all CIs > 0 (supported) |
| SAFE-X minus the better FedOV + OC with K = 20 / 50 (G2) | CIs > 0 in 3 of 6 cells (CIC both, UNSW K = 20); rule needed 4 (not supported) |
| Federated vs owner-only calibration with K = 20 / 50 (G3) | fewer false alarms in all six cells (supported) |
| SAFE-X minus the better FedOV + OC with 2 or 3 owners (H) | +3.4 to +7.6, CIs > 0 in 5 of 6 cells (descriptive) |
| False-alarm budget q (I) | SAFE-X's sign against FedOV + OC changes with q; q = 0.001 is the only tested value where it is behind on no dataset |

All pre-registered outcomes, including those not supported, are in `results/study1/CONFIRMATORY_SUMMARY.md`,
`results/study2/CONFIRMATORY_SUMMARY_v2.md`, `results/study3/study3_report.md` and `results/study4/study4_report.md`.

## Repository layout

```
preregistration/   sealed study plans and their SHA-256 hashes
src/               federated training, baselines, SAFE-X, analysis
src/dev/           development pilots (seeds 0-4; not used for any claim)
scripts/           run scripts, job lists, data conversion, hash check
results/           reports and per-class scores of every confirmatory run
paper/             figure scripts (Figs. 1-4, graphical abstract) and figures
data/              place the datasets here (see data/README.md)
```

## Reproducing

Everything runs on CPU with NumPy; no GPU is needed. Tested with Python 3.13.

```bash
pip install -r requirements.txt
python3 scripts/verify_preregistration.py          # check the sealed plans

# 1. data (see data/README.md)
python3 scripts/csv_to_parquet.py NF-UNSW-NB15-v3.csv data/nf_unsw_v3/NF-UNSW-NB15-v3.parquet
python3 scripts/csv_to_parquet.py NF-ToN-IoT-v3.csv  data/nf_toniot_v3/NF-ToN-IoT-v3.parquet
python3 scripts/csv_to_parquet.py NF-CSE-CIC-IDS2018-v3.csv data/nf_cic2018_v3/NF-CSE-CIC-IDS2018-v3.parquet
python3 src/prep_toniot.py
python3 src/prep_cic.py

# 2. confirmatory studies (WORKERS = parallel runs; lower it if memory runs out, since each run loads the full dataset)
WORKERS=4 bash scripts/run_study1.sh
WORKERS=4 bash scripts/run_study2.sh
WORKERS=4 bash scripts/run_study3.sh   # 130 units; the larger-model units take about 1.5 h each on one core
WORKERS=4 bash scripts/run_study4.sh   # 120 units, about 10-20 min each; Part I reads the Study 3 runs

# 3. figures from the score files
python3 paper/make_figures.py          # Figs. 2-4
python3 paper/make_fig1.py             # Fig. 1 (method overview)
python3 paper/make_graphical_abstract.py
```

Preprocessed arrays are cached in `~/.cache/safex` (override with `SAFEX_CACHE`). Per-run logits are written to
`runs/`, which is not tracked. The figures can be regenerated from the score CSVs in `results/` without
re-running any experiment.

| Script | What it does |
|---|---|
| `src/conf_fl.py` | Study 1 unit: FedAvg, FedAvg-bal, FedProx-bal, FedLC, FedRS, CCVR, GB+CR, FedRep, local and centralized models |
| `src/pilot5_expert.py` | Study 2 unit: owner experts (SAFE-X) and the GB+CR, FedProx-bal, CCVR and centralized baselines |
| `src/pilot6_baselines.py` | Study 2 unit: PROTEAN and FedOV-tab on the same clients and test sets |
| `src/analyze_conf.py`, `src/analyze_conf2.py` | OC / federated calibration, metrics, bootstrap CIs and the pre-registered decision rules |
| `src/audit_toniot.py` | Leakage and duplicate audit of NF-ToN-IoT-v3 |
| `src/s3_unit.py` | Study 3 unit (dataset, arm, seed, k): all methods incl. FedOV-full, DP-SGD experts, host-defined clients |
| `src/analyze_s3.py` | Study 3 metrics and decision rules (Parts A-F) |
| `src/prep_cic.py`, `src/audit_cic.py` | Pool and leakage audit of NF-CSE-CIC-IDS2018-v3 |
| `src/sealed_v3/` | The two Study 3 scripts exactly as sealed (before the Part F additions) |
| `src/s4_unit.py`, `src/analyze_s4.py` | Study 4 unit (K = 20/50 or 2-3 owners) and its decision rules (Parts G-I) |
| `src/sealed_v4/` | The two Study 4 scripts as sealed (identical to `src/`) |

## Notes

- The study 1 plan has one dated deviation (a 20,000-flow cap per common class on NF-ToN-IoT-v3), recorded
  before any confirmatory run. The recorded hash covers the plan text before that entry.
- FedOV-tab omits FedOV's adversarial outlier step and PROSER terms; FedOV-full (Study 3) adds them, with mixup at
  the input. PROTEAN is run under our training budget (Study 2 only).
- The Study 3 plan has one dated deviation: code to run the third dataset was added after sealing and before any of
  its results were seen. `scripts/verify_preregistration.py` checks the plan and the sealed scripts.

## Citation

Please cite the paper (details will be added on publication) and the NetFlow v3 datasets
(Luay et al., arXiv:2503.04404).

## License

MIT (see `LICENSE`).
