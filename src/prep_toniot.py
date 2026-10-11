"""Build the fixed NF-ToN-IoT-v3 pool (study_plan_hybrid_v1_SEALED.md section 3): per-class chronological
70/10/20 split, then a seed-0 subsample inside each split for memory. Output: data/nf_toniot_v3/pool.parquet
with a 'part' column."""
import os
import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

F = os.path.join(os.path.dirname(__file__), "..", "data", "nf_toniot_v3", "NF-ToN-IoT-v3.parquet")
OUT = os.path.join(os.path.dirname(__file__), "..", "data", "nf_toniot_v3", "pool.parquet")
RARE = ["ransomware", "mitm", "Backdoor", "dos"]
CAP = {"train": 200_000, "test": 50_000}; BEN = {"train": 1_000_000, "test": 500_000}; N_VAL = 200_000
meta = pq.read_table(F, columns=["FLOW_START_MILLISECONDS", "Attack"]).to_pandas()
meta["Attack"] = meta.Attack.astype(str); n = len(meta); ts = meta.FLOW_START_MILLISECONDS.to_numpy()
part = np.empty(n, dtype=object)
for c, ix in meta.groupby("Attack").indices.items():
    ix = ix[np.argsort(ts[ix], kind="stable")]; m = len(ix)
    part[ix[: int(0.7 * m)]] = "train"; part[ix[int(0.7 * m): int(0.8 * m)]] = "val"; part[ix[int(0.8 * m):]] = "test"
rng = np.random.default_rng(0); keep = []
for (c, p), ix in pd.DataFrame({"c": meta.Attack, "p": part}).groupby(["c", "p"]).indices.items():
    if p == "val":
        continue
    cap = len(ix) if c in RARE else (BEN[p] if c == "Benign" else CAP[p])
    keep.append(rng.choice(ix, min(cap, len(ix)), replace=False))
va = np.where(part == "val")[0]; keep.append(rng.choice(va, N_VAL, replace=False))
keep = np.sort(np.concatenate(keep))
del meta, ts
pf = pq.ParquetFile(F); w = None; off = 0; tabs = []
for b in pf.iter_batches(batch_size=1_000_000):  # stream to keep memory low
    sel = keep[(keep >= off) & (keep < off + b.num_rows)]
    if len(sel):
        tb = pa.Table.from_batches([b]).take(pa.array(sel - off))
        tb = tb.append_column("part", pa.array(part[sel].astype(str)))
        tb = tb.set_column(tb.schema.get_field_index("Attack"), "Attack", tb.column("Attack").cast(pa.string()))
        if w is None:
            w = pq.ParquetWriter(OUT, tb.schema, compression="zstd")
        w.write_table(tb)
    off += b.num_rows
w.close(); t = pq.read_table(OUT, columns=["Attack", "part"])
print(pd.crosstab(t.column("Attack").to_pandas().astype(str), t.column("part").to_pandas()))
