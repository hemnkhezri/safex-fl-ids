# Study 3 results (plan v3)

Units: {('cic', 'main', 5): 10, ('cic', 'main', 20): 10, ('cic', 'main', 100): 10, ('ton', 'big', 20): 5, ('ton', 'ip', 5): 10, ('ton', 'ip', 20): 10, ('ton', 'ip', 100): 10, ('ton', 'main', 5): 10, ('ton', 'main', 20): 10, ('ton', 'main', 100): 10, ('unsw', 'big', 20): 5, ('unsw', 'main', 5): 10, ('unsw', 'main', 20): 10, ('unsw', 'main', 100): 10} 

## cic, main: rare F1 (seed means)

| method                         |     5 |    20 |   100 |
|:-------------------------------|------:|------:|------:|
| CCVR argmax                    | 0.194 | 0.197 | 0.21  |
| CCVR+OC                        | 0.172 | 0.193 | 0.173 |
| Central-bal argmax             | 0.303 | 0.337 | 0.37  |
| Central-bal+OC                 | 0.242 | 0.236 | 0.262 |
| FedOV argmax                   | 0.169 | 0.169 | 0.168 |
| FedOV+OC                       | 0.194 | 0.17  | 0.153 |
| FedOV-full argmax              | 0.169 | 0.152 | 0.138 |
| FedOV-full+OC                  | 0.21  | 0.156 | 0.172 |
| FedProx-bal argmax             | 0.138 | 0.15  | 0.157 |
| FedProx-bal+OC                 | 0.187 | 0.196 | 0.178 |
| GB+CR argmax                   | 0.119 | 0.173 | 0.174 |
| GB+CR+OC                       | 0.158 | 0.185 | 0.171 |
| SAFE-X                         | 0.169 | 0.24  | 0.25  |
| SAFE-X owner-only cal.         | 0.134 | 0.192 | 0.217 |
| SAFE-X recalibrated (eval 75%) | 0.078 | 0.073 | 0.075 |
| SAFE-X static (eval 75%)       | 0.169 | 0.24  | 0.251 |
| SAFE-X-DP eps1                 | 0.009 | 0.069 | 0.146 |
| SAFE-X-DP eps8                 | 0.009 | 0.005 | 0.159 | 

MCC (seed means)

| method                         |     5 |    20 |   100 |
|:-------------------------------|------:|------:|------:|
| CCVR argmax                    | 0.952 | 0.899 | 0.961 |
| CCVR+OC                        | 0.959 | 0.958 | 0.961 |
| Central-bal argmax             | 0.979 | 0.981 | 0.983 |
| Central-bal+OC                 | 0.975 | 0.978 | 0.978 |
| FedOV argmax                   | 0.976 | 0.98  | 0.98  |
| FedOV+OC                       | 0.967 | 0.974 | 0.971 |
| FedOV-full argmax              | 0.985 | 0.985 | 0.983 |
| FedOV-full+OC                  | 0.976 | 0.973 | 0.974 |
| FedProx-bal argmax             | 0.984 | 0.982 | 0.984 |
| FedProx-bal+OC                 | 0.972 | 0.967 | 0.97  |
| GB+CR argmax                   | 0.974 | 0.979 | 0.981 |
| GB+CR+OC                       | 0.973 | 0.974 | 0.977 |
| SAFE-X                         | 0.932 | 0.937 | 0.948 |
| SAFE-X owner-only cal.         | 0.779 | 0.825 | 0.864 |
| SAFE-X recalibrated (eval 75%) | 0.366 | 0.514 | 0.606 |
| SAFE-X static (eval 75%)       | 0.89  | 0.898 | 0.917 |
| SAFE-X-DP eps1                 | 0.949 | 0.94  | 0.937 |
| SAFE-X-DP eps8                 | 0.95  | 0.935 | 0.936 | 

## ton, big: rare F1 (seed means)

