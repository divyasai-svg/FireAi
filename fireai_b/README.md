# Fire AI Take-Home — Project B

A reproducible NYC 311 data-quality laboratory. The project profiles raw records, injects 12 controlled defect classes, compares declarative rules, statistical detectors, and an LLM-review adapter, then measures a hybrid pipeline.

## Quick start

```bash
python3 run.py
```

The command uses the bundled demonstration fixture in `data/sample_311.csv`, runs injection, detection, benchmarks, and writes `reports/RESULTS_B.md`.

To process the complete 76k-row sample (or any larger CSV), pass its path and omit `--rows` so no row limit is applied:

```bash
python3 run.py --input /path/to/sample_76k.csv
```

For a quick smoke test, limit the input explicitly:

```bash
python3 run.py --input /path/to/sample_76k.csv --rows 5000
```

The CSV loader reads every record by default. Near-duplicate detection uses an inverted token index and bounded candidate comparisons rather than a quadratic all-pairs scan. The pipeline still holds the loaded rows in memory, so for multi-million-row files use a streaming/distributed engine as described in `reports/SCALE_DESIGN.md`.

The default schema is compatible with the NYC 311 columns used by the assignment: `Unique Key`, `Created Date`, `Closed Date`, `Complaint Type`, `Descriptor`, `Status`, `Incident Zip`, `Borough`, `Latitude`, `Longitude`, and `Resolution Description`.

## Design

- **Rules** are used for schema, dates, coordinates, duplicates, cross-field contradictions, ZIP/borough consistency, and PII patterns. They are cheap, explainable, and row-level.
- **Statistics** are used for near-duplicate similarity and null-spike detection, where thresholds should be learned from a clean baseline rather than hard-coded.
- **LLM review** is represented by a deterministic, provider-neutral adapter. It receives only rows already flagged by cheap checks or a controlled sample. The adapter can be replaced with Gemini without changing the pipeline contract; no network call is required for the reproducible run.
- **Hybrid routing** runs rules on every row, statistics per batch, and LLM review only for flagged/sample rows. It returns evidence and detector provenance for auditability.

## Defect classes

The injector supports the assignment's twelve classes: renamed/dropped column, column type change, date format switch, swapped latitude/longitude, exact duplicates, near-duplicates, null spike, closed-before-created, ZIP/borough inconsistency, complaint-type/descriptor inconsistency, resolution/status contradiction, and PII in free text.

See `reports/RESULTS_B.md`, `reports/DECISION_MATRIX.md`, and `reports/AI_USAGE.md` for measured results and design rationale.
