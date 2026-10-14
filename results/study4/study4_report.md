# Study 4 results (plan v4)

Units: {('cic', 'K20'): 10, ('cic', 'K50'): 10, ('cic', 'own2'): 10, ('cic', 'own3'): 10, ('ton', 'K20'): 10, ('ton', 'K50'): 10, ('ton', 'own2'): 10, ('ton', 'own3'): 10, ('unsw', 'K20'): 10, ('unsw', 'K50'): 10, ('unsw', 'own2'): 10, ('unsw', 'own3'): 10} 

## K20: rare-class F1 (seed means, k = 20)

| method                 |   cic |   ton |   unsw |
|:-----------------------|------:|------:|-------:|
| CCVR argmax            | 0.184 | 0.549 |  0.131 |
| CCVR+OC                | 0.209 | 0.669 |  0.157 |
| Central-bal argmax     | 0.343 | 0.813 |  0.31  |
| Central-bal+OC         | 0.266 | 0.715 |  0.218 |
| FedOV argmax           | 0.169 | 0.111 |  0     |
| FedOV+OC               | 0.158 | 0.676 |  0.212 |
| FedOV-full argmax      | 0.138 | 0.008 |  0     |
| FedOV-full+OC          | 0.162 | 0.684 |  0.219 |
| FedProx-bal argmax     | 0.084 | 0.112 |  0.007 |
| FedProx-bal+OC         | 0.122 | 0.297 |  0.161 |
| GB+CR argmax           | 0.152 | 0.32  |  0.062 |
| GB+CR+OC               | 0.168 | 0.428 |  0.167 |
| SAFE-X                 | 0.236 | 0.661 |  0.246 |
| SAFE-X owner-only cal. | 0.218 | 0.64  |  0.224 | 

MCC

| method                 |   cic |   ton |   unsw |
|:-----------------------|------:|------:|-------:|
| CCVR argmax            | 0.913 | 0.73  |  0.692 |
| CCVR+OC                | 0.968 | 0.758 |  0.745 |
| Central-bal argmax     | 0.985 | 0.804 |  0.791 |
| Central-bal+OC         | 0.982 | 0.803 |  0.779 |
| FedOV argmax           | 0.97  | 0.677 |  0.779 |
| FedOV+OC               | 0.965 | 0.782 |  0.769 |
| FedOV-full argmax      | 0.981 | 0.672 |  0.779 |
| FedOV-full+OC          | 0.975 | 0.786 |  0.768 |
| FedProx-bal argmax     | 0.984 | 0.687 |  0.777 |
| FedProx-bal+OC         | 0.968 | 0.712 |  0.774 |
| GB+CR argmax           | 0.983 | 0.711 |  0.776 |
| GB+CR+OC               | 0.979 | 0.725 |  0.768 |
| SAFE-X                 | 0.932 | 0.782 |  0.775 |
| SAFE-X owner-only cal. | 0.815 | 0.782 |  0.767 | 

## K50: rare-class F1 (seed means, k = 20)

| method                 |   cic |   ton |   unsw |
|:-----------------------|------:|------:|-------:|
| CCVR argmax            | 0.183 | 0.545 |  0.128 |
| CCVR+OC                | 0.194 | 0.648 |  0.167 |
| Central-bal argmax     | 0.335 | 0.807 |  0.279 |
| Central-bal+OC         | 0.252 | 0.712 |  0.238 |
| FedOV argmax           | 0.152 | 0.038 |  0     |
| FedOV+OC               | 0.167 | 0.698 |  0.222 |
| FedOV-full argmax      | 0.1   | 0     |  0     |
| FedOV-full+OC          | 0.186 | 0.693 |  0.236 |
| FedProx-bal argmax     | 0.052 | 0.056 |  0.006 |
| FedProx-bal+OC         | 0.1   | 0.145 |  0.106 |
| GB+CR argmax           | 0.17  | 0.299 |  0.017 |
| GB+CR+OC               | 0.173 | 0.369 |  0.128 |
| SAFE-X                 | 0.251 | 0.675 |  0.235 |
| SAFE-X owner-only cal. | 0.232 | 0.652 |  0.23  | 

MCC