| method                         |    20 |
|:-------------------------------|------:|
| CCVR argmax                    | 0.591 |
| CCVR+OC                        | 0.69  |
| Central-bal argmax             | 0.819 |
| Central-bal+OC                 | 0.731 |
| FedOV argmax                   | 0.182 |
| FedOV+OC                       | 0.698 |
| FedOV-full argmax              | 0.084 |
| FedOV-full+OC                  | 0.648 |
| FedProx-bal argmax             | 0.531 |
| FedProx-bal+OC                 | 0.593 |
| GB+CR argmax                   | 0.632 |
| GB+CR+OC                       | 0.591 |
| SAFE-X                         | 0.719 |
| SAFE-X owner-only cal.         | 0.692 |
| SAFE-X recalibrated (eval 75%) | 0.568 |
| SAFE-X static (eval 75%)       | 0.558 |
| SAFE-X-DP eps1                 | 0.217 |
| SAFE-X-DP eps8                 | 0.128 | 

MCC (seed means)

| method                         |    20 |
|:-------------------------------|------:|
| CCVR argmax                    | 0.749 |
| CCVR+OC                        | 0.764 |
| Central-bal argmax             | 0.818 |
| Central-bal+OC                 | 0.815 |
| FedOV argmax                   | 0.698 |
| FedOV+OC                       | 0.782 |
| FedOV-full argmax              | 0.688 |
| FedOV-full+OC                  | 0.77  |
| FedProx-bal argmax             | 0.724 |
| FedProx-bal+OC                 | 0.754 |
| GB+CR argmax                   | 0.738 |
| GB+CR+OC                       | 0.748 |
| SAFE-X                         | 0.783 |
| SAFE-X owner-only cal.         | 0.783 |
| SAFE-X recalibrated (eval 75%) | 0.918 |
| SAFE-X static (eval 75%)       | 0.917 |
| SAFE-X-DP eps1                 | 0.696 |
| SAFE-X-DP eps8                 | 0.686 | 

## ton, ip: rare F1 (seed means)

| method                         |     5 |    20 |   100 |
|:-------------------------------|------:|------:|------:|
| CCVR argmax                    | 0.326 | 0.336 | 0.381 |
| CCVR+OC                        | 0.362 | 0.374 | 0.405 |
| Central-bal argmax             | 0.552 | 0.636 | 0.663 |
| Central-bal+OC                 | 0.493 | 0.536 | 0.54  |
| FedOV argmax                   | 0.095 | 0.195 | 0.205 |
| FedOV+OC                       | 0.363 | 0.444 | 0.387 |
| FedOV-full argmax              | 0.066 | 0.111 | 0.155 |
| FedOV-full+OC                  | 0.335 | 0.399 | 0.361 |
| FedProx-bal argmax             | 0.071 | 0.14  | 0.193 |
| FedProx-bal+OC                 | 0.147 | 0.216 | 0.271 |
| GB+CR argmax                   | 0.26  | 0.291 | 0.301 |
| GB+CR+OC                       | 0.302 | 0.276 | 0.299 |
| SAFE-X                         | 0.38  | 0.446 | 0.477 |
| SAFE-X owner-only cal.         | 0.211 | 0.262 | 0.246 |
| SAFE-X recalibrated (eval 75%) | 0.406 | 0.445 | 0.444 |
| SAFE-X static (eval 75%)       | 0.401 | 0.401 | 0.42  |
| SAFE-X-DP eps1                 | 0.015 | 0.092 | 0.336 |
| SAFE-X-DP eps8                 | 0.019 | 0.079 | 0.338 | 

MCC (seed means)

