# Confirmatory results (sealed plan v1)

Units: {('ton', 'big', 0.5, 20): 5, ('ton', 'e1', 0.5, 20): 5, ('ton', 'primary', 0.3, 20): 5, ('ton', 'primary', 0.5, 5): 10, ('ton', 'primary', 0.5, 20): 10, ('ton', 'primary', 0.5, 100): 10, ('unsw', 'big', 0.5, 20): 5, ('unsw', 'e1', 0.5, 20): 5, ('unsw', 'primary', 0.3, 20): 5, ('unsw', 'primary', 0.5, 5): 10, ('unsw', 'primary', 0.5, 20): 10, ('unsw', 'primary', 0.5, 100): 10} 

## ton, arm=big, alpha=0.5: rare-class F1 (seed mean)

|                                   |    20 |
|:----------------------------------|------:|
| ('CCVR', 'OC q=0.0001')           | 0.537 |
| ('CCVR', 'OC q=0.001')            | 0.689 |
| ('CCVR', 'OC q=0.01')             | 0.545 |
| ('CCVR', 'OC-own q=0.001')        | 0.66  |
| ('CCVR', 'argmax')                | 0.515 |
| ('Central-bal', 'OC q=0.0001')    | 0.785 |
| ('Central-bal', 'OC q=0.001')     | 0.743 |
| ('Central-bal', 'OC q=0.01')      | 0.65  |
| ('Central-bal', 'OC-own q=0.001') | 0.767 |
| ('Central-bal', 'argmax')         | 0.807 |
| ('FedAvg-bal', 'OC q=0.0001')     | 0.095 |
| ('FedAvg-bal', 'OC q=0.001')      | 0.143 |
| ('FedAvg-bal', 'OC q=0.01')       | 0.171 |
| ('FedAvg-bal', 'OC-own q=0.001')  | 0.111 |
| ('FedAvg-bal', 'argmax')          | 0.025 |
| ('GB+CR', 'OC q=0.0001')          | 0.495 |
| ('GB+CR', 'OC q=0.001')           | 0.512 |
| ('GB+CR', 'OC q=0.01')            | 0.46  |
| ('GB+CR', 'OC-own q=0.001')       | 0.508 |
| ('GB+CR', 'argmax')               | 0.47  | 

## ton, arm=e1, alpha=0.5: rare-class F1 (seed mean)

|                                   |    20 |
|:----------------------------------|------:|
| ('Central-bal', 'OC q=0.0001')    | 0.781 |
| ('Central-bal', 'OC q=0.001')     | 0.696 |
| ('Central-bal', 'OC q=0.01')      | 0.634 |
| ('Central-bal', 'OC-own q=0.001') | 0.727 |
| ('Central-bal', 'argmax')         | 0.777 |
| ('FedAvg-bal', 'OC q=0.0001')     | 0.196 |
| ('FedAvg-bal', 'OC q=0.001')      | 0.219 |
| ('FedAvg-bal', 'OC q=0.01')       | 0.269 |
| ('FedAvg-bal', 'OC-own q=0.001')  | 0.199 |
| ('FedAvg-bal', 'argmax')          | 0.048 |
| ('GB+CR', 'OC q=0.0001')          | 0.483 |
| ('GB+CR', 'OC q=0.001')           | 0.545 |
| ('GB+CR', 'OC q=0.01')            | 0.453 |
| ('GB+CR', 'OC-own q=0.001')       | 0.542 |
| ('GB+CR', 'argmax')               | 0.41  | 

## ton, arm=primary, alpha=0.3: rare-class F1 (seed mean)

