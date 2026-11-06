# Scale design: 76k-row sample and 50 million rows/day

## Current implementation (76k-row CSV)

The runner accepts the complete CSV without a default row cap (`python run.py --input path/to/sample.csv`). CSV loading, profiling, and rule checks are linear in the number of rows. Near-duplicate detection uses an inverted token index, ignores extremely common tokens, and caps candidate comparisons per row; this replaces the original O(n²) pairwise scan. The 76k-row dataset should be processed as one in-memory batch on a typical development machine, subject to available RAM and the width of the CSV.

The benchmark intentionally injects each defect into a copy of the input. For a large sample this repeats work across the 12 defect scenarios and increases peak memory. Use `--rows` for a smaller smoke test; do not use a truncated run as the final 76k-row measurement. Record hardware, Python version, input row count, and wall-clock time when publishing benchmark claims.

## Production target: 50 million rows/day, 120 customer schemas

Use a schema registry per customer with versioned mappings into a canonical 311-like record. Run column normalization, type checks, date parsing, coordinate bounds, PII regex, and exact fingerprints in a vectorized streaming engine (Arrow/Polars/Spark) with bounded memory. Partition by customer and ingestion batch; maintain a compact baseline profile per schema version.

Run statistical checks once per batch, not once per row. Keep a small reservoir sample of clean rows for threshold calibration. Route only rule/statistics candidates and an auditable random sample to Gemini. Apply a token-bucket budget per customer, cache review results by row fingerprint plus prompt/model version, and preserve detector evidence in an append-only findings table.

At 50M rows/day, the dominant control is backpressure: queue candidate reviews, enforce timeouts, and never block ingestion on the LLM. Alert metrics should include row throughput, candidate rate, review backlog, false-alarm estimates, schema drift, and cost per million rows. Customers with a new schema version start in shadow mode until profile and clean-batch checks pass.
