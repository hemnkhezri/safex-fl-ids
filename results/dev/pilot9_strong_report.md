# Pilot 9: SAFE-X with a federated feedback loop (development seeds 0-4, k = 20, K = 10, ACI gamma = 0.005; exploratory, no claims)

Seeds per dataset: {'cic': 5, 'ton': 5, 'unsw': 5} 

## Seed means

|                          |   rare_f1 |   rare_p |   rare_r |   rare_f1_2nd_half |     fa |   fa_2nd_half |   d_common_f1 |   alarms_labelled |
|:-------------------------|----------:|---------:|---------:|-------------------:|-------:|--------------:|--------------:|------------------:|
| ('cic', 'FedOV+OC ACI')  |    0.258  |   0.2505 |   0.276  |             0.0875 | 0.001  |        0.001  |        0      |            1245   |
| ('cic', 'loop')          |    0.2273 |   0.2317 |   0.2335 |             0.0491 | 0.001  |        0.001  |       -0.0003 |            1124.2 |
| ('cic', 'loopneg')       |    0.2328 |   0.2408 |   0.2379 |             0.0567 | 0.001  |        0.001  |       -0.0003 |            1069.2 |
| ('cic', 'static')        |    0.2353 |   0.2207 |   0.2984 |             0.0682 | 0.001  |        0.001  |       -0.0005 |            1287.4 |
| ('ton', 'FedOV+OC ACI')  |    0.6017 |   0.6814 |   0.5718 |             0.3845 | 0.001  |        0.001  |        0.0142 |           26566.4 |
| ('ton', 'loop')          |    0.5653 |   0.6364 |   0.5388 |             0.3286 | 0.001  |        0.001  |        0.0127 |           28423.6 |
| ('ton', 'loopneg')       |    0.505  |   0.5863 |   0.4692 |             0.2744 | 0.001  |        0.001  |        0.0111 |           26207.6 |
| ('ton', 'static')        |    0.5991 |   0.6639 |   0.5739 |             0.3716 | 0.001  |        0.001  |        0.0133 |           27888.8 |
| ('unsw', 'FedOV+OC ACI') |    0.1924 |   0.2962 |   0.1816 |             0.186  | 0.0009 |        0.0009 |       -0.0015 |             803.2 |
| ('unsw', 'loop')         |    0.2286 |   0.3015 |   0.2434 |             0.2269 | 0.0009 |        0.0009 |       -0.0003 |             837.2 |
| ('unsw', 'loopneg')      |    0.1505 |   0.2379 |   0.1464 |             0.0944 | 0.0009 |        0.0009 |       -0.0011 |             661.4 |
| ('unsw', 'static')       |    0.2345 |   0.3    |   0.2539 |             0.2165 | 0.0009 |        0.0009 |       -0.0003 |             870.6 | 

## Paired differences (F1 points, bootstrap over seeds)

- cic rare_f1: loop - static -0.8 [-6.6, +3.8]; loopneg - static -0.3 [-5.9, +4.3]; loop - FedOV+OC ACI -3.1 [-5.9, +0.2]; static - FedOV+OC ACI -2.3 [-5.1, +0.6]
- ton rare_f1: loop - static -3.4 [-8.0, +3.3]; loopneg - static -9.4 [-16.0, -2.7]; loop - FedOV+OC ACI -3.6 [-9.6, +4.2]; static - FedOV+OC ACI -0.3 [-3.1, +2.6]
- unsw rare_f1: loop - static -0.6 [-2.2, +0.8]; loopneg - static -8.4 [-10.3, -6.4]; loop - FedOV+OC ACI +3.6 [+1.5, +5.7]; static - FedOV+OC ACI +4.2 [+2.4, +6.1]
- cic rare_f1_2nd_half: loop - static -1.9 [-8.6, +3.7]; loopneg - static -1.1 [-8.4, +4.6]; loop - FedOV+OC ACI -3.8 [-7.3, -0.2]; static - FedOV+OC ACI -1.9 [-4.6, +1.0]
- ton rare_f1_2nd_half: loop - static -4.3 [-8.8, +2.1]; loopneg - static -9.7 [-16.5, -2.8]; loop - FedOV+OC ACI -5.6 [-10.6, +1.0]; static - FedOV+OC ACI -1.3 [-4.1, +1.6]
- unsw rare_f1_2nd_half: loop - static +1.0 [-1.2, +3.5]; loopneg - static -12.2 [-14.0, -10.2]; loop - FedOV+OC ACI +4.1 [+1.2, +6.3]; static - FedOV+OC ACI +3.0 [+0.3, +5.7]
