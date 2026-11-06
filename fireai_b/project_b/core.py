from __future__ import annotations

import csv
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime
from functools import lru_cache
from pathlib import Path
from typing import Any

REQUIRED = ["Unique Key", "Created Date", "Closed Date", "Complaint Type", "Descriptor", "Status", "Incident Zip", "Borough", "Latitude", "Longitude", "Resolution Description"]
DATE_FORMATS = [
    "%m/%d/%Y %I:%M:%S %p", "%Y-%m-%dT%H:%M:%S",
    "%Y-%m-%d %H:%M:%S", "%Y-%m-%d", "%m/%d/%Y",
    "%m/%d/%Y %H:%M:%S", "%Y-%m-%dT%H:%M:%S.%f",
]
BOROUGH_ZIPS = {"MANHATTAN": range(10001, 10283), "BRONX": range(10451, 10476), "BROOKLYN": range(11201, 11257), "QUEENS": range(11001, 11698), "STATEN ISLAND": range(10301, 10315)}

@dataclass
class Finding:
    defect: str
    row: int | None
    message: str
    detector: str
    evidence: dict[str, Any]


def load_csv(path: str | Path, limit: int | None = None) -> list[dict[str, str]]:
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            raise ValueError(f"CSV has no header: {path}")
        rows = []
        for row in reader:
            # DictReader uses a None key for surplus fields; preserve valid columns only.
            rows.append({str(k): (v or "") for k, v in row.items() if k is not None})
            if limit is not None and limit > 0 and len(rows) >= limit:
                break
        return rows


@lru_cache(maxsize=100_000)
def parse_date(value: str | None) -> datetime | None:
    if not value or not value.strip():
        return None
    value = value.strip()
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(value.strip(), fmt)
        except ValueError:
            pass
    return None


def profile(rows: list[dict[str, str]]) -> dict[str, Any]:
    columns = list(rows[0]) if rows else []
    missing = {c: sum(1 for r in rows if not r.get(c, "").strip()) for c in columns}
    types = {}
    for c in columns:
        vals = [r.get(c, "") for r in rows if r.get(c, "")]
        numeric = sum(_number(v) is not None for v in vals)
        if vals and numeric == len(vals):
            types[c] = "numeric"
        else:
            # Avoid trying every date format on obvious free-text columns.
            date_like = [v for v in vals if re.match(r"^\\d{1,4}[-/]", v.strip())]
            dates = sum(parse_date(v) is not None for v in date_like)
            types[c] = "date" if vals and len(date_like) == len(vals) and dates == len(vals) else "string"
    return {"rows": len(rows), "columns": columns, "missing": missing, "inferred_types": types, "exact_duplicate_rows": len(rows) - len({tuple(r.get(c, "") for c in columns) for r in rows})}


def _number(value: str) -> float | None:
    try:
        return float(value.strip())
    except (ValueError, AttributeError):
        return None


def norm_text(value: str | None) -> str:
    return re.sub(r"\s+", " ", (value or "").strip().lower())


def has_pii(value: str | None) -> bool:
    text = value or ""
    return bool(re.search(r"(?:\+?\d[\d .()\-]{8,}\d|[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}|\b(?:mr|mrs|ms|dr)\.?\s+[A-Z][a-z]+)", text, re.I))


def zip_borough_match(zip_code: str, borough: str) -> bool:
    try:
        z = int(zip_code)
    except (ValueError, TypeError):
        return False
    return z in BOROUGH_ZIPS.get((borough or "").strip().upper(), range(0))


def similarity(a: str, b: str) -> float:
    sa, sb = set(norm_text(a).split()), set(norm_text(b).split())
    return len(sa & sb) / max(1, len(sa | sb))
