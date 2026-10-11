# Pilot 5: shared owner experts (development seeds 0-4, alpha=0.5)

## ton, k=20

| method                               |   rare |   precision |   recall |   common |   benign_recall |
|:-------------------------------------|-------:|------------:|---------:|---------:|----------------:|
| Central-bal argmax                   |  0.791 |       0.862 |    0.751 |    0.719 |           0.917 |
| Experts[none (argmax)] + GB+CR       |  0.694 |       0.67  |    0.799 |    0.716 |           0.903 |
| Experts[none (argmax)] + FedProx-bal |  0.694 |       0.67  |    0.799 |    0.718 |           0.9   |
| Central-bal+OC                       |  0.678 |       0.632 |    0.821 |    0.726 |           0.912 |
| Experts[fed-others] + FedProx-bal    |  0.659 |       0.744 |    0.676 |    0.722 |           0.912 |
| Experts[fed-others] + GB+CR          |  0.659 |       0.744 |    0.676 |    0.721 |           0.915 |
| Experts[fed] + GB+CR                 |  0.657 |       0.74  |    0.677 |    0.721 |           0.915 |
| Experts[fed] + FedProx-bal           |  0.657 |       0.74  |    0.677 |    0.722 |           0.912 |
| Experts[val] + GB+CR                 |  0.646 |       0.613 |    0.795 |    0.717 |           0.904 |
| Experts[val] + FedProx-bal           |  0.646 |       0.613 |    0.795 |    0.72  |           0.901 |
| FedOV+OC                             |  0.636 |       0.605 |    0.782 |    0.712 |           0.902 |
| Experts[own] + GB+CR                 |  0.63  |       0.615 |    0.797 |    0.716 |           0.893 |
| Experts[own] + FedProx-bal           |  0.63  |       0.615 |    0.797 |    0.718 |           0.89  |
| CCVR+OC                              |  0.617 |       0.622 |    0.696 |    0.677 |           0.696 |
| CCVR argmax                          |  0.549 |       0.483 |    0.888 |    0.665 |           0.663 |
| FedProx-bal+OC                       |  0.356 |       0.421 |    0.374 |    0.723 |           0.915 |
| GB+CR+OC                             |  0.352 |       0.406 |    0.407 |    0.721 |           0.911 |
| GB+CR argmax                         |  0.304 |       0.478 |    0.275 |    0.721 |           0.922 |
| PROTEAN argmax                       |  0.303 |       0.35  |    0.32  |    0.699 |           0.895 |
| PROTEAN+OC                           |  0.224 |       0.237 |    0.279 |    0.7   |           0.894 |
| FedOV argmax                         |  0.211 |       0.398 |    0.154 |    0.699 |           0.918 |
| FedProx-bal argmax                   |  0.183 |       0.483 |    0.176 |    0.717 |           0.92  | 

## ton, k=100

| method                               |   rare |   precision |   recall |   common |   benign_recall |
|:-------------------------------------|-------:|------------:|---------:|---------:|----------------:|
| Central-bal argmax                   |  0.836 |       0.804 |    0.893 |    0.737 |           0.915 |
| Experts[fed-others] + FedProx-bal    |  0.736 |       0.701 |    0.841 |    0.726 |           0.914 |
| Experts[fed-others] + GB+CR          |  0.736 |       0.701 |    0.841 |    0.724 |           0.916 |
| Experts[fed] + FedProx-bal           |  0.733 |       0.697 |    0.842 |    0.726 |           0.914 |
| Experts[fed] + GB+CR                 |  0.733 |       0.697 |    0.842 |    0.724 |           0.915 |
| Central-bal+OC                       |  0.731 |       0.644 |    0.925 |    0.736 |           0.905 |
| Experts[none (argmax)] + FedProx-bal |  0.725 |       0.663 |    0.899 |    0.723 |           0.906 |
| Experts[none (argmax)] + GB+CR       |  0.725 |       0.663 |    0.899 |    0.721 |           0.908 |
| Experts[val] + GB+CR                 |  0.694 |       0.625 |    0.872 |    0.723 |           0.911 |
| Experts[val] + FedProx-bal           |  0.694 |       0.625 |    0.872 |    0.725 |           0.909 |
| FedOV+OC                             |  0.693 |       0.625 |    0.891 |    0.708 |           0.903 |
| CCVR+OC                              |  0.692 |       0.662 |    0.786 |    0.654 |           0.844 |
| Experts[own] + FedProx-bal           |  0.676 |       0.62  |    0.878 |    0.725 |           0.902 |
| Experts[own] + GB+CR                 |  0.676 |       0.62  |    0.878 |    0.722 |           0.904 |
| CCVR argmax                          |  0.568 |       0.492 |    0.908 |    0.663 |           0.823 |
| FedProx-bal+OC                       |  0.422 |       0.53  |    0.462 |    0.722 |           0.917 |
| GB+CR+OC                             |  0.421 |       0.422 |    0.499 |    0.709 |           0.813 |
| GB+CR argmax                         |  0.378 |       0.531 |    0.331 |    0.71  |           0.924 |
| PROTEAN+OC                           |  0.272 |       0.305 |    0.342 |    0.704 |           0.898 |
| PROTEAN argmax                       |  0.224 |       0.328 |    0.237 |    0.696 |           0.904 |
| FedOV argmax                         |  0.189 |       0.415 |    0.133 |    0.695 |           0.919 |
| FedProx-bal argmax                   |  0.159 |       0.592 |    0.103 |    0.714 |           0.923 | 

