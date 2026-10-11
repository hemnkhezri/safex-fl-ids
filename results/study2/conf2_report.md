# Confirmatory results, plan v2 (SAFE-X)

Units per (ds, k): {('ton', 5): 10, ('ton', 20): 10, ('ton', 100): 10, ('unsw', 5): 10, ('unsw', 20): 10, ('unsw', 100): 10} 

## Rare-class F1 (seed means)

|                                           |     5 |    20 |   100 |
|:------------------------------------------|------:|------:|------:|
| ('ton', 'CCVR argmax')                    | 0.518 | 0.524 | 0.574 |
| ('ton', 'CCVR+OC')                        | 0.581 | 0.649 | 0.683 |
| ('ton', 'Central-bal argmax')             | 0.584 | 0.819 | 0.829 |
| ('ton', 'Central-bal+OC')                 | 0.573 | 0.713 | 0.718 |
| ('ton', 'Experts[own] + GB+CR')           | 0.544 | 0.681 | 0.638 |
| ('ton', 'FedOV argmax')                   | 0.098 | 0.189 | 0.175 |
| ('ton', 'FedOV+OC')                       | 0.592 | 0.676 | 0.582 |
| ('ton', 'FedProx-bal argmax')             | 0.165 | 0.137 | 0.304 |
| ('ton', 'FedProx-bal+OC')                 | 0.365 | 0.395 | 0.487 |
| ('ton', 'GB+CR argmax')                   | 0.308 | 0.388 | 0.381 |
| ('ton', 'GB+CR+OC')                       | 0.417 | 0.415 | 0.436 |
| ('ton', 'PROTEAN argmax')                 | 0.365 | 0.318 | 0.338 |
| ('ton', 'PROTEAN+OC')                     | 0.319 | 0.272 | 0.251 |
| ('ton', 'SAFE-X (Experts[fed] + GB+CR)')  | 0.573 | 0.687 | 0.705 |
| ('unsw', 'CCVR argmax')                   | 0.122 | 0.145 | 0.141 |
| ('unsw', 'CCVR+OC')                       | 0.126 | 0.187 | 0.184 |
| ('unsw', 'Central-bal argmax')            | 0.191 | 0.293 | 0.338 |
| ('unsw', 'Central-bal+OC')                | 0.182 | 0.229 | 0.233 |
| ('unsw', 'Experts[own] + GB+CR')          | 0.163 | 0.209 | 0.256 |
| ('unsw', 'FedOV argmax')                  | 0     | 0     | 0     |
| ('unsw', 'FedOV+OC')                      | 0.173 | 0.222 | 0.233 |
| ('unsw', 'FedProx-bal argmax')            | 0.026 | 0.046 | 0.029 |
| ('unsw', 'FedProx-bal+OC')                | 0.164 | 0.176 | 0.2   |
| ('unsw', 'GB+CR argmax')                  | 0.083 | 0.085 | 0.089 |
| ('unsw', 'GB+CR+OC')                      | 0.171 | 0.18  | 0.164 |
| ('unsw', 'PROTEAN argmax')                | 0.086 | 0.096 | 0.072 |
| ('unsw', 'PROTEAN+OC')                    | 0.064 | 0.099 | 0.071 |
| ('unsw', 'SAFE-X (Experts[fed] + GB+CR)') | 0.195 | 0.256 | 0.282 | 

Owner alone (own class): {('ton', 5): 0.592, ('ton', 20): 0.735, ('ton', 100): 0.63, ('unsw', 5): 0.232, ('unsw', 20): 0.256, ('unsw', 100): 0.237} 

## M1: SAFE-X - FedOV+OC (rare F1 x100, pooled over k)

- ton: +3.8 [-0.6, +7.7] -> NOT supported
- unsw: +3.5 [+2.5, +4.3] -> SUPPORTED

**M1 main claim (both datasets): NOT supported**

## M2: SAFE-X - best baseline per (dataset, k)

- ton k=5: best baseline FedOV+OC (0.592); SAFE-X 0.573; diff -1.9 [-6.5, +2.5]
- ton k=20: best baseline FedOV+OC (0.676); SAFE-X 0.687; diff +1.1 [-4.6, +8.2]
- ton k=100: best baseline CCVR+OC (0.683); SAFE-X 0.705; diff +2.1 [-2.5, +6.3]
- unsw k=5: best baseline FedOV+OC (0.173); SAFE-X 0.195; diff +2.2 [-0.3, +4.1]
- unsw k=20: best baseline FedOV+OC (0.222); SAFE-X 0.256; diff +3.4 [+1.4, +5.3] (claimed)
- unsw k=100: best baseline FedOV+OC (0.233); SAFE-X 0.282; diff +4.9 [+3.4, +6.3] (claimed)

## M3: false-alarm rate of shared experts on non-rare test flows (target 0.001)

- ton: owner-only 0.0060 (worst 0.0718); federated 0.0026 (worst 0.0115); owner-only - federated +3.3 [+2.2, +4.6] per mille -> SUPPORTED
- unsw: owner-only 0.0036 (worst 0.0461); federated 0.0015 (worst 0.0034); owner-only - federated +2.1 [+1.4, +3.0] per mille -> SUPPORTED

## M4: no harm vs GB+CR argmax (benign recall >= -0.002, common F1 >= -1 pt)

- ton k=5: benign recall -0.0083; common F1 +0.33 pts -> FAIL
- ton k=20: benign recall -0.0066; common F1 +0.23 pts -> FAIL
- ton k=100: benign recall -0.0091; common F1 +0.20 pts -> FAIL
- unsw k=5: benign recall -0.0000; common F1 -0.11 pts -> pass
- unsw k=20: benign recall -0.0000; common F1 -0.00 pts -> pass
- unsw k=100: benign recall -0.0004; common F1 -0.03 pts -> pass

## M5 (descriptive): SAFE-X vs Owner alone and Central-bal (rare F1)

- ton k=5: SAFE-X 0.573; owner alone 0.592; Central-bal 0.584; ablation owner-only calibration 0.544
- ton k=20: SAFE-X 0.687; owner alone 0.735; Central-bal 0.819; ablation owner-only calibration 0.681
- ton k=100: SAFE-X 0.705; owner alone 0.630; Central-bal 0.829; ablation owner-only calibration 0.638
- unsw k=5: SAFE-X 0.195; owner alone 0.232; Central-bal 0.191; ablation owner-only calibration 0.163
- unsw k=20: SAFE-X 0.256; owner alone 0.256; Central-bal 0.293; ablation owner-only calibration 0.209
- unsw k=100: SAFE-X 0.282; owner alone 0.237; Central-bal 0.338; ablation owner-only calibration 0.256
