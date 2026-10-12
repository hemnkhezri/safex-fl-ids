"""Leakage and structure audit of NF-CSE-CIC-IDS2018-v3 before it is used as the third dataset (plan v3 Part F).
Prints: class counts; time span; class presence across the time-ordered 70/10/20 split; source/destination IP
concentration per class; single-feature balanced accuracy (depth-3 tree, binary attack-vs-benign and multiclass,
time-split train -> test on a stratified sample); exact-duplicate rate between train and test.
Usage: python3 src/audit_cic.py > results/audit_cic2018_v3.md
"""
import os

import numpy as np
import pandas as pd
import pyarrow.parquet as pq
from sklearn.metrics import balanced_accuracy_score
from sklearn.tree import DecisionTreeClassifier

F = os.path.join(os.path.dirname(__file__), "..", "data", "nf_cic2018_v3", "NF-CSE-CIC-IDS2018-v3.parquet")
pf = pq.ParquetFile(F); cols = pf.schema_arrow.names
meta = pq.read_table(F, columns=["FLOW_START_MILLISECONDS", "Attack", "IPV4_SRC_ADDR", "IPV4_DST_ADDR"], read_dictionary=["Attack", "IPV4_SRC_ADDR", "IPV4_DST_ADDR"]).to_pandas()
meta["Attack"] = meta.Attack.astype(str)
n = len(meta); order = np.argsort(meta.FLOW_START_MILLISECONDS.to_numpy(), kind="stable")
part = np.empty(n, dtype=object)
part[order[: int(0.7 * n)]] = "train"; part[order[int(0.7 * n): int(0.8 * n)]] = "val"; part[order[int(0.8 * n):]] = "test"
meta["part_global"] = part
# attacks may be scheduled by day, so a global time split separates classes; use a per-class
# chronological split instead (first 70% of each class's flows -> train, next 10% -> val, last 20% -> test)
part = np.empty(n, dtype=object)
for c, ix in meta.groupby("Attack").indices.items():
    ix = ix[np.argsort(meta.FLOW_START_MILLISECONDS.to_numpy()[ix], kind="stable")]; m = len(ix)
    part[ix[: int(0.7 * m)]] = "train"; part[ix[int(0.7 * m): int(0.8 * m)]] = "val"; part[ix[int(0.8 * m):]] = "test"
meta["part"] = part
t = pd.to_datetime(meta.FLOW_START_MILLISECONDS, unit="ms")
print(f"# NF-CSE-CIC-IDS2018-v3 audit\n\nrows {n:,}; time {t.min()} to {t.max()}; days {t.dt.date.nunique()}\n")
print("## Class counts by global time-ordered split (unusable: classes fall in disjoint periods)\n")
print(pd.crosstab(meta.Attack, meta.part_global)[["train", "val", "test"]].assign(total=lambda d: d.sum(1))
      .sort_values("total").to_markdown(), "\n")
print("## Per class: first/last day, top source IP share, number of source IPs\n")
g = []
for c, d in meta.groupby("Attack"):
    vc = d.IPV4_SRC_ADDR.value_counts()
    g.append(dict(cls=c, first=t[d.index].min().date(), last=t[d.index].max().date(), n_src=len(vc),
                  top_src=vc.index[0], top_src_share=round(vc.iloc[0] / len(d), 3),
                  top_dst_share=round(d.IPV4_DST_ADDR.value_counts().iloc[0] / len(d), 3)))
print(pd.DataFrame(g).to_markdown(index=False), "\n")
# stratified sample: up to 30k per class per split
rng = np.random.default_rng(0)
idx = np.concatenate([rng.choice(ix, min(len(ix), 30000), replace=False)
                      for _, ix in meta.groupby(["Attack", "part"]).indices.items()])
idx.sort()
feat = [c for c in cols if c not in ("Attack", "Label", "IPV4_SRC_ADDR", "IPV4_DST_ADDR")]
del meta["IPV4_SRC_ADDR"], meta["IPV4_DST_ADDR"]
X = pd.DataFrame({f: pq.read_table(F, columns=[f]).column(0).take(idx).to_numpy(zero_copy_only=False).astype("float64")
                  for f in feat}).replace([np.inf, -np.inf], np.nan).fillna(0)
y = meta.Attack.to_numpy()[idx]; p = part[idx]; yb = (y != "Benign").astype(int)
tr, te = p == "train", p == "test"
rows = []
for f in feat:
    r = {"feature": f}
    for name, yy in (("binary", yb), ("multi", y)):
        if len(np.unique(yy[tr])) < 2 or len(np.unique(yy[te])) < 2:
            r[name] = np.nan; continue
        m = DecisionTreeClassifier(max_depth=3, class_weight="balanced", random_state=0).fit(X.loc[tr, [f]], yy[tr])
        r[name] = round(balanced_accuracy_score(yy[te], m.predict(X.loc[te, [f]])), 3)
    rows.append(r)
s = pd.DataFrame(rows).sort_values("binary", ascending=False)
print("## Per-class split: day ranges of train and test per class\n")
print(meta.assign(day=t.dt.strftime("%m-%d")).groupby(["Attack", "part"]).day.agg(["min", "max"]).unstack().to_markdown(), "\n")
print("## Single-feature balanced accuracy (depth-3 tree, train period -> test period, stratified sample)\n")
print(s.head(20).to_markdown(index=False), "\n")
print(f"classes in test sample: {sorted(set(y[te]))}\n")
key = pd.util.hash_pandas_object(X, index=False).to_numpy()
dup = np.isin(key[te], key[tr]).mean()
print(f"## Exact duplicates\n\nshare of sampled test rows whose full feature vector (incl. timestamps) occurs in sampled train: {dup:.3f}")
Xn = X.drop(columns=["FLOW_START_MILLISECONDS", "FLOW_END_MILLISECONDS"])
key = pd.util.hash_pandas_object(Xn, index=False).to_numpy()
print(f"\nsame without timestamps: {np.isin(key[te], key[tr]).mean():.3f}")
# Plan v3 Part F rules
tt = meta.FLOW_START_MILLISECONDS.to_numpy(); days = pd.to_datetime(tt, unit="ms").normalize()
n_days = days.nunique(); span = meta.assign(d=days).groupby("Attack").d.nunique()
cnt = meta.Attack.value_counts(); att = cnt.drop("Benign")
rare = list(att[att >= 100].sort_values().index[:4]); common = list(att.drop(rare).sort_values(ascending=False).index[:5])
print(f"\n## Plan v3 Part F rules\n\ncapture days {n_days}; days spanned per class: {span.to_dict()}")
print(f"split: {'per-class chronological' if (span.drop('Benign') < n_days / 2).any() else 'global chronological'}")
print(f"rare (4 smallest attack classes with >= 100 flows): {rare}\ncommon (up to 5 largest remaining): {common}")
print("dropped by the 0.99 rule (binary single-feature balanced accuracy > 0.99):", list(s[s.binary > 0.99].feature))
