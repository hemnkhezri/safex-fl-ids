"""Confirmatory runs for study_plan_hybrid_v1_SEALED.md. One call = one (dataset, arm, seed, alpha, k) unit;
saves logits of every model on the test set, the calibration set and each owner's non-rare flows, plus labels,
so OC and all metrics are computed afterwards by analyze_conf.py.
Usage: python3 conf_fl.py DATASET ARM SEED ALPHA K OUTDIR      (DATASET: unsw|ton; ARM: primary|e1|big)
"""
from __future__ import annotations

import os
import sys
import time

import numpy as np
import pandas as pd

import pilot_fl
import pilot2_fl

DS = {
    "unsw": dict(common=["Benign", "Exploits", "Fuzzers", "Generic", "Reconnaissance", "DoS"],
                 rare=["Backdoor", "Shellcode", "Analysis", "Worms"]),
    "ton": dict(common=["Benign", "ddos", "xss", "password", "scanning", "injection"],
                rare=["ransomware", "mitm", "Backdoor", "dos"]),
    # plan v3 Part F: classes chosen by rule from results/audit_cic2018_v3.md
    "cic": dict(common=["Benign", "DDOS_attack-HOIC", "FTP-BruteForce", "DDoS_attacks-LOIC-HTTP", "Bot", "SSH-Bruteforce"],
                rare=["SQL_Injection", "Brute_Force_-XSS", "Brute_Force_-Web", "DDOS_attack-LOIC-UDP"]),
}
TON_POOL = os.path.join(os.path.dirname(__file__), "..", "data", "nf_toniot_v3", "pool.parquet")
CIC_POOL = os.path.join(os.path.dirname(__file__), "..", "data", "nf_cic2018_v3", "pool.parquet")
ROUNDS, N_CAL, TON_COMMON_TRAIN = int(os.environ.get("SMOKE_ROUNDS", 60)), 20000, 20000


def setup(ds, arm):
    pilot_fl.CLASSES = DS[ds]["common"] + DS[ds]["rare"]; pilot_fl.RARE = DS[ds]["rare"]
    if arm == "big":
        pilot_fl.HID, pilot_fl.EMB = 128, 64; pilot2_fl.EMB = 64


def load(ds):
    """Cached preprocessed arrays (local disk) so parallel workers do not each pay the pandas memory peak."""
    cache = os.path.join(os.environ.get("SAFEX_CACHE", os.path.expanduser("~/.cache/safex")), f"{ds}.npz")
    if os.path.exists(cache):
        z = np.load(cache, allow_pickle=True)
        return z["X"], z["y"], z["part"]
    X, y, part = _load(ds)
    os.makedirs(os.path.dirname(cache), exist_ok=True)
    np.savez(cache + ".tmp.npz", X=X, y=y, part=part); os.replace(cache + ".tmp.npz", cache)
    return X, y, part


def _load(ds):
    if ds == "unsw":
        X, y, part, _ = pilot_fl.load()
        return X, y, part
    df = pd.read_parquet(TON_POOL)
    part = df.pop("part").to_numpy().astype(object)
    X = df.drop(columns=pilot_fl.DROP).astype("float64").replace([np.inf, -np.inf], np.nan)
    X = X.fillna(X.max())
    X["DST_PORT_WELLKNOWN"] = (df.L4_DST_PORT < 1024).astype(float)
    X = np.log1p(X.clip(lower=0)).to_numpy(np.float32)
    y = df.Attack.astype(str).map({c: i for i, c in enumerate(pilot_fl.CLASSES)}).to_numpy()
    key = pd.util.hash_pandas_object(pd.DataFrame(X), index=False).to_numpy()
    keep = ~((part == "test") & np.isin(key, key[part == "train"]))
    return X[keep], y[keep], part[keep]


