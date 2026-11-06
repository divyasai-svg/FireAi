
import json
from pathlib import Path


def test_dataset_contains_200_cases():
    project_root = Path(__file__).resolve().parents[1]
    dataset_file = project_root / "data" / "test_cases.json"

    with open(dataset_file, "r", encoding="utf-8") as file:
        cases = json.load(file)

    assert len(cases) == 200


def test_dataset_has_both_regimes():
    project_root = Path(__file__).resolve().parents[1]
    dataset_file = project_root / "data" / "test_cases.json"

    with open(dataset_file, "r", encoding="utf-8") as file:
        cases = json.load(file)

    regimes = {case["regime"] for case in cases}

    assert regimes == {"old_regime", "new_regime"}


def test_dataset_has_unique_case_ids():
    project_root = Path(__file__).resolve().parents[1]
    dataset_file = project_root / "data" / "test_cases.json"

    with open(dataset_file, "r", encoding="utf-8") as file:
        cases = json.load(file)

    ids = [case["case_id"] for case in cases]

    assert len(ids) == len(set(ids))