|                                   |    20 |
|:----------------------------------|------:|
| ('CCVR', 'OC q=0.0001')           | 0.467 |
| ('CCVR', 'OC q=0.001')            | 0.69  |
| ('CCVR', 'OC q=0.01')             | 0.541 |
| ('CCVR', 'OC-own q=0.001')        | 0.646 |
| ('CCVR', 'argmax')                | 0.561 |
| ('Central-bal', 'OC q=0.0001')    | 0.812 |
| ('Central-bal', 'OC q=0.001')     | 0.728 |
| ('Central-bal', 'OC q=0.01')      | 0.639 |
| ('Central-bal', 'OC-own q=0.001') | 0.785 |
| ('Central-bal', 'argmax')         | 0.828 |
| ('FedAvg', 'OC q=0.0001')         | 0.181 |
| ('FedAvg', 'OC q=0.001')          | 0.198 |
| ('FedAvg', 'OC q=0.01')           | 0.193 |
| ('FedAvg', 'OC-own q=0.001')      | 0.201 |
| ('FedAvg', 'argmax')              | 0.082 |
| ('FedAvg-bal', 'OC q=0.0001')     | 0.209 |
| ('FedAvg-bal', 'OC q=0.001')      | 0.231 |
| ('FedAvg-bal', 'OC q=0.01')       | 0.233 |
| ('FedAvg-bal', 'OC-own q=0.001')  | 0.206 |
| ('FedAvg-bal', 'argmax')          | 0.086 |
| ('FedLC', 'OC q=0.0001')          | 0.248 |
| ('FedLC', 'OC q=0.001')           | 0.274 |
| ('FedLC', 'OC q=0.01')            | 0.285 |
| ('FedLC', 'OC-own q=0.001')       | 0.257 |
| ('FedLC', 'argmax')               | 0.149 |
| ('FedProx-bal', 'OC q=0.0001')    | 0.476 |
| ('FedProx-bal', 'OC q=0.001')     | 0.512 |
| ('FedProx-bal', 'OC q=0.01')      | 0.457 |
| ('FedProx-bal', 'OC-own q=0.001') | 0.502 |
| ('FedProx-bal', 'argmax')         | 0.39  |
| ('FedRS', 'OC q=0.0001')          | 0.177 |
| ('FedRS', 'OC q=0.001')           | 0.203 |
| ('FedRS', 'OC q=0.01')            | 0.182 |
| ('FedRS', 'OC-own q=0.001')       | 0.178 |
| ('FedRS', 'argmax')               | 0.069 |
| ('GB+CR', 'OC q=0.0001')          | 0.565 |
| ('GB+CR', 'OC q=0.001')           | 0.559 |
| ('GB+CR', 'OC q=0.01')            | 0.476 |
| ('GB+CR', 'OC-own q=0.001')       | 0.551 |
| ('GB+CR', 'argmax')               | 0.555 | 

## ton, arm=primary, alpha=0.5: rare-class F1 (seed mean)

