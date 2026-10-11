# Pilot 4: owner-calibrated rare-class threshold (step 4), alpha=0.5, E=5, R=60, seeds [np.int64(0), np.int64(1), np.int64(2), np.int64(3), np.int64(4)]

## k=20: rare-class F1 / precision / recall (mean over 4 rare classes and seeds)

| rule            |   ('f1', 'CCVR') |   ('f1', 'Central-bal') |   ('f1', 'FedAvg-bal') |   ('f1', 'GB+CR') |   ('precision', 'CCVR') |   ('precision', 'Central-bal') |   ('precision', 'FedAvg-bal') |   ('precision', 'GB+CR') |   ('recall', 'CCVR') |   ('recall', 'Central-bal') |   ('recall', 'FedAvg-bal') |   ('recall', 'GB+CR') |
|:----------------|-----------------:|------------------------:|-----------------------:|------------------:|------------------------:|-------------------------------:|------------------------------:|-------------------------:|---------------------:|----------------------------:|---------------------------:|----------------------:|
| OC-own q=0.0001 |            0.054 |                   0.211 |                  0.017 |             0.094 |                   0.179 |                          0.441 |                         0.1   |                    0.229 |                0.041 |                       0.175 |                      0.011 |                 0.091 |
| OC-own q=0.001  |            0.144 |                   0.285 |                  0.06  |             0.191 |                   0.188 |                          0.293 |                         0.154 |                    0.229 |                0.178 |                       0.364 |                      0.057 |                 0.249 |
| OC-own q=0.01   |            0.163 |                   0.215 |                  0.095 |             0.178 |                   0.113 |                          0.151 |                         0.083 |                    0.125 |                0.549 |                       0.633 |                      0.181 |                 0.525 |
| OC-val q=0.0001 |            0.103 |                   0.288 |                  0.047 |             0.16  |                   0.189 |                          0.325 |                         0.167 |                    0.235 |                0.084 |                       0.333 |                      0.033 |                 0.166 |
| OC-val q=0.001  |            0.173 |                   0.228 |                  0.11  |             0.197 |                   0.148 |                          0.172 |                         0.188 |                    0.153 |                0.286 |                       0.485 |                      0.103 |                 0.386 |
| OC-val q=0.01   |            0.109 |                   0.127 |                  0.112 |             0.122 |                   0.062 |                          0.074 |                         0.092 |                    0.071 |                0.664 |                       0.697 |                      0.32  |                 0.644 |
| argmax          |            0.141 |                   0.283 |                  0     |             0.061 |                   0.085 |                          0.307 |                         0     |                    0.253 |                0.623 |                       0.41  |                      0     |                 0.038 |
| oracle          |            0.234 |                   0.31  |                  0.047 |             0.082 |                   0.201 |                          0.355 |                         0.066 |                    0.093 |                0.522 |                       0.457 |                      0.162 |                 0.291 | 

## k=100: rare-class F1 / precision / recall (mean over 4 rare classes and seeds)

| rule            |   ('f1', 'CCVR') |   ('f1', 'Central-bal') |   ('f1', 'FedAvg-bal') |   ('f1', 'GB+CR') |   ('precision', 'CCVR') |   ('precision', 'Central-bal') |   ('precision', 'FedAvg-bal') |   ('precision', 'GB+CR') |   ('recall', 'CCVR') |   ('recall', 'Central-bal') |   ('recall', 'FedAvg-bal') |   ('recall', 'GB+CR') |
|:----------------|-----------------:|------------------------:|-----------------------:|------------------:|------------------------:|-------------------------------:|------------------------------:|-------------------------:|---------------------:|----------------------------:|---------------------------:|----------------------:|
| OC-own q=0.0001 |            0.079 |                   0.247 |                  0.034 |             0.147 |                   0.201 |                          0.444 |                         0.138 |                    0.302 |                0.052 |                       0.226 |                      0.02  |                 0.115 |
| OC-own q=0.001  |            0.179 |                   0.297 |                  0.091 |             0.208 |                   0.189 |                          0.274 |                         0.165 |                    0.228 |                0.218 |                       0.435 |                      0.08  |                 0.274 |
| OC-own q=0.01   |            0.177 |                   0.22  |                  0.088 |             0.186 |                   0.113 |                          0.141 |                         0.145 |                    0.125 |                0.584 |                       0.697 |                      0.159 |                 0.539 |
| OC-val q=0.0001 |            0.123 |                   0.308 |                  0.04  |             0.187 |                   0.199 |                          0.353 |                         0.146 |                    0.276 |                0.104 |                       0.374 |                      0.027 |                 0.182 |
| OC-val q=0.001  |            0.215 |                   0.236 |                  0.131 |             0.19  |                   0.166 |                          0.176 |                         0.17  |                    0.156 |                0.389 |                       0.519 |                      0.146 |                 0.376 |
| OC-val q=0.01   |            0.106 |                   0.123 |                  0.131 |             0.113 |                   0.06  |                          0.071 |                         0.092 |                    0.066 |                0.675 |                       0.71  |                      0.412 |                 0.65  |
| argmax          |            0.146 |                   0.358 |                  0     |             0.091 |                   0.086 |                          0.318 |                         0     |                    0.243 |                0.659 |                       0.561 |                      0     |                 0.066 |
| oracle          |            0.265 |                   0.426 |                  0.015 |             0.207 |                   0.215 |                          0.414 |                         0.008 |                    0.232 |                0.606 |                       0.632 |                      0.121 |                 0.354 | 

