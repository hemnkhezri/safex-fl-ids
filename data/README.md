# Data

The datasets are not redistributed here. Download them from the University of Queensland NIDS datasets page
(https://staff.itee.uq.edu.au/marius/NIDS_datasets/) and place them as follows:

```
data/nf_unsw_v3/NF-UNSW-NB15-v3.parquet
data/nf_toniot_v3/NF-ToN-IoT-v3.parquet
```

Both are distributed as CSV. Convert them with `python3 scripts/csv_to_parquet.py <in.csv> <out.parquet>`.
For NF-ToN-IoT-v3, then build the fixed seed-0 subsample used by all runs:

```
python3 src/prep_toniot.py      # writes data/nf_toniot_v3/pool.parquet
python3 src/audit_toniot.py     # optional: leakage and duplicate audit (results/audit_toniot_v3.md)
```

Expected file sizes: NF-UNSW-NB15-v3 has 2,365,424 flows; NF-ToN-IoT-v3 has 27,520,260 flows.
