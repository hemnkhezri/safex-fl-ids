"""Pilot (development, not sealed): are client-exclusive rare attack classes lost in federated learning?
Design notes for the development pilots are summarised in results/dev/.

All methods share one small MLP encoder (numpy, manual backprop, Adam). FL methods average encoder (+ head)
parameters every round; prototype methods add a pull-to-global-prototype loss and classify by the nearest
global prototype. The aggregation weighting of prototypes and of client models is what differs.

Usage: python3 pilot_fl.py --frac 0.05 --seeds 1 --out results/pilot_smoke.csv
"""
from __future__ import annotations

import argparse
import os
import time

import numpy as np
import pandas as pd

DATA = os.path.join(os.path.dirname(__file__), "..", "data", "nf_unsw_v3", "NF-UNSW-NB15-v3.parquet")
DROP = ["FLOW_START_MILLISECONDS", "FLOW_END_MILLISECONDS", "IPV4_SRC_ADDR", "IPV4_DST_ADDR", "L4_SRC_PORT",
        "DNS_QUERY_ID", "MIN_TTL", "MAX_TTL", "MIN_IP_PKT_LEN", "Label", "Attack"]
COMMON = ["Benign", "Exploits", "Fuzzers", "Generic", "Reconnaissance", "DoS"]
RARE = ["Backdoor", "Shellcode", "Analysis", "Worms"]
CLASSES = COMMON + RARE
K_CLIENTS, ROUNDS, BATCH, LR, LAM, HID, EMB = 10, 30, 256, 1e-3, 0.5, 64, 32
N_BENIGN_TRAIN, N_BENIGN_TEST = 150_000, 100_000


# ---------------------------------------------------------------- data
def load():
    df = pd.read_parquet(DATA)
    df = df.sort_values("FLOW_START_MILLISECONDS").reset_index(drop=True)
    n = len(df)
    part = np.empty(n, dtype=object)
    part[: int(0.7 * n)] = "train"; part[int(0.7 * n): int(0.8 * n)] = "val"; part[int(0.8 * n):] = "test"
    X = df.drop(columns=DROP).astype("float64").replace([np.inf, -np.inf], np.nan)
    X = X.fillna(X.max())
    X["DST_PORT_WELLKNOWN"] = (df.L4_DST_PORT < 1024).astype(float)
    X = np.log1p(X.clip(lower=0)).to_numpy(np.float32)
    y = df.Attack.map({c: i for i, c in enumerate(CLASSES)}).to_numpy()
    # remove test rows whose feature vector also occurs in train (exact duplicates)
    key = pd.util.hash_pandas_object(pd.DataFrame(X), index=False).to_numpy()
    in_train = np.isin(key, key[part == "train"])
    keep = ~((part == "test") & in_train)
    return X[keep], y[keep], part[keep], int((~keep).sum())


# ---------------------------------------------------------------- model
def init(d, C, rng):
    s = lambda a, b: rng.normal(0, np.sqrt(2 / a), (a, b)).astype(np.float32)
    return {"W1": s(d, HID), "b1": np.zeros(HID, np.float32), "W2": s(HID, EMB), "b2": np.zeros(EMB, np.float32),
            "Wh": s(EMB, C), "bh": np.zeros(C, np.float32)}


def forward(p, X):
    a1 = X @ p["W1"] + p["b1"]; z1 = np.maximum(a1, 0)
    h = z1 @ p["W2"] + p["b2"]
    return a1, z1, h, h @ p["Wh"] + p["bh"]


def embed(p, X):
    return forward(p, X)[2]


def local_train(p, X, y, rng, epochs=1, protos=None, mu=0.0, anchor=None, cw=None, ladj=None, train=None, lscale=None):
    """One client's local update. protos: (C, EMB) global prototypes with NaN rows for missing classes."""
    p = {k: v.copy() for k, v in p.items()}
    m = {k: np.zeros_like(v) for k, v in p.items()}; v2 = {k: np.zeros_like(v) for k, v in p.items()}; t = 0
    for _ in range(epochs):
        idx = rng.permutation(len(X))
        for s in range(0, len(X), BATCH):
            b = idx[s:s + BATCH]; xb, yb = X[b], y[b]; nb = len(b)
            a1, z1, h, logit = forward(p, xb)
            if lscale is not None:
                logit = logit * lscale
            if ladj is not None:
                logit = logit + ladj
            logit = logit - logit.max(1, keepdims=True); pr = np.exp(logit); pr /= pr.sum(1, keepdims=True)
            g_logit = pr; g_logit[np.arange(nb), yb] -= 1
            if cw is not None:
                g_logit *= cw[yb][:, None]
            if lscale is not None:
                g_logit *= lscale
            g_logit /= nb
            g = {"Wh": h.T @ g_logit, "bh": g_logit.sum(0)}
            g_h = g_logit @ p["Wh"].T
            if protos is not None:
                tgt = protos[yb]; ok = ~np.isnan(tgt[:, 0])
                if ok.any():
                    g_h[ok] += LAM * 2 * (h[ok] - tgt[ok]) / nb
            g["W2"] = z1.T @ g_h; g["b2"] = g_h.sum(0)
            g_a1 = (g_h @ p["W2"].T) * (a1 > 0)
            g["W1"] = xb.T @ g_a1; g["b1"] = g_a1.sum(0)
            if train is not None:
                g = {k: (v if k in train else np.zeros_like(v)) for k, v in g.items()}
            if mu > 0:
                for k in g:
                    g[k] = g[k] + mu * (p[k] - anchor[k])
            t += 1
            for k in p:
                m[k] = 0.9 * m[k] + 0.1 * g[k]; v2[k] = 0.999 * v2[k] + 0.001 * g[k] ** 2
                p[k] -= LR * (m[k] / (1 - 0.9 ** t)) / (np.sqrt(v2[k] / (1 - 0.999 ** t)) + 1e-8)
    return p


