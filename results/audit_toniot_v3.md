# NF-ToN-IoT-v3 audit

rows 27,520,260; time 2019-04-23 14:09:50.618000 to 2019-04-29 14:45:55.177000; days 7

## Class counts by global time-ordered split (unusable: classes fall in disjoint periods)

| Attack     |    train |     val |    test |    total |
|:-----------|---------:|--------:|--------:|---------:|
| ransomware |        0 |       0 |    3971 |     3971 |
| mitm       |        0 |       0 |    6013 |     6013 |
| Backdoor   |        0 |       0 |  203384 |   203384 |
| dos        |   203456 |       0 |       0 |   203456 |
| injection  |   381777 |       0 |       0 |   381777 |
| scanning   |  1358977 |       0 |       0 |  1358977 |
| password   |        0 | 1594777 |       0 |  1594777 |
| xss        |        0 |   31319 | 2803116 |  2834435 |
| ddos       |  3674745 |  466511 |       0 |  4141256 |
| Benign     | 13645227 |  659419 | 2487568 | 16792214 | 

## Per class: first/last day, top source IP share, number of source IPs

| cls        | first      | last       |   n_src | top_src       |   top_src_share |   top_dst_share |
|:-----------|:-----------|:-----------|--------:|:--------------|----------------:|----------------:|
| Backdoor   | 2019-04-28 | 2019-04-29 |       4 | 192.168.1.193 |           0.998 |           0.841 |
| Benign     | 2019-04-23 | 2019-04-29 |   15268 | 192.168.1.32  |           0.217 |           0.143 |
| ddos       | 2019-04-25 | 2019-04-26 |       6 | 192.168.1.31  |           0.455 |           0.634 |
| dos        | 2019-04-24 | 2019-04-25 |       7 | 192.168.1.30  |           0.509 |           0.464 |
| injection  | 2019-04-25 | 2019-04-25 |       8 | 192.168.1.36  |           0.392 |           0.198 |
| mitm       | 2019-04-29 | 2019-04-29 |       2 | 192.168.1.31  |           0.71  |           0.778 |
| password   | 2019-04-26 | 2019-04-27 |       7 | 192.168.1.32  |           0.648 |           0.659 |
| ransomware | 2019-04-28 | 2019-04-28 |       3 | 192.168.1.33  |           0.569 |           0.94  |
| scanning   | 2019-04-23 | 2019-04-24 |      17 | 192.168.1.32  |           0.508 |           0.121 |
| xss        | 2019-04-27 | 2019-04-27 |       5 | 192.168.1.35  |           0.446 |           0.439 | 

## Per-class split: day ranges of train and test per class

| Attack     | ('min', 'test')   | ('min', 'train')   | ('min', 'val')   | ('max', 'test')   | ('max', 'train')   | ('max', 'val')   |
|:-----------|:------------------|:-------------------|:-----------------|:------------------|:-------------------|:-----------------|
| Backdoor   | 04-29             | 04-28              | 04-29            | 04-29             | 04-29              | 04-29            |
| Benign     | 04-26             | 04-23              | 04-25            | 04-29             | 04-25              | 04-26            |
| ddos       | 04-26             | 04-25              | 04-26            | 04-26             | 04-26              | 04-26            |
| dos        | 04-25             | 04-24              | 04-25            | 04-25             | 04-25              | 04-25            |
| injection  | 04-25             | 04-25              | 04-25            | 04-25             | 04-25              | 04-25            |
| mitm       | 04-29             | 04-29              | 04-29            | 04-29             | 04-29              | 04-29            |
| password   | 04-27             | 04-26              | 04-27            | 04-27             | 04-27              | 04-27            |
| ransomware | 04-28             | 04-28              | 04-28            | 04-28             | 04-28              | 04-28            |
| scanning   | 04-24             | 04-23              | 04-24            | 04-24             | 04-24              | 04-24            |
| xss        | 04-27             | 04-27              | 04-27            | 04-27             | 04-27              | 04-27            | 

## Single-feature balanced accuracy (depth-3 tree, train period -> test period, stratified sample)

| feature                    |   binary |   multi |
|:---------------------------|---------:|--------:|
| L4_DST_PORT                |    0.829 |   0.415 |
| L4_SRC_PORT                |    0.822 |   0.249 |
| SERVER_TCP_FLAGS           |    0.814 |   0.327 |
| OUT_BYTES                  |    0.794 |   0.317 |
| SRC_TO_DST_AVG_THROUGHPUT  |    0.78  |   0.449 |
| DST_TO_SRC_AVG_THROUGHPUT  |    0.776 |   0.381 |
| NUM_PKTS_UP_TO_128_BYTES   |    0.776 |   0.281 |
| MAX_TTL                    |    0.77  |   0.336 |
| MIN_TTL                    |    0.77  |   0.336 |
| MIN_IP_PKT_LEN             |    0.767 |   0.304 |
| IN_PKTS                    |    0.76  |   0.326 |
| FLOW_DURATION_MILLISECONDS |    0.737 |   0.299 |
| SHORTEST_FLOW_PKT          |    0.721 |   0.352 |
| DURATION_IN                |    0.72  |   0.314 |
| SRC_TO_DST_IAT_MAX         |    0.702 |   0.401 |
| SRC_TO_DST_IAT_AVG         |    0.694 |   0.364 |
| DURATION_OUT               |    0.688 |   0.299 |
| OUT_PKTS                   |    0.683 |   0.239 |
| DST_TO_SRC_SECOND_BYTES    |    0.681 |   0.342 |
| DST_TO_SRC_IAT_AVG         |    0.68  |   0.345 | 

classes in test sample: ['Backdoor', 'Benign', 'ddos', 'dos', 'injection', 'mitm', 'password', 'ransomware', 'scanning', 'xss']

## Exact duplicates

share of sampled test rows whose full feature vector (incl. timestamps) occurs in sampled train: 0.000

same without timestamps: 0.042