|                                   |     5 |    20 |   100 |
|:----------------------------------|------:|------:|------:|
| ('CCVR', 'OC q=0.0001')           | 0.473 | 0.45  | 0.491 |
| ('CCVR', 'OC q=0.001')            | 0.576 | 0.648 | 0.667 |
| ('CCVR', 'OC q=0.01')             | 0.485 | 0.527 | 0.554 |
| ('CCVR', 'OC-own q=0.001')        | 0.545 | 0.632 | 0.635 |
| ('CCVR', 'argmax')                | 0.531 | 0.549 | 0.551 |
| ('Central-bal', 'OC q=0.0001')    | 0.627 | 0.777 | 0.831 |
| ('Central-bal', 'OC q=0.001')     | 0.57  | 0.701 | 0.711 |
| ('Central-bal', 'OC q=0.01')      | 0.513 | 0.599 | 0.564 |
| ('Central-bal', 'OC-own q=0.001') | 0.567 | 0.74  | 0.776 |
| ('Central-bal', 'argmax')         | 0.614 | 0.787 | 0.831 |
| ('FedAvg', 'OC q=0.0001')         | 0.164 | 0.073 | 0.108 |
| ('FedAvg', 'OC q=0.001')          | 0.187 | 0.094 | 0.119 |
| ('FedAvg', 'OC q=0.01')           | 0.192 | 0.111 | 0.139 |
| ('FedAvg', 'OC-own q=0.001')      | 0.182 | 0.095 | 0.107 |
| ('FedAvg', 'argmax')              | 0.046 | 0.025 | 0.022 |
| ('FedAvg-bal', 'OC q=0.0001')     | 0.103 | 0.102 | 0.049 |
| ('FedAvg-bal', 'OC q=0.001')      | 0.117 | 0.148 | 0.072 |
| ('FedAvg-bal', 'OC q=0.01')       | 0.135 | 0.172 | 0.107 |
| ('FedAvg-bal', 'OC-own q=0.001')  | 0.115 | 0.121 | 0.057 |
| ('FedAvg-bal', 'argmax')          | 0.029 | 0.028 | 0.016 |
| ('FedLC', 'OC q=0.0001')          | 0.207 | 0.174 | 0.21  |
| ('FedLC', 'OC q=0.001')           | 0.235 | 0.204 | 0.241 |
| ('FedLC', 'OC q=0.01')            | 0.252 | 0.234 | 0.262 |
| ('FedLC', 'OC-own q=0.001')       | 0.221 | 0.194 | 0.234 |
| ('FedLC', 'argmax')               | 0.128 | 0.109 | 0.07  |
| ('FedProx-bal', 'OC q=0.0001')    | 0.312 | 0.364 | 0.387 |
| ('FedProx-bal', 'OC q=0.001')     | 0.347 | 0.442 | 0.437 |
| ('FedProx-bal', 'OC q=0.01')      | 0.326 | 0.418 | 0.449 |
| ('FedProx-bal', 'OC-own q=0.001') | 0.335 | 0.405 | 0.431 |
| ('FedProx-bal', 'argmax')         | 0.228 | 0.202 | 0.238 |
| ('FedRS', 'OC q=0.0001')          | 0.133 | 0.06  | 0.093 |
| ('FedRS', 'OC q=0.001')           | 0.122 | 0.071 | 0.11  |
| ('FedRS', 'OC q=0.01')            | 0.145 | 0.083 | 0.127 |
| ('FedRS', 'OC-own q=0.001')       | 0.112 | 0.07  | 0.109 |
| ('FedRS', 'argmax')               | 0.072 | 0.034 | 0.055 |
| ('GB+CR', 'OC q=0.0001')          | 0.322 | 0.429 | 0.417 |
| ('GB+CR', 'OC q=0.001')           | 0.371 | 0.468 | 0.445 |
| ('GB+CR', 'OC q=0.01')            | 0.341 | 0.4   | 0.422 |
| ('GB+CR', 'OC-own q=0.001')       | 0.36  | 0.446 | 0.441 |
| ('GB+CR', 'argmax')               | 0.255 | 0.382 | 0.372 | 

## unsw, arm=big, alpha=0.5: rare-class F1 (seed mean)

|                                   |    20 |
|:----------------------------------|------:|
| ('CCVR', 'OC q=0.0001')           | 0.121 |
| ('CCVR', 'OC q=0.001')            | 0.207 |
| ('CCVR', 'OC q=0.01')             | 0.111 |
| ('CCVR', 'OC-own q=0.001')        | 0.192 |
| ('CCVR', 'argmax')                | 0.154 |
| ('Central-bal', 'OC q=0.0001')    | 0.283 |
| ('Central-bal', 'OC q=0.001')     | 0.218 |
| ('Central-bal', 'OC q=0.01')      | 0.135 |
| ('Central-bal', 'OC-own q=0.001') | 0.27  |
| ('Central-bal', 'argmax')         | 0.323 |
| ('FedAvg-bal', 'OC q=0.0001')     | 0.097 |
| ('FedAvg-bal', 'OC q=0.001')      | 0.147 |
| ('FedAvg-bal', 'OC q=0.01')       | 0.135 |
| ('FedAvg-bal', 'OC-own q=0.001')  | 0.11  |
| ('FedAvg-bal', 'argmax')          | 0     |
| ('GB+CR', 'OC q=0.0001')          | 0.229 |
| ('GB+CR', 'OC q=0.001')           | 0.206 |
| ('GB+CR', 'OC q=0.01')            | 0.112 |
| ('GB+CR', 'OC-own q=0.001')       | 0.221 |
| ('GB+CR', 'argmax')               | 0.151 | 

