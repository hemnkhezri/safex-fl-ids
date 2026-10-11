"""Convert a NetFlow v3 CSV to parquet in chunks (floats stored as float32 to save memory).
Usage: python3 scripts/csv_to_parquet.py IN.csv OUT.parquet
"""
import sys

import pyarrow as pa
import pyarrow.parquet as pq
import pandas as pd

src, dst = sys.argv[1], sys.argv[2]
writer = None
for chunk in pd.read_csv(src, chunksize=1_000_000, low_memory=False):
    for c in chunk.select_dtypes("float64").columns:
        chunk[c] = chunk[c].astype("float32")
    t = pa.Table.from_pandas(chunk, preserve_index=False)
    if writer is None:
        writer = pq.ParquetWriter(dst, t.schema, compression="zstd")
    writer.write_table(t.cast(writer.schema))
writer.close()
print("wrote", dst)
