
import json

import project_a.evaluation.compare_approaches as comparison


def test_comparison_report(tmp_path, monkeypatch):
    monkeypatch.setattr(comparison, "DATA_DIR", tmp_path)
    monkeypatch.setattr(
        comparison,
        "OUTPUT_FILE",
        tmp_path / "comparison_results.json"
    )

    rules = [
        {"status": "success"},
        {"status": "error"}
    ]

    parser = [
        {"passed": True},
        {"passed": False}
    ]

    (tmp_path / "rules_results.json").write_text(
        json.dumps(rules), encoding="utf-8"
    )

    (tmp_path / "parser_results.json").write_text(
        json.dumps(parser), encoding="utf-8"
    )

    result = comparison.compare_approaches()

    assert result["rules_based"]["success_rate"] == 50.0
    assert result["parser"]["accuracy"] == 50.0
    assert (tmp_path / "comparison_results.json").exists()
