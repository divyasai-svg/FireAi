
import json

import project_a.evaluation.parser_evaluator as evaluator


def test_parser_evaluator(tmp_path, monkeypatch):
    input_file = tmp_path / "natural_language_cases.json"
    output_file = tmp_path / "parser_results.json"

    cases = [
        {
            "case_id": 1,
            "query": "Calculate my income tax for a salary of 12 lakh under the new regime.",
            "expected_salary": "12 lakh",
            "expected_regime": "new"
        }
    ]

    input_file.write_text(json.dumps(cases), encoding="utf-8")

    monkeypatch.setattr(evaluator, "INPUT_FILE", input_file)
    monkeypatch.setattr(evaluator, "OUTPUT_FILE", output_file)

    results = evaluator.evaluate_parser()

    assert len(results) == 1
    assert results[0]["passed"] is True
    assert output_file.exists()
