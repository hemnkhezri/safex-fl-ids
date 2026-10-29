"""Pilot 9 (development seeds 0-4 only; exploratory, no claims): SAFE-X with a federated feedback loop.
Analysts label every alarm (as in Study 5's ACI). After each of W time windows of the test stream, the labelled
alarms are used to fine-tune the shared expert by FedAvg: each client trains on the alarms raised on its own
traffic (false alarms as negatives with their true class, confirmed rare flows as new positives), replaying a
sample of its own training flows; the owner also replays its labelled rare flows. The threshold is then
recalibrated on all clients' non-rare training flows (federated calibration) and ACI continues.
Variants (same expert initialisation, paired):
  static   SAFE-X + ACI, expert never updated (Study 5)
  loop     feedback loop with false alarms and confirmed positives
  loopneg  feedback loop with false alarms only (no new positives)
GB+CR and FedOV(-full) test/cal logits are read from the pilot 8 unit of the same dataset and seed; the test set is
rebuilt with the same random stream and checked against it.
Usage: python3 pilot9_loop.py DATASET SEED P8DIR OUTDIR
"""
from __future__ import annotations

import os
import sys
import time

import numpy as np
import pandas as pd

import conf_fl
import pilot2_fl
import pilot_fl
import s3_unit
import s4_unit

K, K_SHOTS, ALPHA, Q, G = 10, 20, 0.5, 1e-3, 0.005
W, FT_ROUNDS, FT_EPOCHS, REPLAY = 10, int(os.environ.get("P9_ROUNDS", 5)), int(os.environ.get("P9_EPOCHS", 1)), 3000
UPW = int(os.environ.get("P9_UPWEIGHT", 1))  # repeat labelled alarms this many times in local data


def aci_window(s, bad, cal_sorted, a):
    """ACI over one window in time order; bad[t] tells whether an alarm at t would be false. Returns alarms, excess, alpha."""
    n = len(cal_sorted); alarm = np.zeros(len(s), bool); ex = np.zeros(len(s), np.float32)
    for t in range(len(s)):
        tau = np.inf if a <= 0 else (-np.inf if a >= 1 else cal_sorted[min(n - 1, int(np.floor((1 - a) * n)))])
        hit = s[t] >= tau; alarm[t] = hit; ex[t] = s[t] - tau if np.isfinite(tau) else (-1.0 if tau > 0 else 1.0)
        a += G * (Q - float(hit and bad[t]))
    return alarm, ex, a


def prf(m, pr):
    tp = (pr & m).sum(); p = tp / max(pr.sum(), 1); r = tp / max(m.sum(), 1)
    return p, r, (0 if p + r == 0 else 2 * p * r / (p + r))


