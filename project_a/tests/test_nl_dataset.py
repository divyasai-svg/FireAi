
import json
from pathlib import Path


def test_natural_language_dataset_has_50_cases():
    project_root = Path(__file__).resolve().parents[1]
    file_path = project_root / "data" / "natural_language_cases.json"

    with open(file_path, "r", encoding="utf-8") as file:
        cases = json.load(file)

    assert len(cases) == 50


def test_natural_language_cases_have_required_fields():
    project_root = Path(__file__).resolve().parents[1]
    file_path = project_root / "data" / "natural_language_cases.json"

    with open(file_path, "r", encoding="utf-8") as file:
        cases = json.load(file)

    for case in cases:
        assert "query" in case
        assert "expected_salary" in case
        assert "expected_regime" in case
