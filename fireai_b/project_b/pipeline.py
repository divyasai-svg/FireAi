from __future__ import annotations

from collections import defaultdict
from .detectors import rule_detector, statistical_detector, llm_review


def hybrid(rows):
    rules = rule_detector(rows)
    stats = statistical_detector(rows)
    candidates = rules + stats
    reviewed = llm_review(rows, candidates)
    all_findings = candidates + reviewed
    by_defect = defaultdict(list)
    for f in all_findings: by_defect[f.defect].append(f)
    return {"findings": all_findings, "by_defect": dict(by_defect), "counts": {k: len(v) for k, v in by_defect.items()}, "routing": {"rules_rows": len(rows), "statistics_rows": len(rows), "llm_rows": len({f.row for f in candidates if f.row is not None})}}


def detection_metrics(findings, injected_indices, problem):
    found = {f.row for f in findings if f.defect == problem and f.row is not None}
    if problem == "renamed_or_dropped_column":
        detected = any(f.defect == problem for f in findings)
        return {"problem": problem, "injected": len(injected_indices), "detected": len(injected_indices) if detected else 0, "true_positive": len(injected_indices) if detected else 0, "false_negative": 0 if detected else len(injected_indices), "false_positive": 0, "detection_rate": 1.0 if detected else 0.0, "false_alarm_rate": 0.0}
    if problem in {"exact_duplicate", "near_duplicate"}:
        found_count = len([f for f in findings if f.defect == problem])
        return {"problem": problem, "injected": len(injected_indices), "detected": found_count, "true_positive": min(found_count, len(injected_indices)), "false_negative": max(0, len(injected_indices)-found_count), "false_positive": max(0, found_count-len(injected_indices)), "detection_rate": round(min(found_count, len(injected_indices)) / max(1, len(injected_indices)), 3), "false_alarm_rate": round(max(0, found_count-len(injected_indices)) / max(1, len(findings)), 3)}
    tp = len(found & set(injected_indices)); fn = len(set(injected_indices) - found); fp = len(found - set(injected_indices))
    return {"problem": problem, "injected": len(injected_indices), "detected": len(found), "true_positive": tp, "false_negative": fn, "false_positive": fp, "detection_rate": round(tp / max(1, len(injected_indices)), 3), "false_alarm_rate": round(fp / max(1, len(findings)), 3)}