| method                         |     5 |    20 |   100 |
|:-------------------------------|------:|------:|------:|
| CCVR argmax                    | 0.601 | 0.569 | 0.583 |
| CCVR+OC                        | 0.628 | 0.596 | 0.575 |
| Central-bal argmax             | 0.719 | 0.734 | 0.744 |
| Central-bal+OC                 | 0.716 | 0.732 | 0.737 |
| FedOV argmax                   | 0.384 | 0.387 | 0.399 |
| FedOV+OC                       | 0.419 | 0.439 | 0.439 |
| FedOV-full argmax              | 0.396 | 0.376 | 0.439 |
| FedOV-full+OC                  | 0.429 | 0.433 | 0.483 |
| FedProx-bal argmax             | 0.512 | 0.544 | 0.548 |
| FedProx-bal+OC                 | 0.523 | 0.559 | 0.564 |
| GB+CR argmax                   | 0.523 | 0.533 | 0.551 |
| GB+CR+OC                       | 0.528 | 0.53  | 0.549 |
| SAFE-X                         | 0.536 | 0.564 | 0.589 |
| SAFE-X owner-only cal.         | 0.43  | 0.438 | 0.472 |
| SAFE-X recalibrated (eval 75%) | 0.699 | 0.708 | 0.728 |
| SAFE-X static (eval 75%)       | 0.704 | 0.714 | 0.732 |
| SAFE-X-DP eps1                 | 0.5   | 0.516 | 0.548 |
| SAFE-X-DP eps8                 | 0.5   | 0.513 | 0.552 | 

## ton, main: rare F1 (seed means)

| method                         |     5 |    20 |   100 |
|:-------------------------------|------:|------:|------:|
| CCVR argmax                    | 0.549 | 0.559 | 0.569 |
| CCVR+OC                        | 0.614 | 0.66  | 0.654 |
| Central-bal argmax             | 0.633 | 0.818 | 0.848 |
| Central-bal+OC                 | 0.627 | 0.734 | 0.725 |
| FedOV argmax                   | 0.116 | 0.17  | 0.221 |
| FedOV+OC                       | 0.659 | 0.665 | 0.67  |
| FedOV-full argmax              | 0.052 | 0.141 | 0.133 |
| FedOV-full+OC                  | 0.591 | 0.691 | 0.672 |
| FedProx-bal argmax             | 0.177 | 0.177 | 0.268 |
| FedProx-bal+OC                 | 0.371 | 0.416 | 0.418 |
| GB+CR argmax                   | 0.275 | 0.343 | 0.431 |
| GB+CR+OC                       | 0.409 | 0.451 | 0.461 |
| SAFE-X                         | 0.623 | 0.665 | 0.713 |
| SAFE-X owner-only cal.         | 0.609 | 0.671 | 0.691 |
| SAFE-X recalibrated (eval 75%) | 0.468 | 0.532 | 0.557 |
| SAFE-X static (eval 75%)       | 0.496 | 0.525 | 0.544 |
| SAFE-X-DP eps1                 | 0.045 | 0.104 | 0.384 |
| SAFE-X-DP eps8                 | 0.026 | 0.126 | 0.421 | 

MCC (seed means)

| method                         |     5 |    20 |   100 |
|:-------------------------------|------:|------:|------:|
| CCVR argmax                    | 0.712 | 0.712 | 0.737 |
| CCVR+OC                        | 0.733 | 0.735 | 0.756 |
| Central-bal argmax             | 0.75  | 0.805 | 0.82  |
| Central-bal+OC                 | 0.766 | 0.806 | 0.815 |
| FedOV argmax                   | 0.687 | 0.69  | 0.7   |
| FedOV+OC                       | 0.773 | 0.765 | 0.793 |
| FedOV-full argmax              | 0.682 | 0.696 | 0.693 |
| FedOV-full+OC                  | 0.764 | 0.786 | 0.793 |
| FedProx-bal argmax             | 0.693 | 0.696 | 0.708 |
| FedProx-bal+OC                 | 0.721 | 0.738 | 0.736 |
| GB+CR argmax                   | 0.704 | 0.72  | 0.724 |
| GB+CR+OC                       | 0.719 | 0.72  | 0.734 |
| SAFE-X                         | 0.754 | 0.777 | 0.787 |
| SAFE-X owner-only cal.         | 0.763 | 0.764 | 0.797 |
| SAFE-X recalibrated (eval 75%) | 0.9   | 0.915 | 0.914 |
| SAFE-X static (eval 75%)       | 0.908 | 0.915 | 0.912 |
| SAFE-X-DP eps1                 | 0.653 | 0.687 | 0.714 |
| SAFE-X-DP eps8                 | 0.674 | 0.691 | 0.722 | 