def avg(params, w):
    w = np.asarray(w, float); w = w / w.sum()
    return {k: sum(wi * pi[k] for wi, pi in zip(w, params)) for k in params[0]}


# ---------------------------------------------------------------- prototypes and weights
def local_stats(p, X, y, C):
    h = embed(p, X); logit = h @ p["Wh"] + p["bh"]
    logit -= logit.max(1, keepdims=True); pr = np.exp(logit); pr /= pr.sum(1, keepdims=True)
    ent = -(pr * np.log(pr + 1e-12)).sum(1) / np.log(C)
    P = np.full((C, EMB), np.nan, np.float32); n = np.zeros(C); var = np.zeros(C); unc = np.zeros(C)
    for c in np.unique(y):
        hc = h[y == c]; P[c] = hc.mean(0); n[c] = len(hc)
        var[c] = ((hc - P[c]) ** 2).sum(1).mean(); unc[c] = ent[y == c].mean()
    return P, n, var, unc


def aggregate_protos(stats, rule, C, beta=3.0, a=0.2, b=0.2):
    P_all = np.stack([s[0] for s in stats]); n_all = np.stack([s[1] for s in stats])
    unc_all = np.stack([s[3] for s in stats])
    G = np.full((C, EMB), np.nan, np.float32); client_conf = np.zeros(len(stats))
    for c in range(C):
        has = n_all[:, c] > 0
        if not has.any():
            continue
        if rule == "count":
            w = n_all[has, c]
        elif rule == "discrepancy":  # FedGMKD-style: count share minus a * normalised distance to the others' mean
            share = n_all[has, c] / n_all[has, c].sum(); Ph = P_all[has, c]
            if has.sum() == 1:
                w = share
            else:
                d = np.array([np.linalg.norm(Ph[i] - np.delete(Ph, i, 0).mean(0)) for i in range(len(Ph))])
                w = np.maximum(share - a * d / (d.mean() + 1e-8) + b, 0) + 1e-8
        elif rule == "confidence":  # CAFedCL-style: normalised sample size x exp(-beta * class uncertainty), clipped
            nn = np.sqrt(n_all[has, c]); conf = (nn / nn.max()) * np.exp(-beta * unc_all[has, c])
            w = np.clip(conf, 0.05, 1.0)
            client_conf[np.where(has)[0]] += w
        else:
            raise ValueError(rule)
        w = w / w.sum(); G[c] = (w[:, None] * P_all[has, c]).sum(0)
    return G, client_conf


def predict(p, X, G=None):
    h = embed(p, X)
    if G is None:
        return (h @ p["Wh"] + p["bh"]).argmax(1)
    ok = ~np.isnan(G[:, 0]); d = ((h[:, None, :] - G[None, ok, :]) ** 2).sum(2)
    return np.where(ok)[0][d.argmin(1)]


# ---------------------------------------------------------------- experiment
def make_clients(X, y, part, rng, alpha, k, frac):
    tr = np.where(part == "train")[0]
    ben = tr[y[tr] == 0]; ben = rng.choice(ben, int(N_BENIGN_TRAIN * frac), replace=False)
    owner = {}
    clients = [[] for _ in range(K_CLIENTS)]
    for ci, c in enumerate(CLASSES):
        if c in RARE:
            continue
        idx = ben if c == "Benign" else tr[y[tr] == ci]
        if c != "Benign":
            idx = rng.choice(idx, max(1, int(len(idx) * frac)), replace=False)
        share = rng.dirichlet([alpha] * K_CLIENTS); cut = (np.cumsum(share) * len(idx)).astype(int)[:-1]
        for j, chunk in enumerate(np.split(rng.permutation(idx), cut)):
            clients[j].extend(chunk)
    rare_clients = rng.choice(K_CLIENTS, len(RARE), replace=False)
    for c, j in zip(RARE, rare_clients):
        ci = CLASSES.index(c); idx = tr[y[tr] == ci]
        clients[j].extend(rng.choice(idx, min(k, len(idx)), replace=False)); owner[c] = int(j)
    return [np.array(c) for c in clients], owner


