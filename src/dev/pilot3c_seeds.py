"""User-requested check (10 Oct 2026): repeat GB+CR+OW with 5 seeds at the longer budget (E=5, R=60),
alpha = 0.5 (where common classes reach centralised level), k in {20, 100}.
Methods: FedAvg-bal (+CCVR), GB+CR, GB+CR+OW, Central-bal. One process per seed.
Usage: python3 pilot3c_seeds.py SEED OUT
"""
import functools
import sys
import time

import pandas as pd

import pilot_fl
import pilot3_fl

SEED, OUT = int(sys.argv[1]), sys.argv[2]
pilot3_fl.ROUNDS = 60
pilot3_fl.local_train = functools.partial(pilot_fl.local_train, epochs=5)
t0 = time.time(); log = lambda s: print(f"[{time.time() - t0:6.0f}s] {s}", flush=True)
X, y, part, _ = pilot_fl.load(); rows = []
for k in (20, 100):
    log(f"seed={SEED} alpha=0.5 k={k}")
    rows += pilot3_fl.run(X, y, part, SEED, 0.5, k, log, methods={"FedAvg-bal", "GB+CR", "GB+CR+OW"})
    pd.DataFrame(rows).to_csv(OUT, index=False)
log("finished")
