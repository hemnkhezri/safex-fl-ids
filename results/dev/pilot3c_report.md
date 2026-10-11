# 5-seed repeat: E=5, R=60, alpha=0.5 (seeds: [np.int64(0), np.int64(1), np.int64(2), np.int64(3), np.int64(4)] )

## Rare-class F1 / precision / recall (mean over 4 rare classes and seeds)

| method      |   ('f1', 20) |   ('f1', 100) |   ('precision', 20) |   ('precision', 100) |   ('recall', 20) |   ('recall', 100) |
|:------------|-------------:|--------------:|--------------------:|---------------------:|-----------------:|------------------:|
| CCVR        |        0.141 |         0.146 |               0.085 |                0.086 |            0.623 |             0.659 |
| Central-bal |        0.341 |         0.358 |               0.399 |                0.317 |            0.439 |             0.542 |
| FedAvg-bal  |        0     |         0     |               0     |                0     |            0     |             0     |
| GB+CR       |        0.061 |         0.091 |               0.253 |                0.243 |            0.038 |             0.066 |
| GB+CR+OW    |        0.099 |         0.092 |               0.227 |                0.268 |            0.066 |             0.074 | 

## Common attack classes F1

|   k |   CCVR |   Central-bal |   FedAvg-bal |   GB+CR |   GB+CR+OW |
|----:|-------:|--------------:|-------------:|--------:|-----------:|
|  20 |  0.438 |         0.525 |        0.485 |   0.487 |      0.5   |
| 100 |  0.445 |         0.532 |        0.488 |   0.491 |      0.506 | 

## Benign recall

|   k |   CCVR |   Central-bal |   FedAvg-bal |   GB+CR |   GB+CR+OW |
|----:|-------:|--------------:|-------------:|--------:|-----------:|
|  20 |  0.995 |        0.9997 |       0.9998 |  0.9998 |     0.9998 |
| 100 |  0.993 |        0.9997 |       0.9997 |  0.9997 |     0.9997 | 

## Paired differences in rare-class F1 (x100), 95% CI bootstrap over seeds

- k=20 OW_vs_FAbal: +9.9 [+6.0, +13.7]
- k=20 OW_vs_CR: +3.8 [+0.7, +6.1]
- k=20 OW_vs_CCVR: -4.3 [-8.5, +0.2]
- k=20 gap_central: +15.9 [+11.6, +20.6]
- k=100 OW_vs_FAbal: +9.2 [+5.5, +13.3]
- k=100 OW_vs_CR: +0.1 [-3.8, +3.8]
- k=100 OW_vs_CCVR: -5.4 [-8.0, -1.8]
- k=100 gap_central: +13.2 [+6.8, +19.4]

## Per seed rare F1 (GB+CR+OW)

|   k |     0 |     1 |     2 |     3 |     4 |
|----:|------:|------:|------:|------:|------:|
|  20 | 0.098 | 0.009 | 0.194 | 0.12  | 0.072 |
| 100 | 0.045 | 0.14  | 0.013 | 0.106 | 0.154 |

## Interpretation (development, not sealed)

- Encoder weights a_i (results/encoder_weights_a_i.csv): owners get only 1.2-1.5x their size weight at alpha=0.5; rare classes are 5-13% of the owner's balanced mass. Step 3 (OW) is a weak lever by construction.
- OW signal: +3.8 F1 points over GB+CR at k=20 (CI [+0.7, +6.1], barely above 0), +0.1 at k=100 (CI spans 0). Per-seed rare F1 of GB+CR+OW ranges 0.01-0.19. Not a robust effect; drop OW as a contribution.
- GB+CR+OW is worse than CCVR in rare F1 (-4.3 and -5.4 points). The two fail in opposite ways: CCVR recall ~0.64 / precision ~0.09; GB+CR(+OW) precision ~0.23-0.27 / recall ~0.07.
- FedAvg-bal rare F1 = 0 at E=5 (local epochs erase classes the client does not hold).
- Gap to Central-bal stays large and its CI excludes 0: +15.9 [+11.6, +20.6] at k=20, +13.2 [+6.8, +19.4] at k=100.
- Implication: the precision/recall split means step 4 (owner-calibrated threshold on the rare logit) is the only remaining lever worth one development test before sealing.
