# Decision Matrix — Rules, Statistics, or LLM Review?

The data-quality pipeline uses three detector families: declarative rules, statistical/ML checks, and LLM-based review. The detector is selected according to the nature of each data-quality problem, its expected accuracy, computational cost, and the risk of false alarms.

| Check / Component | Primary Detector | Evidence / Measurement | Why This Is the Default |
|---|---|---|---|
| Renamed or dropped column | Rule (Schema validation) | Compare incoming column names against the required schema; report missing and unexpected columns. | Schema requirements are explicit and deterministic. An LLM is unnecessary for checking column names. |
| Column type change | Rule (Type validation) | Validate expected data types for dates, coordinates, ZIP codes, and other required fields. Measure invalid-value counts. | Type constraints are directly testable and provide precise, explainable failures. |
| Date format switch | Rule (Date validation) | Parse dates using the expected format and compare format distributions across the batch. Measure unparseable and inconsistent date counts. | Date formats and timestamp parsing should follow explicit rules rather than model interpretation. |
| Latitude/Longitude swapped | Rule (Geospatial validation) | Check numeric values, coordinate ranges, and NYC geographic bounding-box constraints. | Geographic bounds are known invariants. Rules are fast and auditable. |
| Exact duplicates | Rule (Fingerprinting) | Generate a stable fingerprint from selected columns and identify repeated fingerprints. Measure duplicate count and percentage. | Exact equality is deterministic; statistical or LLM-based interpretation adds no value. |
| Near duplicates | Statistical (Similarity detection) | Calculate token Jaccard similarity between normalized text records. Flag pairs exceeding a threshold calibrated on clean data. Measure precision and recall. | Similarity is a scored problem. Statistical thresholds can identify similar records without expensive LLM calls. |
| Null spike in one agency | Statistical (Distribution monitoring) | Calculate null percentage per agency and compare it with the clean-data baseline using a threshold or statistical deviation. | A null spike is a batch-level distribution change, not necessarily an individual-row error. |
| Closed Date earlier than Created Date | Rule (Temporal validation) | Parse both timestamps and flag records where Closed Date is earlier than Created Date. | This is a clear temporal invariant that can be checked deterministically. |
| ZIP inconsistent with Borough | Rule (Reference-data validation) | Validate ZIP codes against a maintained ZIP-to-Borough reference mapping. | Reference data provides an explicit and auditable consistency check. |
| Complaint Type inconsistent with Descriptor | Hybrid (Rules + LLM review) | Rules identify suspicious category-description combinations. An LLM reviews only ambiguous flagged records using the complaint type and descriptor as evidence. | Taxonomies can contain variations and ambiguous descriptions. Rules reduce the candidate set while LLM review handles nuanced cases. |
| Resolution Description contradicts Status | Rule + LLM review | Rules detect clear contradictions between status and resolution text. LLM review is reserved for borderline or context-dependent wording. | Explicit status conflicts are deterministic, while nuanced language may require contextual interpretation. |
| PII in free text | Rule + LLM review | Regex patterns detect emails, phone numbers, and other recognizable identifiers. LLM review may classify selected ambiguous cases after sensitive values are masked. | Regex provides fast, high-precision detection. LLM review is limited to uncertain cases to reduce privacy exposure and cost. |

## Overall Production Routing Decision

The production pipeline uses a hybrid architecture:

1. **Rules on every incoming row:** Perform schema, type, date, coordinate, duplicate, ZIP/Borough, temporal, and other deterministic checks.
2. **Statistical checks at batch level:** Monitor null percentages, distribution changes, and near-duplicate similarity.
3. **LLM review only for selected candidates:** Send only ambiguous records flagged by rules or statistical checks, after masking sensitive information where applicable.
4. **Final decision and reporting:** Combine detector findings, preserve evidence, and produce a structured quality report for downstream dashboards.

## Evaluation Criteria

Each detector family will be evaluated using:

- **Detection rate (Recall):** Percentage of injected corruptions successfully detected.
- **False-alarm rate:** Percentage of clean records incorrectly flagged.
- **Cost per million rows:** Estimated or measured processing cost.
- **Throughput:** Number of rows processed per second on the test machine.
- **Explanation clarity:** Whether the finding includes understandable evidence explaining why the record was flagged.

The final production choice will favor detectors that provide high detection rates, low false-alarm rates, clear explanations, and acceptable processing cost.