
import json

import project_a.evaluation.rules_evaluator as evaluator


def test_rules_evaluator(tmp_path, monkeypatch):
    input_file = tmp_path / "test_cases.json"
    output_file = tmp_path / "rules_results.json"

    cases = [
        {
            "case_id": 1,
            "gross_salary": 1200000,
            "regime": "new_regime",
            "is_resident": True,
            "deductions": {
                "section_80c": 0,
                "section_80ccd_1b": 0,
                "health_self": 0,
                "health_parents": 0,
                "home_loan_interest": 0
            }
        }
    ]

    input_file.write_text(json.dumps(cases), encoding="utf-8")

    monkeypatch.setattr(evaluator, "INPUT_FILE", input_file)
    monkeypatch.setattr(evaluator, "OUTPUT_FILE", output_file)

    results = evaluator.evaluate_rules_cases()

    assert len(results) == 1
    assert results[0]["status"] == "success"
    assert output_file.exists()
