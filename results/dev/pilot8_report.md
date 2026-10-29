# Pilot 8: Study 5 candidates (development seeds 0-4, k = 20, K = 10; exploratory, no claims)

Seeds per dataset: {'cic': 5, 'ton': 5, 'unsw': 5} 

## Seed means (FA = expert alarm rate on non-rare test flows; target 0.001)

|                                  |   rare_f1 |   rare_p |   rare_r |       fa |   fa_benign |   fa_common |   fa_2nd_half |   benign_recall |   d_common_f1 |
|:---------------------------------|----------:|---------:|---------:|---------:|------------:|------------:|--------------:|----------------:|--------------:|
| ('cic', 'FedOV+OC')              |    0.1926 |   0.352  |   0.3693 |   0.0035 |      0.0004 |      0.0062 |        0.0012 |          0.9984 |       -0.0015 |
| ('cic', 'FedOV+OC ACI 0.005')    |    0.258  |   0.2505 |   0.276  |   0.001  |      0.001  |      0.001  |        0.001  |          0.9966 |        0.001  |
| ('cic', 'FedOV+OC ACI 0.02')     |    0.1799 |   0.1954 |   0.1744 |   0.001  |      0.001  |      0.001  |        0.001  |          0.9965 |        0.0006 |
| ('cic', 'FedOV+OC ACI 0.05')     |    0.1612 |   0.1795 |   0.1538 |   0.001  |      0.001  |      0.001  |        0.001  |          0.9965 |        0.0004 |
| ('cic', 'Owner alone (frozen)')  |    0.2556 | nan      | nan      | nan      |    nan      |    nan      |      nan      |        nan      |      nan      |
| ('cic', 'Owner alone (plain)')   |    0.3136 | nan      | nan      | nan      |    nan      |    nan      |      nan      |        nan      |      nan      |
| ('cic', 'SAFE-X')                |    0.2428 |   0.2191 |   0.4495 |   0.0103 |      0.0015 |      0.0177 |        0.0061 |          0.9945 |       -0.0236 |
| ('cic', 'SAFE-X ACI 0.005')      |    0.2521 |   0.2373 |   0.3153 |   0.001  |      0.001  |      0.001  |        0.001  |          0.9962 |       -0.0005 |
| ('cic', 'SAFE-X ACI 0.02')       |    0.1783 |   0.1911 |   0.1813 |   0.001  |      0.001  |      0.001  |        0.001  |          0.9962 |       -0.0006 |
| ('cic', 'SAFE-X ACI 0.05')       |    0.1684 |   0.1838 |   0.1726 |   0.001  |      0.001  |      0.001  |        0.001  |          0.9963 |       -0.0008 |
| ('cic', 'SAFE-X frozen')         |    0.2913 |   0.2493 |   0.4692 |   0.0035 |      0.0014 |      0.0053 |        0.002  |          0.9955 |        0.0003 |
| ('cic', 'SAFE-X per-group')      |    0.2535 |   0.2547 |   0.4304 |   0.0076 |      0.001  |      0.0132 |        0.0043 |          0.996  |       -0.0175 |
| ('ton', 'FedOV+OC')              |    0.6564 |   0.6395 |   0.7749 |   0.0048 |      0.0049 |      0.0047 |        0.0036 |          0.9106 |        0.0029 |
| ('ton', 'FedOV+OC ACI 0.005')    |    0.6017 |   0.6814 |   0.5718 |   0.001  |      0.0011 |      0.001  |        0.001  |          0.9194 |        0.0047 |
| ('ton', 'FedOV+OC ACI 0.02')     |    0.6044 |   0.6846 |   0.5624 |   0.0011 |      0.0011 |      0.001  |        0.0011 |          0.919  |        0.0039 |
| ('ton', 'FedOV+OC ACI 0.05')     |    0.5932 |   0.7017 |   0.5388 |   0.001  |      0.0011 |      0.001  |        0.001  |          0.9188 |        0.0028 |
| ('ton', 'Owner alone (frozen)')  |    0.6735 | nan      | nan      | nan      |    nan      |    nan      |      nan      |        nan      |      nan      |
| ('ton', 'Owner alone (plain)')   |    0.7436 | nan      | nan      | nan      |    nan      |    nan      |      nan      |        nan      |      nan      |
| ('ton', 'SAFE-X')                |    0.6686 |   0.7053 |   0.6919 |   0.0022 |      0.0031 |      0.0014 |        0.0023 |          0.9161 |        0.008  |
| ('ton', 'SAFE-X ACI 0.005')      |    0.6122 |   0.6695 |   0.592  |   0.001  |      0.0011 |      0.001  |        0.001  |          0.9199 |        0.0135 |
| ('ton', 'SAFE-X ACI 0.02')       |    0.6172 |   0.6899 |   0.5814 |   0.0011 |      0.0011 |      0.001  |        0.001  |          0.9196 |        0.0119 |
| ('ton', 'SAFE-X ACI 0.05')       |    0.5983 |   0.6891 |   0.5553 |   0.0011 |      0.0011 |      0.001  |        0.001  |          0.9192 |        0.0108 |
| ('ton', 'SAFE-X frozen')         |    0.6215 |   0.6506 |   0.6877 |   0.0025 |      0.0037 |      0.0016 |        0.0027 |          0.9139 |        0.0101 |
| ('ton', 'SAFE-X per-group')      |    0.6719 |   0.7258 |   0.6796 |   0.0019 |      0.0029 |      0.0011 |        0.0021 |          0.9165 |        0.0092 |
| ('unsw', 'FedOV+OC')             |    0.2257 |   0.1691 |   0.4803 |   0.0047 |      0      |      0.0211 |        0.005  |          0.9997 |       -0.0005 |
| ('unsw', 'FedOV+OC ACI 0.005')   |    0.1924 |   0.2962 |   0.1816 |   0.0009 |      0      |      0.0041 |        0.0009 |          0.9996 |        0.0035 |
| ('unsw', 'FedOV+OC ACI 0.02')    |    0.1756 |   0.3133 |   0.1453 |   0.0009 |      0      |      0.0041 |        0.0009 |          0.9996 |        0.0037 |
| ('unsw', 'FedOV+OC ACI 0.05')    |    0.1694 |   0.2998 |   0.1357 |   0.0009 |      0      |      0.0041 |        0.0009 |          0.9996 |        0.0036 |
| ('unsw', 'Owner alone (frozen)') |    0.2592 | nan      | nan      | nan      |    nan      |    nan      |      nan      |        nan      |      nan      |
| ('unsw', 'Owner alone (plain)')  |    0.2692 | nan      | nan      | nan      |    nan      |    nan      |      nan      |        nan      |      nan      |
| ('unsw', 'SAFE-X')               |    0.2521 |   0.2474 |   0.3475 |   0.0017 |      0      |      0.0077 |        0.0019 |          0.9998 |        0.0014 |
| ('unsw', 'SAFE-X ACI 0.005')     |    0.2438 |   0.3112 |   0.2638 |   0.0009 |      0      |      0.0041 |        0.0009 |          0.9997 |       -0.0003 |
| ('unsw', 'SAFE-X ACI 0.02')      |    0.1928 |   0.2953 |   0.1887 |   0.0009 |      0      |      0.0042 |        0.0009 |          0.9998 |       -0.0009 |
| ('unsw', 'SAFE-X ACI 0.05')      |    0.1865 |   0.3159 |   0.1612 |   0.0009 |      0      |      0.0041 |        0.0009 |          0.9997 |       -0.0009 |
| ('unsw', 'SAFE-X frozen')        |    0.2166 |   0.2369 |   0.2872 |   0.0015 |      0      |      0.0068 |        0.0015 |          0.9997 |        0.0013 |
| ('unsw', 'SAFE-X per-group')     |    0.2373 |   0.3501 |   0.2139 |   0.0005 |      0      |      0.0023 |        0.0006 |          0.9998 |        0.0018 | 

