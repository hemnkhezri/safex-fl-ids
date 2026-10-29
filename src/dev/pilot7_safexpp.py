"""Pilot 7 (development seeds 0-4 only; exploratory, no claims): two candidate extensions of SAFE-X.
NR      federated negative refinement of each shared expert: R_NR rounds where the owner trains on its own data and
        every other client trains on a refinement half of its non-rare flows; the expert is averaged (owner weight W_OWN).
CASCADE an expert alarm counts only when the GB+CR global model does not call the flow benign (p_benign < 0.5);
        the threshold is set so that the joint rule fires on a fraction q of the calibration negatives.
All variants (except the "full" reference) are calibrated on the held-out calibration half of each client's
non-rare flows, so NR is never calibrated on its own refinement data.
Setting = Study 3 main arm via Study 4 code: K = 10 clients, one owner per rare class, k = 20, alpha = 0.5.
Usage: python3 pilot7_safexpp.py DATASET SEED OUTDIR
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

Q, R_NR, W_OWN, NEG_CAP, K, K_SHOTS = 1e-3, 10, 0.5, 4000, 10, 20


def prf(m, pr):
    tp = (pr & m).sum(); p = tp / max(pr.sum(), 1); r = tp / max(m.sum(), 1)
    return p, r, (0 if p + r == 0 else 2 * p * r / (p + r))


def fuse(G, excess, rid, nrid):
    pred = np.array(nrid)[G[:, nrid].argmax(1)]
    ex = np.stack(excess, 1); hit = ex.max(1) >= 0
    pred[hit] = np.array(rid)[ex[hit].argmax(1)]
    return pred


def joint_tau(s, gate, q):
    """Smallest threshold t with mean(gate & s >= t) <= q on the calibration negatives."""
    sg = np.sort(s[gate])[::-1]; n_ok = int(np.floor(q * len(s)))
    return -np.inf if n_ok >= len(sg) else sg[n_ok] + 1e-6


def run(ds, seed, log):
    conf_fl.setup(ds, "primary"); pilot_fl.K_CLIENTS = K
    X, y, part, tt, _ = s3_unit.load_meta(ds); log("loaded")
    C = len(pilot_fl.CLASSES); E = 5; R = conf_fl.ROUNDS
    rng = np.random.default_rng(seed * 1000 + 50 + K_SHOTS + 7777)
    if pilot_fl.RARE[0] in ("ransomware", "SQL_Injection"):
        part = part.copy(); r2 = np.random.default_rng(20_000 + seed)
        for ci in range(1, C - len(pilot_fl.RARE)):
            ix = np.where((part == "train") & (y == ci))[0]
            if len(ix) > conf_fl.TON_COMMON_TRAIN:
                part[r2.choice(ix, len(ix) - conf_fl.TON_COMMON_TRAIN, replace=False)] = "unused"
    mu_, sd_ = X[part == "train"].mean(0), X[part == "train"].std(0) + 1e-6; Z = (X - mu_) / sd_
    clients, owners = s4_unit.make_clients_multi(y, part, rng, 0.5, K_SHOTS, 1)
    te = np.where(part == "test")[0]
    ben = te[y[te] == 0]; ben = rng.choice(ben, min(len(ben), pilot_fl.N_BENIGN_TEST), replace=False)
    te = np.concatenate([ben, te[y[te] != 0]]); yt = y[te]
    rid = [pilot_fl.CLASSES.index(c) for c in pilot_fl.RARE]; nrid = [i for i in range(C) if i not in rid]
    va = np.where((part == "val") & ~np.isin(y, rid))[0]
    cal = np.random.default_rng(10_000 + seed).choice(va, min(conf_fl.N_CAL, len(va)), replace=False)
    p0 = pilot_fl.init(X.shape[1], C, rng)
    n = np.stack([np.bincount(y[i], minlength=C) for i in clients]).astype(float); sizes = n.sum(1)
    Nc = n.sum(0); wg = np.where(Nc > 0, 1 / np.sqrt(np.maximum(Nc, 1)), 0); wg = (wg / (wg @ Nc / Nc.sum())).astype(np.float32)
    CW = [pilot2_fl.class_weights(y[i], C) for i in clients]
    lg = lambda p, idx: pilot_fl.forward(p, Z[idx])[3].astype(np.float32)
    timing = {}
    # GB+CR global model (as Study 4)
    t0 = time.time(); p = p0
    for _ in range(R):
        ups = [pilot_fl.local_train(p, Z[clients[j]], y[clients[j]], rng, epochs=E, cw=wg) for j in range(K)]
        p = pilot_fl.avg(ups, sizes)
        for c in range(C):
            h = np.where(n[:, c] > 0)[0]
            if len(h):
                w = n[h, c] / n[h, c].sum()
                p["Wh"][:, c] = sum(wi * ups[j]["Wh"][:, c] for wi, j in zip(w, h)); p["bh"][c] = sum(wi * ups[j]["bh"][c] for wi, j in zip(w, h))
    gb = p; timing["GB+CR"] = time.time() - t0; log(f"  GB+CR {timing['GB+CR']:.0f}s")
    # negatives: per client split into refinement half and calibration half
    neg = [clients[j][~np.isin(y[clients[j]], rid)] for j in range(K)]; negall = np.concatenate(neg)
    sr = np.random.default_rng(30_000 + seed); nref, ncal = [], []
    for a in neg:
        a = sr.permutation(a); nref.append(a[: len(a) // 2]); ncal.append(a[len(a) // 2:])
    ncal_all = np.concatenate(ncal)
    soft = lambda L: np.exp(L - L.max(1, keepdims=True)) / np.exp(L - L.max(1, keepdims=True)).sum(1, keepdims=True)
    G = lg(gb, te); gate_te = soft(G)[:, 0] < 0.5; gate_cal = soft(lg(gb, ncal_all))[:, 0] < 0.5
    negte = ~np.isin(yt, rid)
    S = {v: [] for v in ("plain", "nr")}; SC = {v: [] for v in ("plain", "nr")}; SA = []
    t0 = time.time()
    for c, ci in zip(pilot_fl.RARE, rid):
        o = owners[c][0]; idx = clients[o]
        pe = pilot_fl.local_train(p0, Z[idx], y[idx], rng, epochs=R, cw=CW[o])
        S["plain"].append(s3_unit.margin(lg(pe, te), ci)); SC["plain"].append(s3_unit.margin(lg(pe, ncal_all), ci))
        SA.append(s3_unit.margin(lg(pe, negall), ci))
        pr_ = pe
        for _ in range(R_NR):
            ups, ws = [pilot_fl.local_train(pr_, Z[idx], y[idx], rng, epochs=1, cw=CW[o])], [W_OWN]
            subs = [rng.choice(nref[j], min(NEG_CAP, len(nref[j])), replace=False) for j in range(K) if j != o]
            tot = sum(len(s_) for s_ in subs)
            for s_ in subs:
                ups.append(pilot_fl.local_train(pr_, Z[s_], y[s_], rng, epochs=1, cw=pilot2_fl.class_weights(y[s_], C)))
                ws.append((1 - W_OWN) * len(s_) / tot)
            pr_ = pilot_fl.avg(ups, ws)
        S["nr"].append(s3_unit.margin(lg(pr_, te), ci)); SC["nr"].append(s3_unit.margin(lg(pr_, ncal_all), ci))
    timing["experts+NR"] = time.time() - t0; log(f"  experts+NR {timing['experts+NR']:.0f}s")
    # FedOV baselines
    fed = {}
    for name, fn in (("FedOV", None), ("FedOV-full", s3_unit.fedov_full_local)):
        t0 = time.time(); locs = []
        for i in clients:
            Xi, yi = Z[i], y[i]
            if fn is None:
                import pilot6_baselines
                sub = rng.choice(len(i), max(1, len(i) // 2), replace=False)
                Xa = np.concatenate([Xi, pilot6_baselines.destroy(Xi[sub], rng)]); ya = np.concatenate([yi, np.full(len(sub), C)])
                locs.append(pilot_fl.local_train(pilot_fl.init(X.shape[1], C + 1, rng), Xa, ya, rng, epochs=R, cw=pilot2_fl.class_weights(ya, C + 1)))
            else:
                locs.append(fn(Xi, yi, C, rng, R))
        fed[name] = s3_unit.softmax_sum(locs, Z, [te, cal]); timing[name] = time.time() - t0; log(f"  {name} {timing[name]:.0f}s")
    # predictions
    preds, fa = {}, []
    preds["GB+CR argmax"] = np.array(nrid)[G[:, nrid].argmax(1)]
    for name, (Lt, Lc) in fed.items():
        Lt, Lc = Lt.astype(np.float32), Lc.astype(np.float32)
        preds[f"{name}+OC"] = fuse(Lt, [s3_unit.margin(Lt, c) - np.quantile(s3_unit.margin(Lc, c), 1 - Q) for c in rid], rid, nrid)
    variants = {"SAFE-X (full cal.)": ("plain", False, True), "SAFE-X": ("plain", False, False), "SAFE-X+NR": ("nr", False, False),
                "SAFE-X+cascade": ("plain", True, False), "SAFE-X+NR+cascade": ("nr", True, False)}
    for vname, (kind, casc, full) in variants.items():
        ex = []
        for i, c in enumerate(pilot_fl.RARE):
            s, sc = S[kind][i], SC[kind][i]
            if full:
                e = s - np.quantile(SA[i], 1 - Q)
            elif casc:
                e = np.where(gate_te, s - joint_tau(sc, gate_cal, Q), -np.inf)
            else:
                e = s - np.quantile(sc, 1 - Q)
            ex.append(e)
            fa.append(dict(method=vname, cls=c, fa=(e[negte] >= 0).mean(), fa_benign=(e[yt == 0] >= 0).mean(),
                           recall_expert=(e[yt == rid[i]] >= 0).mean()))
        preds[vname] = fuse(G, ex, rid, nrid)
    rows = []
    for mname, pr in preds.items():
        for ci, c in enumerate(pilot_fl.CLASSES):
            p_, r_, f_ = prf(yt == ci, pr == ci)
            rows.append(dict(method=mname, cls=c, group="rare" if ci in rid else ("benign" if ci == 0 else "common"), precision=p_, recall=r_, f1=f_))
    rows.append(dict(method="_gate", cls="rare_pass", group="info", precision=np.nan,
                     recall=np.mean([gate_te[yt == ci].mean() for ci in rid]), f1=gate_cal.mean()))
    return pd.DataFrame(rows), pd.DataFrame(fa), timing


if __name__ == "__main__":
    ds, seed, outdir = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    f = os.path.join(outdir, f"{ds}_s{seed}")
    if os.path.exists(f + "_scores.csv"):
        sys.exit(0)
    os.makedirs(outdir, exist_ok=True)
    t0 = time.time(); log = lambda s: print(f"[{time.time() - t0:6.0f}s] {ds} s{seed} {s}", flush=True)
    sc, fa, tm = run(ds, seed, log)
    for d_ in (sc, fa):
        d_.insert(0, "seed", seed); d_.insert(0, "ds", ds)
    fa.to_csv(f + "_far.csv", index=False); sc.to_csv(f + "_scores.csv.tmp", index=False); os.replace(f + "_scores.csv.tmp", f + "_scores.csv")
    log(f"finished {tm}")
