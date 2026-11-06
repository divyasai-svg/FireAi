from __future__ import annotations

from collections import Counter
from .core import Finding, REQUIRED, has_pii, norm_text, parse_date, similarity, zip_borough_match


def schema_rules(rows):
    cols = set(rows[0]) if rows else set()
    return [Finding("renamed_or_dropped_column", None, f"Missing required columns: {sorted(set(REQUIRED)-cols)}", "rules", {"missing": sorted(set(REQUIRED)-cols)})] if set(REQUIRED) - cols else []


def rule_detector(rows):
    findings = schema_rules(rows)
    if not rows: return findings
    date_values = [r.get("Created Date", "") for r in rows if r.get("Created Date")]
    slash_share = sum("/" in v for v in date_values) / max(1, len(date_values))
    for i, r in enumerate(rows):
        created, closed = parse_date(r.get("Created Date")), parse_date(r.get("Closed Date"))
        if r.get("Created Date") and ((slash_share > 0.5 and "T" in r.get("Created Date")) or (slash_share <= 0.5 and "/" in r.get("Created Date"))):
            findings.append(Finding("date_format_switch", i, "Created Date format differs from batch baseline", "rules", {"value": r.get("Created Date")}))
        if r.get("Created Date") and created is None: findings.append(Finding("date_format_switch", i, "Created Date is not parseable", "rules", {"value": r.get("Created Date")}))
        if r.get("Closed Date") and closed is None: findings.append(Finding("date_format_switch", i, "Closed Date is not parseable", "rules", {"value": r.get("Closed Date")}))
        if created and closed and closed < created: findings.append(Finding("closed_before_created", i, "Closed Date precedes Created Date", "rules", {}))
        try:
            lat, lon = float(r.get("Latitude", "")), float(r.get("Longitude", ""))
            if not (40.4 <= lat <= 41.1 and -74.3 <= lon <= -73.6): findings.append(Finding("lat_long_swapped", i, "Coordinates outside NYC bounds", "rules", {"lat": lat, "lon": lon}))
        except ValueError: findings.append(Finding("column_type_change", i, "Latitude/Longitude are not numeric", "rules", {}))
        try: int(r.get("Incident Zip", ""))
        except ValueError: findings.append(Finding("column_type_change", i, "Incident Zip is not an integer ZIP", "rules", {"value": r.get("Incident Zip")}))
        if not zip_borough_match(r.get("Incident Zip"), r.get("Borough")): findings.append(Finding("zip_borough_inconsistent", i, "ZIP does not map to Borough", "rules", {"zip": r.get("Incident Zip"), "borough": r.get("Borough")}))
        status, resolution = norm_text(r.get("Status")), norm_text(r.get("Resolution Description"))
        if status in {"open", "pending"} and any(x in resolution for x in ("closed", "resolved")): findings.append(Finding("resolution_status_contradiction", i, "Open/pending status conflicts with resolved text", "rules", {}))
        if has_pii(r.get("Descriptor")) or has_pii(r.get("Resolution Description")): findings.append(Finding("pii_in_free_text", i, "Possible phone, email, or named person in free text", "rules", {}))
        complaint, descriptor = norm_text(r.get("Complaint Type")), norm_text(r.get("Descriptor"))
        if descriptor == "hydrant leaking" and "water" not in complaint and "illegal" not in complaint: findings.append(Finding("complaint_descriptor_inconsistent", i, "Hydrant descriptor is unusual for complaint type", "rules", {}))
    seen = {}
    for i, r in enumerate(rows):
        key = tuple(r.get(c, "") for c in REQUIRED)
        if key in seen: findings.append(Finding("exact_duplicate", i, "Row exactly duplicates an earlier row", "rules", {"first_row": seen[key]}))
        else: seen[key] = i
    return findings


def statistical_detector(rows, max_candidates_per_row=200):
    """Batch checks with bounded near-duplicate work (not an all-pairs scan)."""
    findings = []
    n = len(rows)
    if not n:
        return findings
    desc = [norm_text(r.get("Descriptor")) for r in rows]
    null_count = sum(not value for value in desc)
    null_share = null_count / n
    if null_share >= 0.2:
        findings.extend(Finding("null_spike", i, "Descriptor null share exceeds batch threshold",
                                "statistics", {"null_share": null_share})
                        for i, value in enumerate(desc) if not value)
    counts = Counter(desc)
    for value, count in counts.items():
        if value and count / n >= 0.5:
            findings.extend(Finding("null_spike", i, "Descriptor value dominates batch",
                                    "statistics", {"value": value, "share": count / n})
                            for i, current in enumerate(desc) if current == value)

    token_sets = [set(value.split()) for value in desc]
    doc_freq = Counter(token for tokens in token_sets for token in tokens)
    max_df = max(100, int(n * 0.02))
    postings = {}
    for i, tokens in enumerate(token_sets):
        if not tokens:
            continue
        candidate_ids = set()
        for token in tokens:
            if doc_freq[token] <= max_df:
                candidate_ids.update(postings.get(token, ()))
        checked = 0
        for j in sorted(candidate_ids, reverse=True):
            if rows[j].get("Unique Key") == rows[i].get("Unique Key"):
                continue
            score = similarity(desc[j], desc[i])
            if score >= 0.5:
                findings.append(Finding("near_duplicate", i, "Descriptions are highly similar",
                                        "statistics", {"similarity": score, "other_row": j}))
                break
            checked += 1
            if checked >= max_candidates_per_row:
                break
        for token in tokens:
            if doc_freq[token] <= max_df:
                postings.setdefault(token, []).append(i)
    return findings


def llm_review(rows, candidates):
    # Provider-neutral offline stand-in. In production, serialize candidates to Gemini
    # with a JSON schema and require evidence spans; the pipeline contract is identical.
    out = []
    for f in candidates:
        if f.defect in {"complaint_descriptor_inconsistent", "resolution_status_contradiction", "pii_in_free_text"}:
            out.append(Finding(f.defect, f.row, f.message, "llm_review", {**f.evidence, "review": "confirmed_by_mock_llm"}))
    return out