| method                 |   cic |   ton |   unsw |
|:-----------------------|------:|------:|-------:|
| CCVR argmax            | 0.925 | 0.701 |  0.69  |
| CCVR+OC                | 0.968 | 0.732 |  0.738 |
| Central-bal argmax     | 0.986 | 0.807 |  0.789 |
| Central-bal+OC         | 0.981 | 0.804 |  0.778 |
| FedOV argmax           | 0.965 | 0.659 |  0.768 |
| FedOV+OC               | 0.962 | 0.782 |  0.758 |
| FedOV-full argmax      | 0.971 | 0.662 |  0.772 |
| FedOV-full+OC          | 0.97  | 0.783 |  0.763 |
| FedProx-bal argmax     | 0.982 | 0.676 |  0.78  |
| FedProx-bal+OC         | 0.965 | 0.685 |  0.776 |
| GB+CR argmax           | 0.974 | 0.71  |  0.777 |
| GB+CR+OC               | 0.97  | 0.722 |  0.766 |
| SAFE-X                 | 0.957 | 0.767 |  0.777 |
| SAFE-X owner-only cal. | 0.83  | 0.776 |  0.764 | 

## own2: rare-class F1 (seed means, k = 20)

| method                 |   cic |   ton |   unsw |
|:-----------------------|------:|------:|-------:|
| CCVR argmax            | 0.235 | 0.587 |  0.151 |
| CCVR+OC                | 0.25  | 0.672 |  0.198 |
| Central-bal argmax     | 0.353 | 0.829 |  0.352 |
| Central-bal+OC         | 0.254 | 0.727 |  0.229 |
| FedOV argmax           | 0.177 | 0.316 |  0.012 |
| FedOV+OC               | 0.168 | 0.698 |  0.235 |
| FedOV-full argmax      | 0.191 | 0.355 |  0.01  |
| FedOV-full+OC          | 0.168 | 0.728 |  0.227 |
| FedProx-bal argmax     | 0.224 | 0.482 |  0.049 |
| FedProx-bal+OC         | 0.207 | 0.585 |  0.22  |
| GB+CR argmax           | 0.223 | 0.598 |  0.149 |
| GB+CR+OC               | 0.194 | 0.581 |  0.206 |
| SAFE-X                 | 0.237 | 0.744 |  0.297 |
| SAFE-X owner-only cal. | 0.181 | 0.669 |  0.253 | 

MCC

| method                 |   cic |   ton |   unsw |
|:-----------------------|------:|------:|-------:|
| CCVR argmax            | 0.956 | 0.748 |  0.692 |
| CCVR+OC                | 0.965 | 0.767 |  0.742 |
| Central-bal argmax     | 0.982 | 0.819 |  0.792 |
| Central-bal+OC         | 0.978 | 0.816 |  0.78  |
| FedOV argmax           | 0.98  | 0.707 |  0.78  |
| FedOV+OC               | 0.973 | 0.797 |  0.77  |
| FedOV-full argmax      | 0.984 | 0.716 |  0.777 |
| FedOV-full+OC          | 0.976 | 0.803 |  0.767 |
| FedProx-bal argmax     | 0.986 | 0.741 |  0.783 |
| FedProx-bal+OC         | 0.97  | 0.77  |  0.774 |
| GB+CR argmax           | 0.98  | 0.762 |  0.775 |
| GB+CR+OC               | 0.973 | 0.767 |  0.764 |
| SAFE-X                 | 0.941 | 0.792 |  0.776 |
| SAFE-X owner-only cal. | 0.839 | 0.79  |  0.769 | 

## own3: rare-class F1 (seed means, k = 20)

| method                 |   cic |   ton |   unsw |
|:-----------------------|------:|------:|-------:|
| CCVR argmax            | 0.203 | 0.587 |  0.161 |
| CCVR+OC                | 0.211 | 0.692 |  0.191 |
| Central-bal argmax     | 0.372 | 0.852 |  0.321 |
| Central-bal+OC         | 0.289 | 0.745 |  0.24  |
| FedOV argmax           | 0.183 | 0.456 |  0.121 |
| FedOV+OC               | 0.139 | 0.716 |  0.241 |
| FedOV-full argmax      | 0.216 | 0.522 |  0.13  |
| FedOV-full+OC          | 0.164 | 0.687 |  0.241 |
| FedProx-bal argmax     | 0.238 | 0.68  |  0.167 |
| FedProx-bal+OC         | 0.197 | 0.709 |  0.222 |
| GB+CR argmax           | 0.23  | 0.725 |  0.248 |
| GB+CR+OC               | 0.212 | 0.691 |  0.23  |
| SAFE-X                 | 0.228 | 0.75  |  0.317 |
| SAFE-X owner-only cal. | 0.144 | 0.656 |  0.292 | 