## Paired differences in rare F1 (points, bootstrap over seeds)

- cic: SAFE-X ACI 0.005 - SAFE-X +0.9 [-3.2, +4.9]; SAFE-X ACI 0.005 - FedOV+OC +6.0 [+3.9, +8.0]
- cic: SAFE-X ACI 0.02 - SAFE-X -6.5 [-11.0, -1.9]; SAFE-X ACI 0.02 - FedOV+OC -1.4 [-4.0, +1.2]
- cic: SAFE-X ACI 0.05 - SAFE-X -7.4 [-12.0, -2.9]; SAFE-X ACI 0.05 - FedOV+OC -2.4 [-5.0, +0.2]
- cic: SAFE-X frozen - SAFE-X +4.9 [-1.7, +11.5]; SAFE-X frozen - FedOV+OC +9.9 [+3.6, +15.8]
- cic: SAFE-X per-group - SAFE-X +1.1 [+0.4, +1.8]; SAFE-X per-group - FedOV+OC +6.1 [+3.0, +8.8]
- cic: SAFE-X - FedOV+OC +5.0 [+2.3, +7.7]
- cic: SAFE-X ACI 0.005 - FedOV+OC ACI 0.005 -0.6 [-3.9, +1.9]
- cic: SAFE-X ACI 0.02 - FedOV+OC ACI 0.02 -0.2 [-2.5, +2.1]
- cic: SAFE-X ACI 0.05 - FedOV+OC ACI 0.05 +0.7 [-0.1, +2.3]
- ton: SAFE-X ACI 0.005 - SAFE-X -5.6 [-16.0, +7.0]; SAFE-X ACI 0.005 - FedOV+OC -4.4 [-8.1, -0.5]
- ton: SAFE-X ACI 0.02 - SAFE-X -5.1 [-12.3, +5.5]; SAFE-X ACI 0.02 - FedOV+OC -3.9 [-9.3, +1.5]
- ton: SAFE-X ACI 0.05 - SAFE-X -7.0 [-15.6, +5.0]; SAFE-X ACI 0.05 - FedOV+OC -5.8 [-12.7, +0.1]
- ton: SAFE-X frozen - SAFE-X -4.7 [-11.4, +1.8]; SAFE-X frozen - FedOV+OC -3.5 [-14.2, +5.2]
- ton: SAFE-X per-group - SAFE-X +0.3 [-1.2, +2.2]; SAFE-X per-group - FedOV+OC +1.5 [-13.7, +13.9]
- ton: SAFE-X - FedOV+OC +1.2 [-13.6, +12.0]
- ton: SAFE-X ACI 0.005 - FedOV+OC ACI 0.005 +1.0 [-2.8, +4.7]
- ton: SAFE-X ACI 0.02 - FedOV+OC ACI 0.02 +1.3 [-2.8, +6.8]
- ton: SAFE-X ACI 0.05 - FedOV+OC ACI 0.05 +0.5 [-7.0, +7.1]
- unsw: SAFE-X ACI 0.005 - SAFE-X -0.8 [-2.6, +0.8]; SAFE-X ACI 0.005 - FedOV+OC +1.8 [-1.2, +4.8]
- unsw: SAFE-X ACI 0.02 - SAFE-X -5.9 [-7.9, -4.3]; SAFE-X ACI 0.02 - FedOV+OC -3.3 [-5.8, -1.1]
- unsw: SAFE-X ACI 0.05 - SAFE-X -6.6 [-9.5, -3.1]; SAFE-X ACI 0.05 - FedOV+OC -3.9 [-7.1, -1.2]
- unsw: SAFE-X frozen - SAFE-X -3.6 [-6.3, -0.8]; SAFE-X frozen - FedOV+OC -0.9 [-3.2, +1.4]
- unsw: SAFE-X per-group - SAFE-X -1.5 [-3.6, +0.6]; SAFE-X per-group - FedOV+OC +1.2 [-1.3, +4.4]
- unsw: SAFE-X - FedOV+OC +2.6 [+0.6, +4.7]
- unsw: SAFE-X ACI 0.005 - FedOV+OC ACI 0.005 +5.1 [+2.2, +7.4]
- unsw: SAFE-X ACI 0.02 - FedOV+OC ACI 0.02 +1.7 [-0.7, +3.8]
- unsw: SAFE-X ACI 0.05 - FedOV+OC ACI 0.05 +1.7 [-1.8, +4.8]