## Common attack classes F1

|                          |   CCVR |   Central-bal |   FedAvg-bal |   GB+CR |
|:-------------------------|-------:|--------------:|-------------:|--------:|
| (20, 'OC-own q=0.0001')  |  0.478 |         0.53  |        0.485 |   0.486 |
| (20, 'OC-own q=0.001')   |  0.476 |         0.53  |        0.484 |   0.485 |
| (20, 'OC-own q=0.01')    |  0.428 |         0.5   |        0.474 |   0.459 |
| (20, 'OC-val q=0.0001')  |  0.479 |         0.531 |        0.485 |   0.486 |
| (20, 'OC-val q=0.001')   |  0.474 |         0.527 |        0.484 |   0.482 |
| (20, 'OC-val q=0.01')    |  0.398 |         0.445 |        0.47  |   0.425 |
| (20, 'argmax')           |  0.438 |         0.534 |        0.485 |   0.487 |
| (20, 'oracle')           |  0.201 |         0.334 |        0.319 |   0.226 |
| (100, 'OC-own q=0.0001') |  0.489 |         0.532 |        0.488 |   0.491 |
| (100, 'OC-own q=0.001')  |  0.486 |         0.529 |        0.488 |   0.49  |
| (100, 'OC-own q=0.01')   |  0.439 |         0.477 |        0.478 |   0.454 |
| (100, 'OC-val q=0.0001') |  0.489 |         0.533 |        0.488 |   0.491 |
| (100, 'OC-val q=0.001')  |  0.487 |         0.526 |        0.487 |   0.487 |
| (100, 'OC-val q=0.01')   |  0.394 |         0.434 |        0.473 |   0.41  |
| (100, 'argmax')          |  0.445 |         0.532 |        0.488 |   0.491 |
| (100, 'oracle')          |  0.17  |         0.377 |        0.386 |   0.343 | 

## Benign recall

|                          |   CCVR |   Central-bal |   FedAvg-bal |   GB+CR |
|:-------------------------|-------:|--------------:|-------------:|--------:|
| (20, 'OC-own q=0.0001')  | 0.9996 |        0.9997 |       0.9998 |  0.9998 |
| (20, 'OC-own q=0.001')   | 0.9994 |        0.9997 |       0.9998 |  0.9997 |
| (20, 'OC-own q=0.01')    | 0.9975 |        0.9996 |       0.999  |  0.9997 |
| (20, 'OC-val q=0.0001')  | 0.9996 |        0.9997 |       0.9998 |  0.9997 |
| (20, 'OC-val q=0.001')   | 0.9991 |        0.9997 |       0.9997 |  0.9997 |
| (20, 'OC-val q=0.01')    | 0.993  |        0.9993 |       0.9982 |  0.9997 |
| (20, 'argmax')           | 0.995  |        0.9997 |       0.9998 |  0.9998 |
| (20, 'oracle')           | 0.9976 |        0.998  |       0.964  |  0.9997 |
| (100, 'OC-own q=0.0001') | 0.9997 |        0.9997 |       0.9997 |  0.9997 |
| (100, 'OC-own q=0.001')  | 0.9997 |        0.9997 |       0.9997 |  0.9997 |
| (100, 'OC-own q=0.01')   | 0.9941 |        0.9997 |       0.9977 |  0.9997 |
| (100, 'OC-val q=0.0001') | 0.9997 |        0.9997 |       0.9997 |  0.9997 |
| (100, 'OC-val q=0.001')  | 0.9994 |        0.9997 |       0.9996 |  0.9997 |
| (100, 'OC-val q=0.01')   | 0.992  |        0.9997 |       0.9964 |  0.9997 |
| (100, 'argmax')          | 0.993  |        0.9997 |       0.9997 |  0.9997 |
| (100, 'oracle')          | 0.9977 |        0.9996 |       0.9695 |  0.9997 | 