MCC

| method                 |   cic |   ton |   unsw |
|:-----------------------|------:|------:|-------:|
| CCVR argmax            | 0.961 | 0.753 |  0.698 |
| CCVR+OC                | 0.961 | 0.769 |  0.744 |
| Central-bal argmax     | 0.986 | 0.812 |  0.788 |
| Central-bal+OC         | 0.979 | 0.81  |  0.778 |
| FedOV argmax           | 0.982 | 0.726 |  0.778 |
| FedOV+OC               | 0.973 | 0.795 |  0.768 |
| FedOV-full argmax      | 0.984 | 0.739 |  0.781 |
| FedOV-full+OC          | 0.977 | 0.798 |  0.771 |
| FedProx-bal argmax     | 0.987 | 0.77  |  0.779 |
| FedProx-bal+OC         | 0.976 | 0.795 |  0.771 |
| GB+CR argmax           | 0.984 | 0.778 |  0.773 |
| GB+CR+OC               | 0.979 | 0.788 |  0.762 |
| SAFE-X                 | 0.93  | 0.805 |  0.773 |
| SAFE-X owner-only cal. | 0.851 | 0.792 |  0.767 | 

Owner alone (own class): {('cic', 'K20'): 0.249, ('cic', 'K50'): 0.253, ('cic', 'own2'): 0.283, ('cic', 'own3'): 0.291, ('ton', 'K20'): 0.705, ('ton', 'K50'): 0.687, ('ton', 'own2'): 0.738, ('ton', 'own3'): 0.736, ('unsw', 'K20'): 0.236, ('unsw', 'K50'): 0.216, ('unsw', 'own2'): 0.271, ('unsw', 'own3'): 0.271} 

## Part G

- cic K20: G1 gap Central - best FL +15.9 [+12.1, +19.3]; G2 SAFE-X - FedOV-full+OC +7.5 [+1.5, +13.1]; SAFE-X - CCVR+OC +2.8 [-4.0, +9.3]; G3 FA owner-only 0.0564 vs federated 0.0144, diff +41.9 [+24.6, +59.9] per mille; common F1 SAFE-X - GB+CR -3.1 [-4.5, -2.0]
- ton K20: G1 gap Central - best FL +26.4 [+23.0, +29.5]; G2 SAFE-X - FedOV-full+OC -2.3 [-8.2, +2.5]; SAFE-X - CCVR+OC -0.8 [-10.0, +5.8]; G3 FA owner-only 0.0069 vs federated 0.0031, diff +3.8 [+2.2, +5.5] per mille; common F1 SAFE-X - GB+CR +0.1 [-0.4, +0.9]
- unsw K20: G1 gap Central - best FL +17.5 [+14.6, +20.0]; G2 SAFE-X - FedOV-full+OC +2.7 [+0.8, +4.6]; SAFE-X - GB+CR+OC +8.0 [+4.3, +11.5]; G3 FA owner-only 0.0034 vs federated 0.0014, diff +2.0 [+1.0, +3.2] per mille; common F1 SAFE-X - GB+CR -0.1 [-0.2, +0.0]
- cic K50: G1 gap Central - best FL +14.9 [+13.3, +16.7]; G2 SAFE-X - FedOV-full+OC +6.5 [+2.6, +10.1]; SAFE-X - CCVR+OC +5.7 [+0.9, +9.6]; G3 FA owner-only 0.0451 vs federated 0.0064, diff +38.7 [+16.9, +66.8] per mille; common F1 SAFE-X - GB+CR -0.8 [-1.5, -0.2]
- ton K50: G1 gap Central - best FL +26.2 [+23.2, +28.9]; G2 SAFE-X - FedOV+OC -2.3 [-7.0, +2.2]; SAFE-X - CCVR+OC +2.7 [-3.7, +9.4]; G3 FA owner-only 0.0065 vs federated 0.0027, diff +3.8 [+2.6, +5.1] per mille; common F1 SAFE-X - GB+CR -0.1 [-0.5, +0.3]
- unsw K50: G1 gap Central - best FL +15.1 [+10.7, +19.1]; G2 SAFE-X - FedOV-full+OC -0.1 [-3.4, +3.1]; SAFE-X - CCVR+OC +6.8 [+3.9, +9.5]; G3 FA owner-only 0.0042 vs federated 0.0014, diff +2.7 [+0.6, +6.2] per mille; common F1 SAFE-X - GB+CR -0.1 [-0.2, +0.0]