## unsw, big: rare F1 (seed means)

| method                         |    20 |
|:-------------------------------|------:|
| CCVR argmax                    | 0.166 |
| CCVR+OC                        | 0.175 |
| Central-bal argmax             | 0.29  |
| Central-bal+OC                 | 0.204 |
| FedOV argmax                   | 0     |
| FedOV+OC                       | 0.207 |
| FedOV-full argmax              | 0     |
| FedOV-full+OC                  | 0.217 |
| FedProx-bal argmax             | 0.068 |
| FedProx-bal+OC                 | 0.188 |
| GB+CR argmax                   | 0.104 |
| GB+CR+OC                       | 0.181 |
| SAFE-X                         | 0.249 |
| SAFE-X owner-only cal.         | 0.215 |
| SAFE-X recalibrated (eval 75%) | 0.201 |
| SAFE-X static (eval 75%)       | 0.25  |
| SAFE-X-DP eps1                 | 0.012 |
| SAFE-X-DP eps8                 | 0.003 | 

MCC (seed means)

| method                         |    20 |
|:-------------------------------|------:|
| CCVR argmax                    | 0.7   |
| CCVR+OC                        | 0.725 |
| Central-bal argmax             | 0.798 |
| Central-bal+OC                 | 0.785 |
| FedOV argmax                   | 0.786 |
| FedOV+OC                       | 0.778 |
| FedOV-full argmax              | 0.785 |
| FedOV-full+OC                  | 0.778 |
| FedProx-bal argmax             | 0.77  |
| FedProx-bal+OC                 | 0.764 |
| GB+CR argmax                   | 0.775 |
| GB+CR+OC                       | 0.766 |
| SAFE-X                         | 0.777 |
| SAFE-X owner-only cal.         | 0.765 |
| SAFE-X recalibrated (eval 75%) | 0.777 |
| SAFE-X static (eval 75%)       | 0.776 |
| SAFE-X-DP eps1                 | 0.77  |
| SAFE-X-DP eps8                 | 0.77  | 

## unsw, main: rare F1 (seed means)

| method                         |     5 |    20 |   100 |
|:-------------------------------|------:|------:|------:|
| CCVR argmax                    | 0.136 | 0.141 | 0.145 |
| CCVR+OC                        | 0.13  | 0.174 | 0.203 |
| Central-bal argmax             | 0.22  | 0.299 | 0.365 |
| Central-bal+OC                 | 0.199 | 0.223 | 0.241 |
| FedOV argmax                   | 0     | 0     | 0     |
| FedOV+OC                       | 0.21  | 0.22  | 0.242 |
| FedOV-full argmax              | 0     | 0     | 0     |
| FedOV-full+OC                  | 0.204 | 0.213 | 0.254 |
| FedProx-bal argmax             | 0.025 | 0.018 | 0.026 |
| FedProx-bal+OC                 | 0.167 | 0.186 | 0.218 |
| GB+CR argmax                   | 0.059 | 0.098 | 0.095 |
| GB+CR+OC                       | 0.175 | 0.19  | 0.201 |
| SAFE-X                         | 0.212 | 0.275 | 0.292 |
| SAFE-X owner-only cal.         | 0.193 | 0.25  | 0.267 |
| SAFE-X recalibrated (eval 75%) | 0.164 | 0.201 | 0.187 |
| SAFE-X static (eval 75%)       | 0.209 | 0.274 | 0.288 |
| SAFE-X-DP eps1                 | 0.005 | 0.005 | 0.029 |
| SAFE-X-DP eps8                 | 0.001 | 0.004 | 0.022 | 

