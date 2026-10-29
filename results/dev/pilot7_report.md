# Pilot 7: SAFE-X extensions (development seeds 0-4, k = 20, K = 10; exploratory, no claims)

Seeds per dataset: {'ton': 5, 'unsw': 5} 

Cascade gate (GB+CR p_benign < 0.5): share of rare test flows passing {'ton': 0.643, 'unsw': 0.982} ; share of calibration negatives passing {'ton': 0.377, 'unsw': 0.285} 

## Rare-class precision / recall / F1 (seed means)

|                                |   precision |   recall |    f1 |
|:-------------------------------|------------:|---------:|------:|
| ('ton', 'FedOV+OC')            |       0.618 |    0.801 | 0.651 |
| ('ton', 'FedOV-full+OC')       |       0.63  |    0.809 | 0.661 |
| ('ton', 'GB+CR argmax')        |       0     |    0     | 0     |
| ('ton', 'SAFE-X')              |       0.709 |    0.781 | 0.714 |
| ('ton', 'SAFE-X (full cal.)')  |       0.712 |    0.782 | 0.717 |
| ('ton', 'SAFE-X+NR')           |       0.717 |    0.758 | 0.706 |
| ('ton', 'SAFE-X+NR+cascade')   |       0.645 |    0.562 | 0.551 |
| ('ton', 'SAFE-X+cascade')      |       0.645 |    0.561 | 0.548 |
| ('unsw', 'FedOV+OC')           |       0.167 |    0.481 | 0.224 |
| ('unsw', 'FedOV-full+OC')      |       0.18  |    0.475 | 0.227 |
| ('unsw', 'GB+CR argmax')       |       0     |    0     | 0     |
| ('unsw', 'SAFE-X')             |       0.285 |    0.333 | 0.269 |
| ('unsw', 'SAFE-X (full cal.)') |       0.282 |    0.334 | 0.269 |
| ('unsw', 'SAFE-X+NR')          |       0.279 |    0.357 | 0.285 |
| ('unsw', 'SAFE-X+NR+cascade')  |       0.272 |    0.342 | 0.273 |
| ('unsw', 'SAFE-X+cascade')     |       0.279 |    0.322 | 0.26  | 

## Common-attack F1 minus GB+CR argmax

| method             |   ton |   unsw |
|:-------------------|------:|-------:|
| FedOV+OC           | 0.007 | -0.017 |
| FedOV-full+OC      | 0.007 | -0.019 |
| GB+CR argmax       | 0     |  0     |
| SAFE-X             | 0.012 | -0     |
| SAFE-X (full cal.) | 0.012 | -0     |
| SAFE-X+NR          | 0.012 | -0     |
| SAFE-X+NR+cascade  | 0.009 | -0     |
| SAFE-X+cascade     | 0.01  | -0     | 

## Expert false-alarm rate on non-rare test flows (target q = 0.001), mean over rare classes

|                                |     fa |   fa_benign |   recall_expert |
|:-------------------------------|-------:|------------:|----------------:|
| ('ton', 'SAFE-X')              | 0.0022 |      0.0033 |          0.7862 |
| ('ton', 'SAFE-X (full cal.)')  | 0.0022 |      0.0032 |          0.7879 |
| ('ton', 'SAFE-X+NR')           | 0.0026 |      0.0034 |          0.7605 |
| ('ton', 'SAFE-X+NR+cascade')   | 0.0024 |      0.0022 |          0.5641 |
| ('ton', 'SAFE-X+cascade')      | 0.0022 |      0.002  |          0.5654 |
| ('unsw', 'SAFE-X')             | 0.0013 |      0      |          0.3328 |
| ('unsw', 'SAFE-X (full cal.)') | 0.0014 |      0      |          0.3342 |
| ('unsw', 'SAFE-X+NR')          | 0.0014 |      0      |          0.3583 |
| ('unsw', 'SAFE-X+NR+cascade')  | 0.0014 |      0      |          0.3443 |
| ('unsw', 'SAFE-X+cascade')     | 0.0013 |      0      |          0.3225 | 

Per class:

|                       |   SAFE-X |   SAFE-X (full cal.) |   SAFE-X+NR |   SAFE-X+NR+cascade |   SAFE-X+cascade |
|:----------------------|---------:|---------------------:|------------:|--------------------:|-----------------:|
| ('ton', 'Backdoor')   |   0.0011 |               0.0011 |      0.0011 |              0.0006 |           0.0008 |
| ('ton', 'dos')        |   0.002  |               0.002  |      0.0022 |              0.0034 |           0.0026 |
| ('ton', 'mitm')       |   0.0029 |               0.0029 |      0.0034 |              0.0022 |           0.0026 |
| ('ton', 'ransomware') |   0.003  |               0.003  |      0.0036 |              0.0033 |           0.0027 |
| ('unsw', 'Analysis')  |   0.0022 |               0.0023 |      0.0023 |              0.0022 |           0.0022 |
| ('unsw', 'Backdoor')  |   0.001  |               0.001  |      0.0012 |              0.0013 |           0.001  |
| ('unsw', 'Shellcode') |   0.0012 |               0.0013 |      0.0013 |              0.0014 |           0.0013 |
| ('unsw', 'Worms')     |   0.0008 |               0.0008 |      0.0008 |              0.0008 |           0.0008 | 

## Paired differences in rare F1 (points, bootstrap over seeds)

- ton: SAFE-X+NR - SAFE-X -0.8 [-2.6, +1.5]; SAFE-X+NR - FedOV-full+OC +4.5 [-4.1, +11.8]
- ton: SAFE-X+cascade - SAFE-X -16.5 [-20.0, -13.8]; SAFE-X+cascade - FedOV-full+OC -11.2 [-18.7, -3.8]
- ton: SAFE-X+NR+cascade - SAFE-X -16.3 [-19.6, -13.7]; SAFE-X+NR+cascade - FedOV-full+OC -11.0 [-18.2, -3.8]
- ton: SAFE-X - FedOV-full+OC +5.3 [-2.7, +12.7]
- unsw: SAFE-X+NR - SAFE-X +1.5 [-0.8, +4.2]; SAFE-X+NR - FedOV-full+OC +5.7 [+4.6, +7.0]
- unsw: SAFE-X+cascade - SAFE-X -0.9 [-1.8, -0.0]; SAFE-X+cascade - FedOV-full+OC +3.3 [+0.4, +5.1]
- unsw: SAFE-X+NR+cascade - SAFE-X +0.4 [-2.5, +3.4]; SAFE-X+NR+cascade - FedOV-full+OC +4.6 [+3.2, +6.0]
- unsw: SAFE-X - FedOV-full+OC +4.2 [+0.7, +6.3]