## unsw, arm=e1, alpha=0.5: rare-class F1 (seed mean)

|                                   |    20 |
|:----------------------------------|------:|
| ('Central-bal', 'OC q=0.0001')    | 0.262 |
| ('Central-bal', 'OC q=0.001')     | 0.216 |
| ('Central-bal', 'OC q=0.01')      | 0.13  |
| ('Central-bal', 'OC-own q=0.001') | 0.278 |
| ('Central-bal', 'argmax')         | 0.288 |
| ('FedAvg-bal', 'OC q=0.0001')     | 0.113 |
| ('FedAvg-bal', 'OC q=0.001')      | 0.143 |
| ('FedAvg-bal', 'OC q=0.01')       | 0.132 |
| ('FedAvg-bal', 'OC-own q=0.001')  | 0.134 |
| ('FedAvg-bal', 'argmax')          | 0.021 |
| ('GB+CR', 'OC q=0.0001')          | 0.177 |
| ('GB+CR', 'OC q=0.001')           | 0.204 |
| ('GB+CR', 'OC q=0.01')            | 0.104 |
| ('GB+CR', 'OC-own q=0.001')       | 0.195 |
| ('GB+CR', 'argmax')               | 0.079 | 

## unsw, arm=primary, alpha=0.3: rare-class F1 (seed mean)

|                                   |    20 |
|:----------------------------------|------:|
| ('CCVR', 'OC q=0.0001')           | 0.086 |
| ('CCVR', 'OC q=0.001')            | 0.161 |
| ('CCVR', 'OC q=0.01')             | 0.109 |
| ('CCVR', 'OC-own q=0.001')        | 0.136 |
| ('CCVR', 'argmax')                | 0.146 |
| ('Central-bal', 'OC q=0.0001')    | 0.263 |
| ('Central-bal', 'OC q=0.001')     | 0.228 |
| ('Central-bal', 'OC q=0.01')      | 0.124 |
| ('Central-bal', 'OC-own q=0.001') | 0.261 |
| ('Central-bal', 'argmax')         | 0.353 |
| ('FedAvg', 'OC q=0.0001')         | 0.106 |
| ('FedAvg', 'OC q=0.001')          | 0.108 |
| ('FedAvg', 'OC q=0.01')           | 0.086 |
| ('FedAvg', 'OC-own q=0.001')      | 0.091 |
| ('FedAvg', 'argmax')              | 0     |
| ('FedAvg-bal', 'OC q=0.0001')     | 0.099 |
| ('FedAvg-bal', 'OC q=0.001')      | 0.102 |
| ('FedAvg-bal', 'OC q=0.01')       | 0.084 |
| ('FedAvg-bal', 'OC-own q=0.001')  | 0.084 |
| ('FedAvg-bal', 'argmax')          | 0     |
| ('FedLC', 'OC q=0.0001')          | 0.079 |
| ('FedLC', 'OC q=0.001')           | 0.184 |
| ('FedLC', 'OC q=0.01')            | 0.102 |
| ('FedLC', 'OC-own q=0.001')       | 0.152 |
| ('FedLC', 'argmax')               | 0     |
| ('FedProx-bal', 'OC q=0.0001')    | 0.198 |
| ('FedProx-bal', 'OC q=0.001')     | 0.194 |
| ('FedProx-bal', 'OC q=0.01')      | 0.118 |
| ('FedProx-bal', 'OC-own q=0.001') | 0.176 |
| ('FedProx-bal', 'argmax')         | 0.028 |
| ('FedRS', 'OC q=0.0001')          | 0.029 |
| ('FedRS', 'OC q=0.001')           | 0.069 |
| ('FedRS', 'OC q=0.01')            | 0.075 |
| ('FedRS', 'OC-own q=0.001')       | 0.045 |
| ('FedRS', 'argmax')               | 0     |
| ('GB+CR', 'OC q=0.0001')          | 0.166 |
| ('GB+CR', 'OC q=0.001')           | 0.201 |
| ('GB+CR', 'OC q=0.01')            | 0.109 |
| ('GB+CR', 'OC-own q=0.001')       | 0.162 |
| ('GB+CR', 'argmax')               | 0.12  | 

