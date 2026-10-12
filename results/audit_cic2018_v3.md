# NF-CSE-CIC-IDS2018-v3 audit

rows 20,115,529; time 2018-02-14 12:28:07.705000 to 2018-03-02 20:04:25.524000; days 11

## Class counts by global time-ordered split (unusable: classes fall in disjoint periods)

| Attack                   |    train |     val |    test |    total |
|:-------------------------|---------:|--------:|--------:|---------:|
| SQL_Injection            |      440 |       0 |       0 |      440 |
| Brute_Force_-XSS         |      480 |       0 |       0 |      480 |
| Brute_Force_-Web         |     1618 |       0 |       0 |     1618 |
| DDOS_attack-LOIC-UDP     |     3450 |       0 |       0 |     3450 |
| DoS_attacks-Slowloris    |    36040 |       0 |       0 |    36040 |
| DoS_attacks-GoldenEye    |    61300 |       0 |       0 |    61300 |
| DoS_attacks-Hulk         |   100076 |       0 |       0 |   100076 |
| DoS_attacks-SlowHTTPTest |   105550 |       0 |       0 |   105550 |
| Infilteration            |        0 |   83880 |  104272 |   188152 |
| SSH-Bruteforce           |   188474 |       0 |       0 |   188474 |
| Bot                      |        0 |       0 |  207703 |   207703 |
| DDoS_attacks-LOIC-HTTP   |   288589 |       0 |       0 |   288589 |
| FTP-BruteForce           |   386720 |       0 |       0 |   386720 |
| DDOS_attack-HOIC         |  1032311 |       0 |       0 |  1032311 |
| Benign                   | 11875822 | 1927673 | 3711131 | 17514626 | 

## Per class: first/last day, top source IP share, number of source IPs

| cls                      | first      | last       |   n_src | top_src        |   top_src_share |   top_dst_share |
|:-------------------------|:-----------|:-----------|--------:|:---------------|----------------:|----------------:|
| Benign                   | 2018-02-14 | 2018-03-02 |  181876 | 5.101.40.105   |           0.008 |           0.412 |
| Bot                      | 2018-03-02 | 2018-03-02 |  181876 | 172.31.69.10   |           0.152 |           1     |
| Brute_Force_-Web         | 2018-02-22 | 2018-02-22 |  181876 | 18.218.115.60  |           0.071 |           1     |
| Brute_Force_-XSS         | 2018-02-22 | 2018-02-22 |  181876 | 52.14.77.172   |           0.415 |           0.917 |
| DDOS_attack-HOIC         | 2018-02-21 | 2018-02-21 |  181876 | 18.216.200.189 |           0.101 |           1     |
| DDOS_attack-LOIC-UDP     | 2018-02-21 | 2018-02-21 |  181876 | 18.218.55.126  |           0.107 |           1     |
| DDoS_attacks-LOIC-HTTP   | 2018-02-20 | 2018-02-20 |  181876 | 18.219.9.1     |           0.102 |           1     |
| DoS_attacks-GoldenEye    | 2018-02-15 | 2018-02-15 |  181876 | 18.219.211.138 |           1     |           1     |
| DoS_attacks-Hulk         | 2018-02-16 | 2018-02-16 |  181876 | 18.219.193.20  |           1     |           1     |
| DoS_attacks-SlowHTTPTest | 2018-02-16 | 2018-02-16 |  181876 | 13.59.126.31   |           1     |           1     |
| DoS_attacks-Slowloris    | 2018-02-15 | 2018-02-15 |  181876 | 18.217.165.70  |           1     |           1     |
| FTP-BruteForce           | 2018-02-14 | 2018-02-14 |  181876 | 18.221.219.4   |           1     |           1     |
| Infilteration            | 2018-02-28 | 2018-03-01 |  181876 | 172.31.69.13   |           0.246 |           0.549 |
| SQL_Injection            | 2018-02-22 | 2018-02-22 |  181876 | 13.58.42.57    |           0.264 |           1     |
| SSH-Bruteforce           | 2018-02-14 | 2018-02-14 |  181876 | 13.58.98.64    |           1     |           1     | 

## Per-class split: day ranges of train and test per class