- G1 SUPPORTED (6/6); G2 NOT supported (3/6); G3 SUPPORTED (6/6)

## Part H

- cic own2: H1 gap Central - best FL +8.5 [+3.9, +12.6]; H2 SAFE-X - FedOV-full+OC +6.9 [+1.2, +12.2]; SAFE-X - CCVR+OC -1.3 [-6.8, +3.6]; H3 FA owner-only 0.0551 vs federated 0.0138, diff +41.3 [+21.0, +66.4] per mille; common F1 SAFE-X - GB+CR -2.2 [-3.5, -1.0]
- ton own2: H1 gap Central - best FL +19.2 [+12.7, +25.2]; H2 SAFE-X - FedOV-full+OC +1.6 [-1.7, +5.5]; SAFE-X - CCVR+OC +7.2 [+1.9, +12.8]; H3 FA owner-only 0.0071 vs federated 0.0029, diff +4.2 [+2.5, +6.2] per mille; common F1 SAFE-X - GB+CR -0.0 [-0.4, +0.3]
- unsw own2: H1 gap Central - best FL +17.1 [+13.8, +20.3]; H2 SAFE-X - FedOV+OC +6.2 [+4.8, +7.4]; SAFE-X - FedProx-bal+OC +7.7 [+5.4, +10.6]; H3 FA owner-only 0.0028 vs federated 0.0013, diff +1.5 [+0.7, +2.4] per mille; common F1 SAFE-X - GB+CR -0.0 [-0.1, +0.1]
- cic own3: H1 gap Central - best FL +11.0 [+7.5, +14.5]; H2 SAFE-X - FedOV-full+OC +6.4 [+3.1, +9.8]; SAFE-X - GB+CR+OC +1.6 [-4.5, +8.2]; H3 FA owner-only 0.0473 vs federated 0.0154, diff +31.8 [+16.5, +55.4] per mille; common F1 SAFE-X - GB+CR -3.2 [-4.2, -2.3]
- ton own3: H1 gap Central - best FL +10.7 [+5.9, +15.3]; H2 SAFE-X - FedOV+OC +3.4 [+0.7, +6.4]; SAFE-X - FedProx-bal+OC +4.1 [+0.7, +8.9]; H3 FA owner-only 0.0084 vs federated 0.0038, diff +4.6 [+3.2, +6.0] per mille; common F1 SAFE-X - GB+CR +0.1 [-0.4, +1.0]
- unsw own3: H1 gap Central - best FL +6.6 [+1.4, +11.9]; H2 SAFE-X - FedOV+OC +7.6 [+6.3, +9.0]; SAFE-X - GB+CR+OC +8.7 [+7.6, +9.7]; H3 FA owner-only 0.0027 vs federated 0.0013, diff +1.4 [+0.8, +2.1] per mille; common F1 SAFE-X - GB+CR -0.1 [-0.3, +0.1]

- H (descriptive): gap CI above 0 in 6/6; SAFE-X ahead of better FedOV+OC with CI above 0 in 5/6

## Part I: sensitivity to q (Study 3 main-arm runs, pooled over k)

|                           |   0.0001 |   0.0003 |   0.001 |   0.003 |   0.01 |
|:--------------------------|---------:|---------:|--------:|--------:|-------:|
| ('cic', 'CCVR+OC')        |    0.171 |    0.174 |   0.18  |   0.189 |  0.145 |
| ('cic', 'FedOV+OC')       |    0.165 |    0.152 |   0.172 |   0.201 |  0.178 |
| ('cic', 'FedOV-full+OC')  |    0.168 |    0.167 |   0.179 |   0.194 |  0.178 |
| ('cic', 'SAFE-X')         |    0.188 |    0.236 |   0.22  |   0.171 |  0.11  |
| ('ton', 'CCVR+OC')        |    0.501 |    0.608 |   0.643 |   0.597 |  0.529 |
| ('ton', 'FedOV+OC')       |    0.654 |    0.693 |   0.665 |   0.598 |  0.534 |
| ('ton', 'FedOV-full+OC')  |    0.63  |    0.669 |   0.651 |   0.584 |  0.504 |
| ('ton', 'SAFE-X')         |    0.645 |    0.686 |   0.667 |   0.627 |  0.563 |
| ('unsw', 'CCVR+OC')       |    0.096 |    0.129 |   0.169 |   0.155 |  0.108 |
| ('unsw', 'FedOV+OC')      |    0.226 |    0.244 |   0.224 |   0.189 |  0.117 |
| ('unsw', 'FedOV-full+OC') |    0.234 |    0.246 |   0.224 |   0.185 |  0.11  |
| ('unsw', 'SAFE-X')        |    0.152 |    0.228 |   0.259 |   0.233 |  0.176 | 