## unsw, arm=primary, alpha=0.5: rare-class F1 (seed mean)

|                                   |     5 |    20 |   100 |
|:----------------------------------|------:|------:|------:|
| ('CCVR', 'OC q=0.0001')           | 0.089 | 0.065 | 0.131 |
| ('CCVR', 'OC q=0.001')            | 0.148 | 0.148 | 0.215 |
| ('CCVR', 'OC q=0.01')             | 0.102 | 0.108 | 0.12  |
| ('CCVR', 'OC-own q=0.001')        | 0.111 | 0.118 | 0.141 |
| ('CCVR', 'argmax')                | 0.141 | 0.137 | 0.149 |
| ('Central-bal', 'OC q=0.0001')    | 0.224 | 0.262 | 0.286 |
| ('Central-bal', 'OC q=0.001')     | 0.196 | 0.215 | 0.245 |
| ('Central-bal', 'OC q=0.01')      | 0.121 | 0.125 | 0.123 |
| ('Central-bal', 'OC-own q=0.001') | 0.206 | 0.283 | 0.286 |
| ('Central-bal', 'argmax')         | 0.222 | 0.275 | 0.35  |
| ('FedAvg', 'OC q=0.0001')         | 0.073 | 0.06  | 0.11  |
| ('FedAvg', 'OC q=0.001')          | 0.1   | 0.12  | 0.127 |
| ('FedAvg', 'OC q=0.01')           | 0.095 | 0.115 | 0.098 |
| ('FedAvg', 'OC-own q=0.001')      | 0.063 | 0.084 | 0.11  |
| ('FedAvg', 'argmax')              | 0     | 0     | 0.001 |
| ('FedAvg-bal', 'OC q=0.0001')     | 0.082 | 0.063 | 0.079 |
| ('FedAvg-bal', 'OC q=0.001')      | 0.13  | 0.139 | 0.109 |
| ('FedAvg-bal', 'OC q=0.01')       | 0.103 | 0.12  | 0.106 |
| ('FedAvg-bal', 'OC-own q=0.001')  | 0.081 | 0.103 | 0.081 |
| ('FedAvg-bal', 'argmax')          | 0.013 | 0     | 0.001 |
| ('FedLC', 'OC q=0.0001')          | 0.079 | 0.046 | 0.091 |
| ('FedLC', 'OC q=0.001')           | 0.13  | 0.138 | 0.167 |
| ('FedLC', 'OC q=0.01')            | 0.091 | 0.12  | 0.104 |
| ('FedLC', 'OC-own q=0.001')       | 0.082 | 0.129 | 0.136 |
| ('FedLC', 'argmax')               | 0.033 | 0     | 0.007 |
| ('FedProx-bal', 'OC q=0.0001')    | 0.151 | 0.187 | 0.196 |
| ('FedProx-bal', 'OC q=0.001')     | 0.154 | 0.191 | 0.203 |
| ('FedProx-bal', 'OC q=0.01')      | 0.11  | 0.136 | 0.132 |
| ('FedProx-bal', 'OC-own q=0.001') | 0.134 | 0.187 | 0.186 |
| ('FedProx-bal', 'argmax')         | 0.036 | 0.018 | 0.044 |
| ('FedRS', 'OC q=0.0001')          | 0.046 | 0.029 | 0.06  |
| ('FedRS', 'OC q=0.001')           | 0.058 | 0.079 | 0.064 |
| ('FedRS', 'OC q=0.01')            | 0.043 | 0.054 | 0.047 |
| ('FedRS', 'OC-own q=0.001')       | 0.046 | 0.056 | 0.065 |
| ('FedRS', 'argmax')               | 0     | 0     | 0     |
| ('GB+CR', 'OC q=0.0001')          | 0.154 | 0.183 | 0.207 |
| ('GB+CR', 'OC q=0.001')           | 0.167 | 0.191 | 0.22  |
| ('GB+CR', 'OC q=0.01')            | 0.11  | 0.116 | 0.126 |
| ('GB+CR', 'OC-own q=0.001')       | 0.147 | 0.208 | 0.2   |
| ('GB+CR', 'argmax')               | 0.093 | 0.081 | 0.13  | 

