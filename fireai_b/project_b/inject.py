from __future__ import annotations

import copy
import random
from datetime import datetime, timedelta
from .core import parse_date
from typing import Callable

PROBLEM_TYPES = ["renamed_or_dropped_column", "column_type_change", "date_format_switch", "lat_long_swapped", "exact_duplicate", "near_duplicate", "null_spike", "closed_before_created", "zip_borough_inconsistent", "complaint_descriptor_inconsistent", "resolution_status_contradiction", "pii_in_free_text"]


def inject(rows: list[dict[str, str]], problem: str, rate: float = 0.1, seed: int = 7) -> tuple[list[dict[str, str]], set[int]]:
    out = copy.deepcopy(rows)
    rng = random.Random(seed)
    n = max(1, int(len(out) * rate))
    indices = set(rng.sample(range(len(out)), min(n, len(out))))
    if problem == "renamed_or_dropped_column":
        for r in out: r["BoroughRenamed"] = r.pop("Borough", "")
    elif problem == "column_type_change":
        for i in indices: out[i]["Incident Zip"] = "ZIP-" + out[i].get("Incident Zip", "")
    elif problem == "date_format_switch":
        for i in indices:
            dt = parse_date(out[i].get("Created Date"))
            if dt is not None:
                out[i]["Created Date"] = dt.strftime("%Y-%m-%dT%H:%M:%S")
    elif problem == "lat_long_swapped":
        for i in indices: out[i]["Latitude"], out[i]["Longitude"] = out[i].get("Longitude", ""), out[i].get("Latitude", "")
    elif problem == "exact_duplicate":
        for i in sorted(indices, reverse=True): out.insert(i, copy.deepcopy(out[i]))
    elif problem == "near_duplicate":
        additions = []
        for i in sorted(indices):
            clone = copy.deepcopy(out[i])
            clone["Unique Key"] = clone.get("Unique Key", "") + "-near"
            clone["Descriptor"] = clone.get("Descriptor", "") + " updated"
            additions.append(clone)
        out.extend(additions)
    elif problem == "null_spike":
        for i in indices: out[i]["Descriptor"] = ""
    elif problem == "closed_before_created":
        for i in indices:
            created = parse_date(out[i].get("Created Date"))
            if created is not None:
                out[i]["Closed Date"] = (created - timedelta(hours=2)).strftime("%m/%d/%Y %I:%M:%S %p")
    elif problem == "zip_borough_inconsistent":
        for i in indices: out[i]["Incident Zip"] = "10001" if out[i].get("Borough") != "MANHATTAN" else "11201"
    elif problem == "complaint_descriptor_inconsistent":
        for i in indices:
            out[i]["Complaint Type"] = "Noise - Residential"
            out[i]["Descriptor"] = "Hydrant Leaking"
    elif problem == "resolution_status_contradiction":
        for i in indices: out[i]["Status"] = "Open"; out[i]["Resolution Description"] = "The complaint was closed and resolved."
    elif problem == "pii_in_free_text":
        for i in indices: out[i]["Descriptor"] = out[i].get("Descriptor", "") + " Contact john.doe@example.com at 212-555-0188"
    else: raise ValueError(f"Unknown problem type: {problem}")
    return out, indices