## unsw, k=20

| method                               |   rare |   precision |   recall |   common |   benign_recall |
|:-------------------------------------|-------:|------------:|---------:|---------:|----------------:|
| Central-bal argmax                   |  0.341 |       0.399 |    0.439 |    0.525 |           1     |
| Experts[none (argmax)] + GB+CR       |  0.288 |       0.222 |    0.569 |    0.483 |           0.999 |
| Experts[none (argmax)] + FedProx-bal |  0.288 |       0.222 |    0.569 |    0.483 |           0.999 |
| Experts[fed] + GB+CR                 |  0.268 |       0.252 |    0.358 |    0.487 |           1     |
| Experts[fed] + FedProx-bal           |  0.268 |       0.252 |    0.358 |    0.487 |           1     |
| Experts[fed-others] + FedProx-bal    |  0.267 |       0.249 |    0.359 |    0.487 |           1     |
| Experts[fed-others] + GB+CR          |  0.267 |       0.249 |    0.359 |    0.487 |           1     |
| Experts[own] + FedProx-bal           |  0.264 |       0.263 |    0.371 |    0.48  |           1     |
| Experts[own] + GB+CR                 |  0.264 |       0.263 |    0.371 |    0.481 |           1     |
| Experts[val] + FedProx-bal           |  0.245 |       0.186 |    0.486 |    0.483 |           1     |
| Experts[val] + GB+CR                 |  0.245 |       0.186 |    0.486 |    0.483 |           1     |
| FedOV+OC                             |  0.24  |       0.178 |    0.484 |    0.475 |           1     |
| Central-bal+OC                       |  0.223 |       0.174 |    0.473 |    0.519 |           1     |
| GB+CR+OC                             |  0.193 |       0.15  |    0.375 |    0.485 |           1     |
| FedProx-bal+OC                       |  0.187 |       0.161 |    0.319 |    0.487 |           1     |
| CCVR+OC                              |  0.173 |       0.148 |    0.286 |    0.474 |           0.999 |
| CCVR argmax                          |  0.141 |       0.085 |    0.623 |    0.438 |           0.995 |
| PROTEAN argmax                       |  0.114 |       0.075 |    0.386 |    0.402 |           1     |
| PROTEAN+OC                           |  0.109 |       0.106 |    0.147 |    0.441 |           1     |
| GB+CR argmax                         |  0.047 |       0.141 |    0.029 |    0.488 |           1     |
| FedProx-bal argmax                   |  0.004 |       0.098 |    0.002 |    0.487 |           1     |
| FedOV argmax                         |  0     |       0     |    0     |    0.48  |           1     | 

## unsw, k=100