def run(ds, seed, p8dir, log):
    conf_fl.setup(ds, "primary"); pilot_fl.K_CLIENTS = K
    X, y, part, tt, _ = s3_unit.load_meta(ds)
    C = len(pilot_fl.CLASSES); R = conf_fl.ROUNDS
    rng = np.random.default_rng(seed * 1000 + 50 + K_SHOTS + 8888)
    if pilot_fl.RARE[0] in ("ransomware", "SQL_Injection"):
        part = part.copy(); r2 = np.random.default_rng(20_000 + seed)
        for ci in range(1, C - len(pilot_fl.RARE)):
            ix = np.where((part == "train") & (y == ci))[0]
            if len(ix) > conf_fl.TON_COMMON_TRAIN:
                part[r2.choice(ix, len(ix) - conf_fl.TON_COMMON_TRAIN, replace=False)] = "unused"
    mu_, sd_ = X[part == "train"].mean(0), X[part == "train"].std(0) + 1e-6; Z = ((X - mu_) / sd_).astype(np.float32)
    clients, owners = s4_unit.make_clients_multi(y, part, rng, ALPHA, K_SHOTS, 1)
    te = np.where(part == "test")[0]
    ben = te[y[te] == 0]; ben = rng.choice(ben, min(len(ben), pilot_fl.N_BENIGN_TEST), replace=False)
    te = np.concatenate([ben, te[y[te] != 0]])
    rid = [pilot_fl.CLASSES.index(c) for c in pilot_fl.RARE]; nrid = [i for i in range(C) if i not in rid]
    z8 = np.load(os.path.join(p8dir, f"{ds}_s{seed}.npz"))
    assert np.array_equal(z8["y_test"], y[te]) and np.array_equal(z8["t_test"], tt[te]), "test set differs from pilot 8"
    p0 = pilot_fl.init(X.shape[1], C, rng)
    rng = np.random.default_rng(seed * 1000 + 99_000)  # own stream for the experts of this pilot
    CW = [pilot2_fl.class_weights(y[i], C) for i in clients]
    neg = [clients[j][~np.isin(y[clients[j]], rid)] for j in range(K)]; negall = np.concatenate(neg)
    lg = lambda p, idx: pilot_fl.forward(p, Z[idx])[3].astype(np.float32)
    yt = y[te]; order = np.argsort(tt[te], kind="stable"); wins = np.array_split(order, W)
    site = rng.integers(0, K, len(te))  # client whose traffic each test flow belongs to
    replay = [rng.choice(clients[j], min(REPLAY, len(clients[j])), replace=False) for j in range(K)]
    for c in pilot_fl.RARE:  # owners always replay all their rare flows
        o = owners[c][0]; ci = pilot_fl.CLASSES.index(c)
        replay[o] = np.union1d(replay[o], clients[o][y[clients[o]] == ci])
    base = {c: pilot_fl.local_train(p0, Z[clients[owners[c][0]]], y[clients[owners[c][0]]], rng, epochs=R, cw=CW[owners[c][0]])
            for c in pilot_fl.RARE}
    res = {}
    for var in ("static", "loop", "loopneg"):
        hits = np.zeros((len(te), len(rid)), bool); ex = np.zeros((len(te), len(rid)), np.float32); n_ft = 0
        for k, (c, ci) in enumerate(zip(pilot_fl.RARE, rid)):
            pe = base[c]; cal = np.sort(s3_unit.margin(lg(pe, negall), ci)); a = Q; lab = []
            for w in wins:
                s = s3_unit.margin(lg(pe, te[w]), ci)
                h, e, a = aci_window(s, yt[w] != ci, cal, a); hits[w, k] = h; ex[w, k] = e; lab.extend(w[h])
                if var == "static" or not lab:
                    continue
                L = np.array(lab); L = L[yt[L] != ci] if var == "loopneg" else L
                if not len(L):
                    continue
                ups, sz = [], []
                for _ in range(FT_ROUNDS):
                    ups, sz = [], []
                    for j in range(K):
                        mine = L[site[L] == j]
                        mine = np.repeat(mine, UPW)
                        Xj = np.concatenate([Z[replay[j]], Z[te[mine]]]); yj = np.concatenate([y[replay[j]], yt[mine]])
                        cw = pilot2_fl.class_weights(yj, C); cw[ci] = max(cw[ci], CW[owners[c][0]][ci])
                        ups.append(pilot_fl.local_train(pe, Xj, yj, rng, epochs=FT_EPOCHS, cw=cw)); sz.append(len(yj))
                    pe = pilot_fl.avg(ups, sz)
                n_ft += 1
                cal = np.sort(s3_unit.margin(lg(pe, negall), ci))
        res[var] = (hits, ex)
        log(f"  {var} done ({n_ft} fine-tunes)")
    # FedOV+OC + ACI on the same windows (no model update), better FedOV variant by rare F1 at fixed threshold
    def mg(L, c):
        L = L.astype(np.float32); o = L.copy(); o[:, c] = -np.inf
        return L[:, c] - o.max(1)
    best = max(("FedOV", "FedOV-full"), key=lambda m: np.mean([prf(yt == ci, mg(z8[f"{m}|test"], ci) >= np.quantile(mg(z8[f"{m}|cal"], ci), 1 - Q))[2] for ci in rid]))
    Lt = z8[f"{best}|test"].astype(np.float32); hits = np.zeros((len(te), len(rid)), bool); ex = np.zeros_like(hits, np.float32)
    for k, ci in enumerate(rid):
        s, cal, a = mg(Lt, ci), np.sort(mg(z8[f"{best}|cal"], ci)), Q
        for w in wins:
            h, e, a = aci_window(s[w], yt[w] != ci, cal, a); hits[w, k] = h; ex[w, k] = e
    res["FedOV+OC ACI"] = (hits, ex)
    Gt = z8["GB+CR|test"].astype(np.float32)
    negte = ~np.isin(yt, rid); half = np.zeros(len(te), bool); half[order[len(order) // 2:]] = True
    rows = []
    for v, (h, e) in res.items():
        Gv = Lt if v.startswith("FedOV") else Gt
        pred = np.array(nrid)[Gv[:, nrid].argmax(1)]; anyh = h.any(1); ee = np.where(h, e, -np.inf)
        pred[anyh] = np.array(rid)[ee[anyh].argmax(1)]
        Gp = np.array(nrid)[Gv[:, nrid].argmax(1)]
        rr = [prf(yt == ci, pred == ci) for ci in rid]; rr2 = [prf((yt == ci) & half, (pred == ci) & half) for ci in rid]
        rows.append(dict(ds=ds, seed=seed, method=v, fedov=best, rare_f1=np.mean([r[2] for r in rr]), rare_p=np.mean([r[0] for r in rr]),
                         rare_r=np.mean([r[1] for r in rr]), rare_f1_2nd_half=np.mean([r[2] for r in rr2]),
                         fa=h[negte].mean(), fa_2nd_half=h[negte & half].mean(),
                         d_common_f1=np.mean([prf(yt == ci, pred == ci)[2] - prf(yt == ci, Gp == ci)[2] for ci in nrid if ci != 0]),
                         alarms_labelled=int(h.any(1).sum())))
    return pd.DataFrame(rows)


if __name__ == "__main__":
    ds, seed, p8dir, outdir = sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4]
    f = os.path.join(outdir, f"{ds}_s{seed}.csv")
    if os.path.exists(f):
        sys.exit(0)
    os.makedirs(outdir, exist_ok=True)
    t0 = time.time(); log = lambda s: print(f"[{time.time() - t0:6.0f}s] {ds} s{seed} {s}", flush=True)
    d = run(ds, seed, p8dir, log); d.to_csv(f + ".tmp", index=False); os.replace(f + ".tmp", f); log("finished")