MCC (seed means)

| method                         |     5 |    20 |   100 |
|:-------------------------------|------:|------:|------:|
| CCVR argmax                    | 0.702 | 0.674 | 0.662 |
| CCVR+OC                        | 0.745 | 0.72  | 0.716 |
| Central-bal argmax             | 0.791 | 0.794 | 0.789 |
| Central-bal+OC                 | 0.781 | 0.781 | 0.778 |
| FedOV argmax                   | 0.78  | 0.784 | 0.776 |
| FedOV+OC                       | 0.771 | 0.771 | 0.768 |
| FedOV-full argmax              | 0.778 | 0.783 | 0.775 |
| FedOV-full+OC                  | 0.768 | 0.771 | 0.767 |
| FedProx-bal argmax             | 0.77  | 0.778 | 0.734 |
| FedProx-bal+OC                 | 0.767 | 0.773 | 0.735 |
| GB+CR argmax                   | 0.768 | 0.767 | 0.744 |
| GB+CR+OC                       | 0.759 | 0.758 | 0.739 |
| SAFE-X                         | 0.767 | 0.768 | 0.747 |
| SAFE-X owner-only cal.         | 0.758 | 0.76  | 0.741 |
| SAFE-X recalibrated (eval 75%) | 0.766 | 0.766 | 0.742 |
| SAFE-X static (eval 75%)       | 0.766 | 0.766 | 0.744 |
| SAFE-X-DP eps1                 | 0.761 | 0.761 | 0.738 |
| SAFE-X-DP eps8                 | 0.761 | 0.761 | 0.738 | 

Owner alone (own class): {('cic', 'main', 5): 0.258, ('cic', 'main', 20): 0.279, ('cic', 'main', 100): 0.252, ('ton', 'big', 20): 0.754, ('ton', 'ip', 5): 0.374, ('ton', 'ip', 20): 0.338, ('ton', 'ip', 100): 0.316, ('ton', 'main', 5): 0.701, ('ton', 'main', 20): 0.726, ('ton', 'main', 100): 0.697, ('unsw', 'big', 20): 0.248, ('unsw', 'main', 5): 0.229, ('unsw', 'main', 20): 0.283, ('unsw', 'main', 100): 0.236} 

## Part A: SAFE-X vs the better FedOV+OC (arm main)

- A1 ton: better FedOV = FedOV+OC; SAFE-X - FedOV+OC: +0.2 [-3.5, +3.6] -> NOT supported
  - A2 ton k=5: SAFE-X - FedOV-full+OC +3.1 [-2.4, +9.3]
  - A2 ton k=20: SAFE-X - FedOV-full+OC -2.6 [-11.5, +4.8]
  - A2 ton k=100: SAFE-X - FedOV-full+OC +4.1 [-0.9, +8.9]
- A1 unsw: better FedOV = FedOV+OC; SAFE-X - FedOV+OC: +3.5 [+2.3, +4.7] -> SUPPORTED
  - A2 unsw k=5: SAFE-X - FedOV-full+OC +0.8 [-1.5, +2.8]
  - A2 unsw k=20: SAFE-X - FedOV-full+OC +6.1 [+5.0, +7.3]
  - A2 unsw k=100: SAFE-X - FedOV-full+OC +3.8 [+2.3, +5.4]

## Part B: destination-host sites (ToN)