def run(X, y, part, seed, alpha, k, frac, log):
    rng = np.random.default_rng(seed * 1000 + int(alpha * 100) + k)
    C = len(CLASSES); d = X.shape[1]
    mu_, sd_ = X[part == "train"].mean(0), X[part == "train"].std(0) + 1e-6
    Z = (X - mu_) / sd_
    clients, owner = make_clients(Z, y, part, rng, alpha, k, frac)
    te = np.where(part == "test")[0]
    ben_te = te[y[te] == 0]; ben_te = rng.choice(ben_te, min(len(ben_te), int(N_BENIGN_TEST * max(frac, 0.2))), replace=False)
    te = np.concatenate([ben_te, te[y[te] != 0]])
    Xte, yte = Z[te], y[te]
    p0 = init(d, C, rng)
    out = {}

    def fl(rule=None, mu=0.0):
        p = p0; G = None
        for r in range(ROUNDS):
            ups, sizes = [], []
            for j, idx in enumerate(clients):
                ups.append(local_train(p, Z[idx], y[idx], rng, protos=G if rule else None, mu=mu, anchor=p))
                sizes.append(len(idx))
            w = np.array(sizes, float)
            if rule:
                stats = [local_stats(u, Z[idx], y[idx], C) for u, idx in zip(ups, clients)]
                G, cc = aggregate_protos(stats, rule, C)
                if rule == "confidence":
                    w = sizes * np.maximum(cc, 1e-3)
            p = avg(ups, w)
        return p, G

    for name, kw in [("FedAvg", {}), ("FedProx", {"mu": 0.01}), ("Proto-count", {"rule": "count"}),
                     ("Proto-discrepancy", {"rule": "discrepancy"}), ("Proto-confidence", {"rule": "confidence"})]:
        t0 = time.time(); p, G = fl(**kw)
        out[name] = predict(p, Xte, G); log(f"  {name} {time.time() - t0:.0f}s")
    # centralised reference on the pooled client data, same epochs
    allidx = np.concatenate(clients); t0 = time.time()
    pc = local_train(p0, Z[allidx], y[allidx], rng, epochs=ROUNDS)
    out["Central-head"] = predict(pc, Xte)
    st = local_stats(pc, Z[allidx], y[allidx], C); out["Central-proto"] = predict(pc, Xte, st[0])
    log(f"  Central {time.time() - t0:.0f}s")
    # local-only model of each rare class's owner, evaluated on that class
    loc = {}
    for c, j in owner.items():
        pl = local_train(p0, Z[clients[j]], y[clients[j]], rng, epochs=ROUNDS); loc[c] = predict(pl, Xte)
    rows = []
    for meth, pred in list(out.items()) + [("Local-owner", None)]:
        for ci, c in enumerate(CLASSES):
            pr = (loc[c] if c in loc else None) if meth == "Local-owner" else pred
            if pr is None:
                continue
            m = yte == ci; tp = ((pr == ci) & m).sum(); fp = ((pr == ci) & ~m).sum()
            rows.append(dict(seed=seed, alpha=alpha, k=k, frac=frac, method=meth, cls=c, rare=c in RARE,
                             n_test=int(m.sum()), recall=tp / max(m.sum(), 1), precision=tp / max(tp + fp, 1)))
        if meth != "Local-owner":
            from sklearn.metrics import f1_score, matthews_corrcoef
            rows.append(dict(seed=seed, alpha=alpha, k=k, frac=frac, method=meth, cls="_overall", rare=False,
                             n_test=len(yte), recall=f1_score(yte, pred, average="macro"), precision=matthews_corrcoef(yte, pred)))
    return rows


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--frac", type=float, default=1.0); ap.add_argument("--seeds", type=int, default=5)
    ap.add_argument("--alphas", default="0.1,0.5"); ap.add_argument("--ks", default="5,20,100")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    t0 = time.time(); log = lambda s: print(f"[{time.time() - t0:6.0f}s] {s}", flush=True)
    X, y, part, n_dup = load(); log(f"loaded {X.shape}, removed {n_dup} test rows duplicated in train")
    rows = []
    for seed in range(a.seeds):
        for alpha in map(float, a.alphas.split(",")):
            for k in map(int, a.ks.split(",")):
                log(f"seed={seed} alpha={alpha} k={k}")
                rows += run(X, y, part, seed, alpha, k, a.frac, log)
                os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
                pd.DataFrame(rows).to_csv(a.out, index=False)
    log("done")
