# Project B results

Source: `data/export.csv`

## Raw profile

- Rows: 76182
- Columns: Unique Key, Created Date, Closed Date, Agency, Agency Name, Problem (formerly Complaint Type), Problem Detail (formerly Descriptor), Additional Details, Location Type, Incident Zip, Incident Address, Street Name, Cross Street 1, Cross Street 2, Intersection Street 1, Intersection Street 2, Address Type, City, Landmark, Facility Type, Status, Due Date, Resolution Description, Resolution Action Updated Date, Community Board, Council District, Police Precinct, BBL, Borough, X Coordinate (State Plane), Y Coordinate (State Plane), Open Data Channel Type, Park Facility Name, Park Borough, Vehicle Type, Taxi Company Borough, Taxi Pick Up Location, Bridge Highway Name, Bridge Highway Direction, Road Ramp, Bridge Highway Segment, Latitude, Longitude, Location
- Exact duplicate rows in baseline: 0

## Detector comparison

| Problem | Injected | Detected | Detection rate | False alarms | Rules ms | Statistics ms | Hybrid ms |
|---|---:|---:|---:|---:|---:|---:|---:|
| renamed_or_dropped_column | 19045 | 19045 | 100.0% | 0 | 5583.551 | 139.666 | 4830.804 |
| column_type_change | 19045 | 20104 | 100.0% | 1059 | 4904.730 | 175.609 | 4799.884 |
| date_format_switch | 19045 | 19044 | 100.0% | 0 | 5287.181 | 183.470 | 4765.661 |
| lat_long_swapped | 19045 | 18753 | 98.5% | 0 | 4967.119 | 192.756 | 4860.910 |
| exact_duplicate | 19045 | 19045 | 100.0% | 0 | 5988.198 | 252.170 | 6066.926 |
| near_duplicate | 19045 | 0 | 0.0% | 0 | 6194.721 | 243.388 | 6422.220 |
| null_spike | 19045 | 76182 | 100.0% | 57137 | 4922.596 | 137.863 | 4959.744 |
| closed_before_created | 19045 | 19068 | 100.0% | 24 | 4960.115 | 219.956 | 5645.246 |
| zip_borough_inconsistent | 19045 | 19582 | 100.0% | 537 | 4911.475 | 191.800 | 4958.432 |
| complaint_descriptor_inconsistent | 19045 | 19045 | 100.0% | 0 | 4818.049 | 264.696 | 5087.137 |
| resolution_status_contradiction | 19045 | 19045 | 100.0% | 0 | 3771.506 | 193.011 | 4211.494 |
| pii_in_free_text | 19045 | 20591 | 100.0% | 1546 | 3936.694 | 194.477 | 4380.846 |

## Interpretation

The fixture is intentionally small, so throughput numbers are directional rather than production capacity claims. Run the same command against a representative extract for final capacity figures. Rules run on every row and provide deterministic evidence. Statistics are batch-scoped. The LLM adapter is only reached for candidate rows and is provider-neutral in this offline build; the production Gemini adapter should emit structured JSON with quoted evidence spans and a confidence value.

## Cost model

Let `N` be rows/day, `p` the fraction flagged by rules/statistics, and `c` the Gemini cost per reviewed row. The hybrid LLM cost is `N × p × c`, versus `N × c` for LLM-on-every-row. The measured routing count is written into `raw_metrics.json` for each run.