- B1 k=5: Central - best FL +21.1 [+16.7, +25.1]
- B1 k=20: Central - best FL +29.2 [+24.7, +33.8]
- B1 k=100: Central - best FL +27.4 [+23.2, +31.5]
- B1: SUPPORTED
- B2: SAFE-X - FedOV+OC +3.6 [+0.3, +6.9] -> SUPPORTED
- B3: owner-only 0.0689, federated 0.0018; diff +67.1 [+56.6, +76.7] per mille -> SUPPORTED
  owner flows used: {'min': {(5, 'Backdoor'): 5, (5, 'dos'): 5, (5, 'mitm'): 5, (5, 'ransomware'): 5, (20, 'Backdoor'): 20, (20, 'dos'): 20, (20, 'mitm'): 20, (20, 'ransomware'): 20, (100, 'Backdoor'): 100, (100, 'dos'): 100, (100, 'mitm'): 100, (100, 'ransomware'): 100}, 'max': {(5, 'Backdoor'): 5, (5, 'dos'): 5, (5, 'mitm'): 5, (5, 'ransomware'): 5, (20, 'Backdoor'): 20, (20, 'dos'): 20, (20, 'mitm'): 20, (20, 'ransomware'): 20, (100, 'Backdoor'): 100, (100, 'dos'): 100, (100, 'mitm'): 100, (100, 'ransomware'): 100}}

## Part C: privacy (arm main)

- C1 ton k=5 _dp1: MIA AUC 0.508 [0.447, 0.563]
- C1 ton k=5 _dp8: MIA AUC 0.490 [0.436, 0.540]
- C1 ton k=5 nonDP: MIA AUC 0.768 [0.705, 0.823]
- C1 ton k=20 _dp1: MIA AUC 0.496 [0.473, 0.520]
- C1 ton k=20 _dp8: MIA AUC 0.490 [0.459, 0.520]
- C1 ton k=20 nonDP: MIA AUC 0.574 [0.550, 0.596]
- C1 ton k=100 _dp1: MIA AUC 0.498 [0.486, 0.509]
- C1 ton k=100 _dp8: MIA AUC 0.499 [0.489, 0.509]
- C1 ton k=100 nonDP: MIA AUC 0.521 [0.516, 0.527]
- C1 unsw k=5 _dp1: MIA AUC 0.523 [0.482, 0.561]
- C1 unsw k=5 _dp8: MIA AUC 0.538 [0.519, 0.556]
- C1 unsw k=5 nonDP: MIA AUC 0.854 [0.814, 0.890]
- C1 unsw k=20 _dp1: MIA AUC 0.521 [0.494, 0.545]
- C1 unsw k=20 _dp8: MIA AUC 0.519 [0.489, 0.546]
- C1 unsw k=20 nonDP: MIA AUC 0.678 [0.647, 0.712]
- C1 unsw k=100 _dp1: MIA AUC 0.505 [0.490, 0.519]
- C1 unsw k=100 _dp8: MIA AUC 0.505 [0.488, 0.522]
- C1 unsw k=100 nonDP: MIA AUC 0.572 [0.560, 0.588]
- C2 ton SAFE-X-DP eps8: rare F1 0.191 (SAFE-X 0.667); minus FedOV+OC -47.4 [-50.8, -43.9]
- C2 ton SAFE-X-DP eps1: rare F1 0.178 (SAFE-X 0.667); minus FedOV+OC -48.7 [-51.6, -45.7]
- C2 unsw SAFE-X-DP eps8: rare F1 0.009 (SAFE-X 0.259); minus FedOV+OC -21.5 [-22.4, -20.5]
- C2 unsw SAFE-X-DP eps1: rare F1 0.013 (SAFE-X 0.259); minus FedOV+OC -21.1 [-22.2, -20.0]
  - false-alarm rate ton _dp1: federated 0.0037
  - false-alarm rate ton _dp8: federated 0.0017
  - false-alarm rate ton nonDP: federated 0.0027
  - false-alarm rate unsw _dp1: federated 0.0010
  - false-alarm rate unsw _dp8: federated 0.0009
  - false-alarm rate unsw nonDP: federated 0.0015

## Part D: recalibration under drift (arm main)

- D1 ton: static 0.0028, recalibrated 0.0027; static - recal +0.1 [-0.5, +0.6] per mille -> NOT supported
  - SAFE-X static (eval 75%): rare F1 0.522; benign recall 0.9142
  - SAFE-X recalibrated (eval 75%): rare F1 0.519; benign recall 0.9129