## H1 gap: Central-bal argmax - best global FL argmax (rare F1 x100)

- ton k=5: +8.3 [+3.5, +13.0]
- ton k=20: +22.5 [+17.5, +27.0]
- ton k=100: +28.0 [+25.3, +30.8]
- unsw k=5: +7.0 [+3.0, +11.3]
- unsw k=20: +12.7 [+8.6, +16.1]
- unsw k=100: +18.1 [+14.5, +21.7]

**H1 ton: SUPPORTED**

**H1 unsw: SUPPORTED**

## H3 failure split (rare precision / recall, seed means)

- ton k=5: CCVR P 0.470 R 0.786; GB+CR P 0.549 R 0.218 -> yes
- ton k=20: CCVR P 0.477 R 0.886; GB+CR P 0.620 R 0.345 -> yes
- ton k=100: CCVR P 0.482 R 0.911; GB+CR P 0.603 R 0.330 -> yes
- unsw k=5: CCVR P 0.088 R 0.501; GB+CR P 0.174 R 0.103 -> yes
- unsw k=20: CCVR P 0.081 R 0.627; GB+CR P 0.290 R 0.055 -> yes
- unsw k=100: CCVR P 0.089 R 0.682; GB+CR P 0.274 R 0.113 -> yes

**H3: SUPPORTED**

## H4 OC vs argmax per model (rare F1 x100, pooled over k; harm checks)

- ton FedAvg-bal: +8.8 [+6.1, +11.2]; common F1 +0.58 pts; benign recall -0.0007 -> pass
- ton FedProx-bal: +18.6 [+16.7, +20.6]; common F1 +0.20 pts; benign recall -0.0058 -> fail
- ton FedLC: +12.4 [+10.9, +14.0]; common F1 +0.73 pts; benign recall -0.0032 -> fail
- ton FedRS: +4.7 [+3.0, +6.7]; common F1 +0.48 pts; benign recall -0.0004 -> pass
- ton CCVR: +8.7 [+6.5, +10.9]; common F1 +1.10 pts; benign recall +0.0755 -> pass
- ton GB+CR: +9.2 [+5.1, +13.3]; common F1 +0.07 pts; benign recall -0.0103 -> fail

**H4 ton: 3/6 models pass -> NOT supported**

- unsw FedAvg-bal: +12.1 [+10.3, +13.7]; common F1 -0.10 pts; benign recall -0.0001 -> pass
- unsw FedProx-bal: +15.0 [+12.2, +18.1]; common F1 -0.22 pts; benign recall -0.0000 -> pass
- unsw FedLC: +13.2 [+10.4, +15.6]; common F1 +0.10 pts; benign recall -0.0007 -> pass
- unsw FedRS: +6.7 [+4.6, +8.8]; common F1 -0.08 pts; benign recall -0.0015 -> pass
- unsw CCVR: +2.8 [+1.9, +3.7]; common F1 +3.09 pts; benign recall +0.0086 -> pass
- unsw GB+CR: +9.1 [+7.1, +11.3]; common F1 -0.34 pts; benign recall -0.0000 -> pass