def run(X, y, part, seed, alpha, k, arm, log):
    C = len(pilot_fl.CLASSES); E = 1 if arm == "e1" else 5
    rng = np.random.default_rng(seed * 1000 + int(alpha * 100) + k)
    if len(pilot_fl.CLASSES) and pilot_fl.RARE[0] == "ransomware":  # ToN: per-run cap of common attack train flows
        part = part.copy(); r2 = np.random.default_rng(20_000 + seed)
        for ci in range(1, len(pilot_fl.CLASSES) - len(pilot_fl.RARE)):
            ix = np.where((part == "train") & (y == ci))[0]
            if len(ix) > TON_COMMON_TRAIN:
                part[r2.choice(ix, len(ix) - TON_COMMON_TRAIN, replace=False)] = "unused"
    mu_, sd_ = X[part == "train"].mean(0), X[part == "train"].std(0) + 1e-6
    Z = (X - mu_) / sd_
    clients, owner = pilot_fl.make_clients(Z, y, part, rng, alpha, k, 1.0)
    te = np.where(part == "test")[0]
    ben = te[y[te] == 0]; ben = rng.choice(ben, min(len(ben), pilot_fl.N_BENIGN_TEST), replace=False)
    te = np.concatenate([ben, te[y[te] != 0]])
    rid = [pilot_fl.CLASSES.index(c) for c in pilot_fl.RARE]
    va = np.where((part == "val") & ~np.isin(y, rid))[0]
    cal = np.random.default_rng(10_000 + seed).choice(va, min(N_CAL, len(va)), replace=False)
    p0 = pilot_fl.init(X.shape[1], C, rng)
    n = np.stack([np.bincount(y[i], minlength=C) for i in clients]).astype(float); sizes = n.sum(1)
    Nc = n.sum(0); wg = np.where(Nc > 0, 1 / np.sqrt(np.maximum(Nc, 1)), 0)
    wg = (wg / (wg @ Nc / Nc.sum())).astype(np.float32)
    CW = [pilot2_fl.class_weights(y[i], C) for i in clients]; LA = [pilot2_fl.prior_adj(y[i], C) for i in clients]
    LS = [np.where(n[j] > 0, 1.0, 0.5).astype(np.float32) for j in range(len(clients))]
    lt = lambda p, j, **kw: pilot_fl.local_train(p, Z[clients[j]], y[clients[j]], rng, epochs=E, **kw)

    def fl(kind):
        p = p0
        for _ in range(ROUNDS):
            if kind == "FedAvg":
                ups = [lt(p, j) for j in range(len(clients))]
            elif kind == "FedAvg-bal":
                ups = [lt(p, j, cw=CW[j]) for j in range(len(clients))]
            elif kind == "FedProx-bal":
                ups = [lt(p, j, cw=CW[j], mu=0.01, anchor=p) for j in range(len(clients))]
            elif kind == "FedLC":
                ups = [lt(p, j, ladj=LA[j]) for j in range(len(clients))]
            elif kind == "FedRS":
                ups = [lt(p, j, lscale=LS[j]) for j in range(len(clients))]
            elif kind == "GB+CR":
                ups = [lt(p, j, cw=wg) for j in range(len(clients))]
            p = pilot_fl.avg(ups, sizes)
            if kind == "GB+CR":
                for c in range(C):
                    h = np.where(n[:, c] > 0)[0]
                    if len(h):
                        w = n[h, c] / n[h, c].sum()
                        p["Wh"][:, c] = sum(wi * ups[j]["Wh"][:, c] for wi, j in zip(w, h))
                        p["bh"][c] = sum(wi * ups[j]["bh"][c] for wi, j in zip(w, h))
        return p

    kinds = {"primary": ["FedAvg", "FedAvg-bal", "FedProx-bal", "FedLC", "FedRS", "GB+CR"],
             "e1": ["FedAvg-bal", "GB+CR"], "big": ["FedAvg-bal", "GB+CR"]}[arm]
    models = {}
    for kd in kinds:
        t0 = time.time(); models[kd] = fl(kd)
        if kd == "FedAvg-bal" and arm != "e1":
            models["CCVR"] = pilot2_fl.ccvr(models[kd], Z, y, clients, C, rng)
        log(f"  {kd} {time.time() - t0:.0f}s")
    allidx = np.concatenate(clients)
    models["Central-bal"] = pilot_fl.local_train(p0, Z[allidx], y[allidx], rng, epochs=ROUNDS,
                                                 cw=pilot2_fl.class_weights(y[allidx], C))
    lg = lambda p, idx: pilot_fl.forward(p, Z[idx])[3].astype(np.float32)
    out = {"y_test": y[te], "y_cal": y[cal], "owner": np.array([owner[c] for c in pilot_fl.RARE]),
           "classes": np.array(pilot_fl.CLASSES), "rare": np.array(pilot_fl.RARE)}
    own_idx = {c: clients[owner[c]][~np.isin(y[clients[owner[c]]], rid)] for c in pilot_fl.RARE}
    for m, p in models.items():
        out[f"{m}|test"] = lg(p, te); out[f"{m}|cal"] = lg(p, cal)
        for c in pilot_fl.RARE:
            out[f"{m}|own_{c}"] = lg(p, own_idx[c])
    if arm == "primary":  # owner-view methods, scored on the owner's own class
        t0 = time.time(); body = dict(p0); heads = [{h: p0[h].copy() for h in pilot2_fl.HEAD} for _ in clients]
        for _ in range(ROUNDS):
            ups = []
            for j in range(len(clients)):
                pj = lt({**body, **heads[j]}, j, cw=CW[j], train=pilot2_fl.HEAD)
                pj = lt(pj, j, cw=CW[j], train=pilot2_fl.BODY)
                heads[j] = {h: pj[h] for h in pilot2_fl.HEAD}; ups.append(pj)
            body = pilot_fl.avg(ups, sizes)
        for c, j in owner.items():
            out[f"FedRep|owner_{c}|test"] = lg({**body, **heads[j]}, te)
            idx = clients[j]
            pl = pilot_fl.local_train(p0, Z[idx], y[idx], rng, epochs=ROUNDS, cw=CW[j])
            out[f"Local-owner-bal|owner_{c}|test"] = lg(pl, te)
        log(f"  owner-view {time.time() - t0:.0f}s")
    return out


if __name__ == "__main__":
    ds, arm, seed, alpha, k, outdir = sys.argv[1], sys.argv[2], int(sys.argv[3]), float(sys.argv[4]), int(sys.argv[5]), sys.argv[6]
    f = os.path.join(outdir, f"{ds}_{arm}_s{seed}_a{alpha}_k{k}.npz")
    if os.path.exists(f):
        sys.exit(0)
    os.makedirs(outdir, exist_ok=True); setup(ds, arm)
    t0 = time.time(); log = lambda s: print(f"[{time.time() - t0:6.0f}s] {ds} {arm} s{seed} a{alpha} k{k} {s}", flush=True)
    X, y, part = load(ds); log(f"loaded {X.shape}")
    res = run(X, y, part, seed, alpha, k, arm, log)
    np.savez_compressed(f + ".tmp.npz", **res); os.replace(f + ".tmp.npz", f); log("finished")
