# Confirmatory results, sealed plan v1 (runs finished 2026-10-11)

Full output: conf_report.md; per-class scores: conf_scores.csv; 90/90 units (one UNSW unit re-run after an out-of-memory failure, same seed).

## Sealed decision rules
| Rule | NF-UNSW-NB15-v3 | NF-ToN-IoT-v3 |
|---|---|---|
| H1 gap (Central vs best FL, rare F1) | SUPPORTED: +7.0 / +12.7 / +18.1 at k=5/20/100, all CIs > 0 | SUPPORTED: +8.3 / +22.5 / +28.0, all CIs > 0 |
| H2 E=1 under-training confound | SUPPORTED: +3.1 [+0.9, +5.9] | NOT supported: +1.8 [-1.8, +5.1] |
| H3 failure split (CCVR high recall / GB+CR high precision) | SUPPORTED at every k | SUPPORTED at every k |
| H4 OC raises rare F1 without harm, >= 4/6 models | SUPPORTED 6/6 | NOT supported 3/6 (rare F1 rises +4.7 to +18.6 for all 6, but 3 models lose 0.003-0.010 benign recall, over the 0.002 limit) |
| P best fixed FL+OC (CCVR, chosen by the sealed rule) > best FL argmax at every k | NOT supported (-0.4, +0.0, +4.6) | supported at every k (+4.6, +8.5, +11.6) |
| H5 residual gap after OC | +7.5 / +12.7 / +13.5 | +3.8 (CI includes 0) / +13.9 / +16.4 |

Overall: P NOT supported (fails on UNSW at k=5 and k=20).

## Reported, not part of the decision rules
- Owner view: the rare-class owner's purely local model beats every federated option on its own class (ToN 0.63-0.71 vs FedRep 0.54-0.65 and best global FL+OC 0.58-0.67; UNSW 0.22-0.25 vs FedRep 0.21-0.24 and best FL+OC 0.15-0.22). Note: owner-view F1 is per owner class, global-view F1 is per class from one shared model; comparable but not identical protocols.
- OC lowers the centralised model's rare F1 (ToN 0.83 -> 0.71 at k=100; UNSW 0.35 -> 0.25): it is a fix for weak federated heads, not a general improvement.
- ToN benign recall is only ~0.92 for every model (benign test traffic is from later days than benign train), so calibration on validation-period traffic under-estimates the test false-alarm rate there.
- alpha=0.3 and the larger model give the same picture as the primary setting.