**H4 unsw: 6/6 models pass -> SUPPORTED**

## P (primary claim): best fixed FL+OC model - best FL argmax per setting (rare F1 x100)

best fixed FL+OC model: CCVR (mean rare F1 0.400)

- ton k=5: +4.6 [+1.6, +7.7]; gap closed 55%; H5 residual +3.8 [-1.6, +9.6]
- ton k=20: +8.5 [+4.2, +13.0]; gap closed 38%; H5 residual +13.9 [+10.5, +17.8]
- ton k=100: +11.6 [+8.2, +15.0]; gap closed 41%; H5 residual +16.4 [+11.4, +21.4]
- unsw k=5: -0.4 [-2.7, +1.9]; gap closed -6%; H5 residual +7.5 [+2.4, +12.8]
- unsw k=20: +0.0 [-2.2, +2.3]; gap closed 0%; H5 residual +12.7 [+8.6, +16.9]
- unsw k=100: +4.6 [+1.5, +7.0]; gap closed 25%; H5 residual +13.5 [+10.9, +15.8]

**P: NOT supported**

## H2 under-training confound: (Central - FedAvg-bal) common F1 gap at E=1 minus at E=5 (x100)

- ton: +1.8 [-1.8, +5.1] -> NOT supported
- unsw: +3.1 [+0.9, +5.9] -> SUPPORTED

## Owner view (owner's own class F1, primary alpha=0.5)

|               |   FedRep |   Local-owner-bal |
|:--------------|---------:|------------------:|
| ('ton', 5)    |    0.535 |             0.632 |
| ('ton', 20)   |    0.647 |             0.712 |
| ('ton', 100)  |    0.574 |             0.657 |
| ('unsw', 5)   |    0.212 |             0.215 |
| ('unsw', 20)  |    0.238 |             0.248 |
| ('unsw', 100) |    0.231 |             0.246 |

## Sensitivity (rare F1, primary alpha=0.5, pooled over k): OC variants

|                            |   CCVR |   Central-bal |   FedAvg |   FedAvg-bal |   FedLC |   FedProx-bal |   FedRS |   GB+CR |
|:---------------------------|-------:|--------------:|---------:|-------------:|--------:|--------------:|--------:|--------:|
| ('ton', 'OC q=0.0001')     |  0.471 |         0.745 |    0.115 |        0.084 |   0.197 |         0.355 |   0.096 |   0.39  |
| ('ton', 'OC q=0.001')      |  0.631 |         0.661 |    0.133 |        0.112 |   0.227 |         0.409 |   0.101 |   0.428 |
| ('ton', 'OC q=0.01')       |  0.522 |         0.559 |    0.147 |        0.138 |   0.249 |         0.397 |   0.118 |   0.388 |
| ('ton', 'OC-own q=0.001')  |  0.604 |         0.694 |    0.128 |        0.098 |   0.216 |         0.391 |   0.097 |   0.416 |
| ('ton', 'argmax')          |  0.544 |         0.744 |    0.031 |        0.024 |   0.103 |         0.223 |   0.054 |   0.336 |
| ('unsw', 'OC q=0.0001')    |  0.095 |         0.257 |    0.081 |        0.075 |   0.072 |         0.178 |   0.045 |   0.181 |
| ('unsw', 'OC q=0.001')     |  0.17  |         0.219 |    0.116 |        0.126 |   0.145 |         0.183 |   0.067 |   0.193 |
| ('unsw', 'OC q=0.01')      |  0.11  |         0.123 |    0.103 |        0.11  |   0.105 |         0.126 |   0.048 |   0.117 |
| ('unsw', 'OC-own q=0.001') |  0.123 |         0.258 |    0.086 |        0.088 |   0.115 |         0.169 |   0.056 |   0.185 |
| ('unsw', 'argmax')         |  0.143 |         0.282 |    0     |        0.005 |   0.013 |         0.033 |   0     |   0.101 |
