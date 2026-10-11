"""Confound check for pilots 1-3: is FL just under-trained relative to the centralised reference?
Re-runs pilot 3 with E local epochs per round and R rounds (centralised gets R epochs).
Usage: python3 pilot3b_longer.py E R OUT
"""
import functools
import sys
import time

import numpy as np
import pandas as pd

import pilot_fl
import pilot3_fl

E, R, OUT = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
pilot3_fl.ROUNDS = R
pilot3_fl.local_train = functools.partial(pilot_fl.local_train, epochs=E)
t0 = time.time(); log = lambda s: print(f"[{time.time() - t0:6.0f}s] {s}", flush=True)
X, y, part, _ = pilot_fl.load(); rows = []
for alpha in (0.1, 0.5):
    for k in (20, 100):
        log(f"alpha={alpha} k={k}")
        rows += pilot3_fl.run(X, y, part, 0, alpha, k, log)
        pd.DataFrame(rows).to_csv(OUT, index=False)
log("finished")