SAFE-X: expert false-alarm rate, rare precision and common-F1 change vs GB+CR

|                  |     fa |   rare_p |   rare_r |   dcommon |
|:-----------------|-------:|---------:|---------:|----------:|
| ('cic', 0.0001)  | 0.0028 |   0.2851 |   0.2993 |   -0.0027 |
| ('cic', 0.0003)  | 0.0053 |   0.2649 |   0.4011 |   -0.0079 |
| ('cic', 0.001)   | 0.013  |   0.186  |   0.4736 |   -0.0244 |
| ('cic', 0.003)   | 0.0279 |   0.1173 |   0.5165 |   -0.0529 |
| ('cic', 0.01)    | 0.0573 |   0.0677 |   0.5512 |   -0.11   |
| ('ton', 0.0001)  | 0.0007 |   0.8094 |   0.592  |    0.0146 |
| ('ton', 0.0003)  | 0.0013 |   0.7865 |   0.6689 |    0.0148 |
| ('ton', 0.001)   | 0.0027 |   0.6924 |   0.7355 |    0.0156 |
| ('ton', 0.003)   | 0.0056 |   0.6058 |   0.7953 |    0.0129 |
| ('ton', 0.01)    | 0.0156 |   0.5049 |   0.855  |    0.0027 |
| ('unsw', 0.0001) | 0.0001 |   0.368  |   0.1108 |    0.0006 |
| ('unsw', 0.0003) | 0.0004 |   0.3403 |   0.2078 |    0.0009 |
| ('unsw', 0.001)  | 0.0015 |   0.2616 |   0.3405 |    0.0007 |
| ('unsw', 0.003)  | 0.0043 |   0.1784 |   0.4778 |   -0.0022 |
| ('unsw', 0.01)   | 0.0116 |   0.1118 |   0.6297 |   -0.0245 | 

- I1 cic q=0.0001: SAFE-X - FedOV-full+OC +2.0 [-0.2, +4.3]
- I1 cic q=0.0003: SAFE-X - FedOV-full+OC +6.9 [+4.5, +9.2]
- I1 cic q=0.001: SAFE-X - FedOV-full+OC +4.1 [+2.0, +5.8]
- I1 cic q=0.003: SAFE-X - FedOV+OC -3.0 [-4.6, -1.4]
- I1 cic q=0.01: SAFE-X - FedOV+OC -6.8 [-9.3, -4.5]
- I1 ton q=0.0001: SAFE-X - FedOV+OC -0.9 [-5.3, +4.0]
- I1 ton q=0.0003: SAFE-X - FedOV+OC -0.7 [-3.7, +2.3]
- I1 ton q=0.001: SAFE-X - FedOV+OC +0.2 [-3.5, +3.5]
- I1 ton q=0.003: SAFE-X - FedOV+OC +2.9 [+0.1, +5.6]
- I1 ton q=0.01: SAFE-X - FedOV+OC +2.9 [+0.4, +5.2]
- I1 unsw q=0.0001: SAFE-X - FedOV-full+OC -8.2 [-9.9, -6.7]
- I1 unsw q=0.0003: SAFE-X - FedOV-full+OC -1.7 [-3.8, -0.0]
- I1 unsw q=0.001: SAFE-X - FedOV+OC +3.5 [+2.4, +4.7]
- I1 unsw q=0.003: SAFE-X - FedOV+OC +4.5 [+3.6, +5.3]
- I1 unsw q=0.01: SAFE-X - FedOV+OC +5.9 [+5.4, +6.5]
