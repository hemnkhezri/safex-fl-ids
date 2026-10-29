# Pilot 9: SAFE-X with a federated feedback loop (development seeds 0-4, k = 20, K = 10, ACI gamma = 0.005; exploratory, no claims)

Seeds per dataset: {'cic': 5, 'ton': 5, 'unsw': 5} 

## Seed means

|                          |   rare_f1 |   rare_p |   rare_r |   rare_f1_2nd_half |     fa |   fa_2nd_half |   d_common_f1 |   alarms_labelled |
|:-------------------------|----------:|---------:|---------:|-------------------:|-------:|--------------:|--------------:|------------------:|
| ('cic', 'FedOV+OC ACI')  |    0.258  |   0.2505 |   0.276  |             0.0875 | 0.001  |        0.001  |        0      |            1245   |
| ('cic', 'loop')          |    0.2395 |   0.2386 |   0.2464 |             0.0591 | 0.001  |        0.001  |       -0.0004 |            1167.2 |
| ('cic', 'loopneg')       |    0.2416 |   0.2415 |   0.2467 |             0.0624 | 0.001  |        0.001  |       -0.0004 |            1149.8 |
| ('cic', 'static')        |    0.2353 |   0.2207 |   0.2984 |             0.0682 | 0.001  |        0.001  |       -0.0005 |            1287.4 |
| ('ton', 'FedOV+OC ACI')  |    0.6017 |   0.6814 |   0.5718 |             0.3845 | 0.001  |        0.001  |        0.0142 |           26566.4 |
| ('ton', 'loop')          |    0.5968 |   0.6753 |   0.5682 |             0.3664 | 0.001  |        0.001  |        0.0128 |           27982.6 |
| ('ton', 'loopneg')       |    0.5867 |   0.6733 |   0.551  |             0.3643 | 0.001  |        0.001  |        0.0124 |           26744.2 |
| ('ton', 'static')        |    0.5991 |   0.6639 |   0.5739 |             0.3716 | 0.001  |        0.001  |        0.0133 |           27888.8 |
| ('unsw', 'FedOV+OC ACI') |    0.1924 |   0.2962 |   0.1816 |             0.186  | 0.0009 |        0.0009 |       -0.0015 |             803.2 |
| ('unsw', 'loop')         |    0.2377 |   0.3116 |   0.2562 |             0.2265 | 0.0009 |        0.0009 |       -0      |             855.6 |
| ('unsw', 'loopneg')      |    0.2194 |   0.2943 |   0.2361 |             0.1989 | 0.0009 |        0.0009 |       -0.0004 |             819.8 |
| ('unsw', 'static')       |    0.2345 |   0.3    |   0.2539 |             0.2165 | 0.0009 |        0.0009 |       -0.0003 |             870.6 | 

## Paired differences (F1 points, bootstrap over seeds)

- cic rare_f1: loop - static +0.4 [-2.0, +3.3]; loopneg - static +0.6 [-1.9, +3.6]; loop - FedOV+OC ACI -1.8 [-5.1, +1.6]; static - FedOV+OC ACI -2.3 [-5.1, +0.6]
- ton rare_f1: loop - static -0.2 [-1.0, +0.6]; loopneg - static -1.2 [-2.2, -0.2]; loop - FedOV+OC ACI -0.5 [-4.1, +3.1]; static - FedOV+OC ACI -0.3 [-3.1, +2.6]
- unsw rare_f1: loop - static +0.3 [-0.6, +1.1]; loopneg - static -1.5 [-2.3, -0.8]; loop - FedOV+OC ACI +4.5 [+2.8, +6.5]; static - FedOV+OC ACI +4.2 [+2.4, +6.1]
- cic rare_f1_2nd_half: loop - static -0.9 [-3.9, +3.0]; loopneg - static -0.6 [-3.8, +3.2]; loop - FedOV+OC ACI -2.8 [-6.3, +1.0]; static - FedOV+OC ACI -1.9 [-4.6, +1.0]
- ton rare_f1_2nd_half: loop - static -0.5 [-1.3, +0.2]; loopneg - static -0.7 [-1.8, +0.1]; loop - FedOV+OC ACI -1.8 [-5.7, +1.7]; static - FedOV+OC ACI -1.3 [-4.1, +1.6]
- unsw rare_f1_2nd_half: loop - static +1.0 [-0.9, +2.9]; loopneg - static -1.8 [-3.3, -0.0]; loop - FedOV+OC ACI +4.0 [+1.3, +6.5]; static - FedOV+OC ACI +3.0 [+0.3, +5.7]