| Attack                   | ('min', 'test')   | ('min', 'train')   | ('min', 'val')   | ('max', 'test')   | ('max', 'train')   | ('max', 'val')   |
|:-------------------------|:------------------|:-------------------|:-----------------|:------------------|:-------------------|:-----------------|
| Benign                   | 03-01             | 02-14              | 02-28            | 03-02             | 02-28              | 03-01            |
| Bot                      | 03-02             | 03-02              | 03-02            | 03-02             | 03-02              | 03-02            |
| Brute_Force_-Web         | 02-22             | 02-22              | 02-22            | 02-22             | 02-22              | 02-22            |
| Brute_Force_-XSS         | 02-22             | 02-22              | 02-22            | 02-22             | 02-22              | 02-22            |
| DDOS_attack-HOIC         | 02-21             | 02-21              | 02-21            | 02-21             | 02-21              | 02-21            |
| DDOS_attack-LOIC-UDP     | 02-21             | 02-21              | 02-21            | 02-21             | 02-21              | 02-21            |
| DDoS_attacks-LOIC-HTTP   | 02-20             | 02-20              | 02-20            | 02-20             | 02-20              | 02-20            |
| DoS_attacks-GoldenEye    | 02-15             | 02-15              | 02-15            | 02-15             | 02-15              | 02-15            |
| DoS_attacks-Hulk         | 02-16             | 02-16              | 02-16            | 02-16             | 02-16              | 02-16            |
| DoS_attacks-SlowHTTPTest | 02-16             | 02-16              | 02-16            | 02-16             | 02-16              | 02-16            |
| DoS_attacks-Slowloris    | 02-15             | 02-15              | 02-15            | 02-15             | 02-15              | 02-15            |
| FTP-BruteForce           | 02-14             | 02-14              | 02-14            | 02-14             | 02-14              | 02-14            |
| Infilteration            | 03-01             | 02-28              | 03-01            | 03-01             | 03-01              | 03-01            |
| SQL_Injection            | 02-22             | 02-22              | 02-22            | 02-22             | 02-22              | 02-22            |
| SSH-Bruteforce           | 02-14             | 02-14              | 02-14            | 02-14             | 02-14              | 02-14            | 

## Single-feature balanced accuracy (depth-3 tree, train period -> test period, stratified sample)

| feature                   |   binary |   multi |
|:--------------------------|---------:|--------:|
| L7_PROTO                  |    0.902 |   0.269 |
| L4_DST_PORT               |    0.841 |   0.27  |
| LONGEST_FLOW_PKT          |    0.838 |   0.329 |
| MAX_IP_PKT_LEN            |    0.838 |   0.329 |
| TCP_WIN_MAX_IN            |    0.809 |   0.276 |
| TCP_WIN_MAX_OUT           |    0.807 |   0.248 |
| SERVER_TCP_FLAGS          |    0.777 |   0.286 |
| OUT_BYTES                 |    0.773 |   0.458 |
| NUM_PKTS_UP_TO_128_BYTES  |    0.758 |   0.315 |
| IN_PKTS                   |    0.746 |   0.313 |
| OUT_PKTS                  |    0.742 |   0.341 |
| DST_TO_SRC_AVG_THROUGHPUT |    0.74  |   0.396 |
| IN_BYTES                  |    0.738 |   0.312 |
| MAX_TTL                   |    0.715 |   0.362 |
| MIN_TTL                   |    0.715 |   0.362 |
| TCP_FLAGS                 |    0.712 |   0.267 |
| MIN_IP_PKT_LEN            |    0.7   |   0.241 |
| SRC_TO_DST_AVG_THROUGHPUT |    0.7   |   0.379 |
| CLIENT_TCP_FLAGS          |    0.697 |   0.26  |
| NUM_PKTS_128_TO_256_BYTES |    0.697 |   0.224 | 

classes in test sample: ['Benign', 'Bot', 'Brute_Force_-Web', 'Brute_Force_-XSS', 'DDOS_attack-HOIC', 'DDOS_attack-LOIC-UDP', 'DDoS_attacks-LOIC-HTTP', 'DoS_attacks-GoldenEye', 'DoS_attacks-Hulk', 'DoS_attacks-SlowHTTPTest', 'DoS_attacks-Slowloris', 'FTP-BruteForce', 'Infilteration', 'SQL_Injection', 'SSH-Bruteforce']

## Exact duplicates

share of sampled test rows whose full feature vector (incl. timestamps) occurs in sampled train: 0.000

same without timestamps: 0.200

## Plan v3 Part F rules

capture days 11; days spanned per class: {'Benign': 11, 'Bot': 1, 'Brute_Force_-Web': 1, 'Brute_Force_-XSS': 1, 'DDOS_attack-HOIC': 1, 'DDOS_attack-LOIC-UDP': 1, 'DDoS_attacks-LOIC-HTTP': 1, 'DoS_attacks-GoldenEye': 1, 'DoS_attacks-Hulk': 1, 'DoS_attacks-SlowHTTPTest': 1, 'DoS_attacks-Slowloris': 1, 'FTP-BruteForce': 1, 'Infilteration': 2, 'SQL_Injection': 1, 'SSH-Bruteforce': 1}
split: per-class chronological
rare (4 smallest attack classes with >= 100 flows): ['SQL_Injection', 'Brute_Force_-XSS', 'Brute_Force_-Web', 'DDOS_attack-LOIC-UDP']
common (up to 5 largest remaining): ['DDOS_attack-HOIC', 'FTP-BruteForce', 'DDoS_attacks-LOIC-HTTP', 'Bot', 'SSH-Bruteforce']
dropped by the 0.99 rule (binary single-feature balanced accuracy > 0.99): []