## Paired rare-class F1 differences (x100), 95% CI bootstrap over seeds

- OC-val q=0.0001, k=20: GB+CR+OC - CCVR +1.9 [-0.2, +4.4]; GB+CR+OC - GB+CR +9.9 [+8.2, +12.3]; GB+CR+OC - CCVR+OC +5.7 [+3.9, +7.6]; Central+OC - best FL+OC +11.8 [+8.8, +15.4]; Central argmax - best FL+OC +11.2 [+9.2, +13.3]
- OC-val q=0.0001, k=100: GB+CR+OC - CCVR +4.1 [+1.1, +6.5]; GB+CR+OC - GB+CR +9.6 [+7.0, +12.3]; GB+CR+OC - CCVR+OC +6.4 [+2.8, +9.2]; Central+OC - best FL+OC +9.0 [+7.2, +11.1]; Central argmax - best FL+OC +14.0 [+11.1, +17.1]
- OC-val q=0.001, k=20: GB+CR+OC - CCVR +5.5 [+3.7, +7.1]; GB+CR+OC - GB+CR +13.6 [+11.8, +15.3]; GB+CR+OC - CCVR+OC +2.4 [+0.9, +4.3]; Central+OC - best FL+OC +1.3 [-1.4, +3.4]; Central argmax - best FL+OC +6.8 [+6.0, +7.8]
- OC-val q=0.001, k=100: GB+CR+OC - CCVR +4.5 [+2.5, +6.5]; GB+CR+OC - GB+CR +9.9 [+6.6, +13.6]; GB+CR+OC - CCVR+OC -2.5 [-7.6, +2.2]; Central+OC - best FL+OC -1.3 [-3.5, +1.2]; Central argmax - best FL+OC +10.9 [+9.0, +13.0]
- OC-val q=0.01, k=20: GB+CR+OC - CCVR -2.0 [-2.8, -1.1]; GB+CR+OC - GB+CR +6.1 [+2.5, +8.8]; GB+CR+OC - CCVR+OC +1.2 [+0.7, +1.7]; Central+OC - best FL+OC -1.2 [-2.6, +0.1]; Central argmax - best FL+OC +14.4 [+11.6, +16.7]
- OC-val q=0.01, k=100: GB+CR+OC - CCVR -3.3 [-4.5, -1.9]; GB+CR+OC - GB+CR +2.2 [-2.1, +5.6]; GB+CR+OC - CCVR+OC +0.7 [+0.1, +1.4]; Central+OC - best FL+OC -3.5 [-4.0, -3.1]; Central argmax - best FL+OC +20.0 [+19.1, +20.8]

Note: the 'oracle' rows are NOT a valid upper bound (per-class thresholds searched independently, then they conflict in the joint decision and the search grid is coarse); ignore them.

## Interpretation (development, not sealed; q chosen post hoc, so must be fixed before sealing)

- Step 4 works as a fix: GB+CR+OC (q=1e-3, val calibration) rare F1 0.197 / 0.190 (k=20/100) vs GB+CR argmax 0.061 / 0.091 and CCVR 0.141 / 0.146; differences vs CCVR +5.5 [+3.7,+7.1] and +4.5 [+2.5,+6.5]. Common-class F1 and benign recall unchanged at q <= 1e-3.
- It is model-agnostic: it also lifts CCVR (CCVR+OC 0.173 / 0.215). GB+CR+OC vs CCVR+OC: +2.4 [+0.9,+4.3] at k=20, -2.5 [-7.6,+2.2] at k=100. So the GB+CR base adds little once OC is applied.
- Gap to centralised training (its best rule, argmax) shrinks from ~14-16 to +6.8 [+6.0,+7.8] (k=20) and +10.9 [+9.0,+13.0] (k=100) points; still above 0.
- Rare precision after OC stays ~0.15-0.17 (about 5-6 false alarms per true detection).
- Calibrating on the owner's in-sample training flows ('OC-own') is similar at q=1e-3 (0.191/0.208); at other q it differs.
- Novelty caution: thresholding a one-vs-rest score at a target false-alarm rate on benign traffic is standard practice in IDS; the federated twist (owner-only calibration, server gets only the threshold) is modest.
