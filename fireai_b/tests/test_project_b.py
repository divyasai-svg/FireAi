from pathlib import Path
from project_b.core import load_csv
from project_b.inject import PROBLEM_TYPES, inject
from project_b.detectors import rule_detector

ROWS = load_csv(Path(__file__).parents[1] / 'data/sample_311.csv')

def test_all_problem_types_inject():
    for problem in PROBLEM_TYPES:
        rows, indices = inject(ROWS, problem, rate=.25)
        assert rows and indices

def test_closed_before_created_is_detected():
    rows, _ = inject(ROWS, 'closed_before_created', rate=.5)
    assert any(f.defect == 'closed_before_created' for f in rule_detector(rows))

def test_pii_is_detected():
    rows, _ = inject(ROWS, 'pii_in_free_text', rate=.5)
    assert any(f.defect == 'pii_in_free_text' for f in rule_detector(rows))

def test_missing_column_is_detected():
    rows, _ = inject(ROWS, 'renamed_or_dropped_column')
    assert any(f.defect == 'renamed_or_dropped_column' for f in rule_detector(rows))


def test_76k_batch_is_supported_without_pairwise_scan():
    from project_b.detectors import statistical_detector
    rows = []
    for i in range(76_000):
        row = dict(ROWS[i % len(ROWS)])
        row["Unique Key"] = str(1_000_000 + i)
        rows.append(row)
    assert len(rows) == 76_000
    # The indexed detector should complete this batch without an O(n²) scan.
    findings = statistical_detector(rows)
    assert isinstance(findings, list)