| method                               |   rare |   precision |   recall |   common |   benign_recall |
|:-------------------------------------|-------:|------------:|---------:|---------:|----------------:|
| Central-bal argmax                   |  0.358 |       0.317 |    0.542 |    0.532 |           1     |
| Experts[fed-others] + FedProx-bal    |  0.298 |       0.284 |    0.395 |    0.494 |           1     |
| Experts[fed-others] + GB+CR          |  0.298 |       0.284 |    0.395 |    0.494 |           1     |
| Experts[fed] + FedProx-bal           |  0.298 |       0.281 |    0.396 |    0.494 |           1     |
| Experts[fed] + GB+CR                 |  0.298 |       0.281 |    0.396 |    0.494 |           1     |
| Experts[own] + GB+CR                 |  0.272 |       0.247 |    0.401 |    0.49  |           1     |
| Experts[own] + FedProx-bal           |  0.272 |       0.247 |    0.401 |    0.49  |           1     |
| Experts[none (argmax)] + GB+CR       |  0.244 |       0.167 |    0.642 |    0.473 |           0.998 |
| Experts[val] + FedProx-bal           |  0.244 |       0.179 |    0.512 |    0.489 |           0.999 |
| Experts[none (argmax)] + FedProx-bal |  0.244 |       0.167 |    0.642 |    0.472 |           0.998 |
| Experts[val] + GB+CR                 |  0.244 |       0.179 |    0.512 |    0.49  |           0.999 |
| Central-bal+OC                       |  0.233 |       0.176 |    0.487 |    0.526 |           1     |
| FedOV+OC                             |  0.229 |       0.174 |    0.486 |    0.479 |           1     |
| CCVR+OC                              |  0.215 |       0.166 |    0.389 |    0.487 |           0.999 |
| FedProx-bal+OC                       |  0.215 |       0.195 |    0.33  |    0.492 |           1     |
| GB+CR+OC                             |  0.213 |       0.169 |    0.429 |    0.49  |           1     |
| CCVR argmax                          |  0.146 |       0.086 |    0.659 |    0.445 |           0.993 |
| PROTEAN argmax                       |  0.123 |       0.111 |    0.257 |    0.445 |           1     |
| PROTEAN+OC                           |  0.121 |       0.122 |    0.179 |    0.455 |           1     |
| GB+CR argmax                         |  0.072 |       0.246 |    0.061 |    0.494 |           1     |
| FedProx-bal argmax                   |  0.015 |       0.17  |    0.009 |    0.493 |           1     |
| FedOV argmax                         |  0     |       0     |    0     |    0.483 |           1     | 

## Owner alone (on its own class)

|               |    f1 |
|:--------------|------:|
| ('ton', 20)   | 0.687 |
| ('ton', 100)  | 0.714 |
| ('unsw', 20)  | 0.285 |
| ('unsw', 100) | 0.241 | 

## Paired rare-F1 differences (x100), 95% CI over seeds

- ton k=20: Experts[fed] + GB+CR - best baseline: +0.2 [-8.8, +9.2]
- ton k=20: Experts[fed-others] + GB+CR - best baseline: +0.4 [-8.6, +9.6]
- ton k=20: Experts[fed] + FedProx-bal - best baseline: +0.2 [-8.8, +9.5]
- ton k=20: Central-bal - Experts[fed]+GB+CR: +13.5
- ton k=100: Experts[fed] + GB+CR - best baseline: +0.2 [-3.4, +3.9]
- ton k=100: Experts[fed-others] + GB+CR - best baseline: +0.5 [-3.4, +4.1]
- ton k=100: Experts[fed] + FedProx-bal - best baseline: +0.2 [-3.4, +3.9]
- ton k=100: Central-bal - Experts[fed]+GB+CR: +10.3
- unsw k=20: Experts[fed] + GB+CR - best baseline: +2.8 [+0.1, +5.2]
- unsw k=20: Experts[fed-others] + GB+CR - best baseline: +2.6 [+0.0, +5.2]
- unsw k=20: Experts[fed] + FedProx-bal - best baseline: +2.8 [+0.3, +5.2]
- unsw k=20: Central-bal - Experts[fed]+GB+CR: +7.3
- unsw k=100: Experts[fed] + GB+CR - best baseline: +4.3 [+2.3, +6.6]
- unsw k=100: Experts[fed-others] + GB+CR - best baseline: +4.4 [+2.5, +6.6]
- unsw k=100: Experts[fed] + FedProx-bal - best baseline: +4.3 [+2.3, +6.7]
- unsw k=100: Central-bal - Experts[fed]+GB+CR: +6.0

## Interpretation (development, not sealed)
- Strongest baseline is FedOV adapted to tabular data **with our OC threshold** (FedOV+OC); plain FedOV voting finds almost no rare flows (F1 0-0.21). PROTEAN is weak here (0.11-0.30), below CCVR+OC.
- Experts[fed]+GB+CR vs FedOV+OC (seed means): ToN +2.1 (k=20), +4.0 (k=100); UNSW +2.8 (k=20), +6.9 (k=100). Against the per-seed best of ~10 baselines (conservative): ToN +0.2 (CIs span 0), UNSW +2.8 [+0.1,+5.2] and +4.3 [+2.3,+6.6].
- Experts keep benign recall at the base model's level; FedOV+OC loses ~0.01 on ToN.
- Verdict: consistent but small advantage; clear on UNSW, not on ToN (high seed variance). The distinctive, measurable part is the federated calibration (false-alarm overshoot halved vs owner-only).
