
import json

import project_a.llm_compiled.compiled_query as compiled_query


def test_compiled_query_requires_compiled_file(tmp_path, monkeypatch):
    missing_file = tmp_path / "missing.json"
    monkeypatch.setattr(
        compiled_query, "COMPILED_FILE", missing_file
    )

    try:
        compiled_query.run_compiled_query("Calculate tax on 12 lakh")
        assert False, "Expected FileNotFoundError"
    except FileNotFoundError:
        assert True


def test_compiled_query_loads_saved_rules(tmp_path, monkeypatch):
    rules_file = tmp_path / "compiled_tax_rules.json"

    rules = {
        "financial_year": "2024-25",
        "old_regime": {"slabs": []},
        "new_regime": {"slabs": []}
    }

    rules_file.write_text(json.dumps(rules), encoding="utf-8")

    monkeypatch.setattr(
        compiled_query, "COMPILED_FILE", rules_file
    )

    def fake_ask_llm(prompt):
        assert "2024-25" in prompt
        assert "Calculate tax on 12 lakh" in prompt
        return "Test response"

    monkeypatch.setattr(compiled_query, "ask_llm", fake_ask_llm)

    result = compiled_query.run_compiled_query(
        "Calculate tax on 12 lakh"
    )

    assert result == "Test response"