- D1 unsw: static 0.0014, recalibrated 0.0005; static - recal +0.9 [+0.8, +1.0] per mille -> SUPPORTED
  - SAFE-X static (eval 75%): rare F1 0.257; benign recall 0.9995
  - SAFE-X recalibrated (eval 75%): rare F1 0.184; benign recall 0.9997

## Part E: larger model (k = 20)

| method                         |   ton |   unsw |
|:-------------------------------|------:|-------:|
| CCVR argmax                    | 0.591 |  0.166 |
| CCVR+OC                        | 0.69  |  0.175 |
| Central-bal argmax             | 0.819 |  0.29  |
| Central-bal+OC                 | 0.731 |  0.204 |
| FedOV argmax                   | 0.182 |  0     |
| FedOV+OC                       | 0.698 |  0.207 |
| FedOV-full argmax              | 0.084 |  0     |
| FedOV-full+OC                  | 0.648 |  0.217 |
| FedProx-bal argmax             | 0.531 |  0.068 |
| FedProx-bal+OC                 | 0.593 |  0.188 |
| GB+CR argmax                   | 0.632 |  0.104 |
| GB+CR+OC                       | 0.591 |  0.181 |
| SAFE-X                         | 0.719 |  0.249 |
| SAFE-X owner-only cal.         | 0.692 |  0.215 |
| SAFE-X recalibrated (eval 75%) | 0.568 |  0.201 |
| SAFE-X static (eval 75%)       | 0.558 |  0.25  |
| SAFE-X-DP eps1                 | 0.217 |  0.012 |
| SAFE-X-DP eps8                 | 0.128 |  0.003 |

## Part F: NF-CSE-CIC-IDS2018-v3 (arm main)

- F1 k=5: Central - best FL +10.8 [+7.2, +13.9]
- F1 k=20: Central - best FL +13.7 [+9.9, +17.4]
- F1 k=100: Central - best FL +15.4 [+12.0, +18.1]
- F1: SUPPORTED
- F2: better FedOV = FedOV-full+OC; SAFE-X - FedOV-full+OC: +4.1 [+2.1, +5.8] -> SUPPORTED
- F3: owner-only 0.0515, federated 0.0130; diff +38.5 [+23.2, +57.3] per mille -> SUPPORTED
- F4 k=5: benign recall -0.0056; common F1 -2.71 pts -> FAIL
- F4 k=20: benign recall -0.0043; common F1 -2.93 pts -> FAIL
- F4 k=100: benign recall -0.0057; common F1 -2.01 pts -> FAIL
  descriptive (rare F1 seed means): {'SAFE-X': {5: 0.169, 20: 0.24, 100: 0.25}, 'FedOV-full+OC': {5: 0.21, 20: 0.156, 100: 0.172}, 'GB+CR argmax': {5: 0.119, 20: 0.173, 100: 0.174}, 'Central-bal argmax': {5: 0.303, 20: 0.337, 100: 0.37}}

## Cost: median training seconds per run

| method             |   ('cic', 'main') |   ('ton', 'big') |   ('ton', 'ip') |   ('ton', 'main') |   ('unsw', 'big') |   ('unsw', 'main') |
|:-------------------|------------------:|-----------------:|----------------:|------------------:|------------------:|-------------------:|
| Central-bal        |                38 |              124 |              37 |                37 |               310 |                 31 |
| FedAvg-bal         |               253 |             1216 |             249 |               250 |              1123 |                210 |
| FedOV              |                73 |              336 |              70 |                69 |               328 |                 55 |
| FedOV-full         |               105 |              397 |             103 |                98 |               428 |                 79 |
| FedProx-bal        |               259 |             1255 |             259 |               257 |              1145 |                210 |
| GB+CR              |               243 |             1182 |             252 |               244 |              1101 |                204 |
| experts (incl. DP) |                92 |              365 |              96 |                97 |               328 |                 71 |
