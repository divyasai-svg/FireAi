
import json

from project_a.llm_compiled.rule_compiler import (
    build_compilation_prompt,
    save_compiled_rules
)


def test_compilation_prompt_contains_rules():
    prompt = build_compilation_prompt()

    assert "FY 2024-25" in prompt
    assert "old_regime" in prompt
    assert "new_regime" in prompt
    assert "Return valid JSON only" in prompt


def test_save_compiled_rules(tmp_path, monkeypatch):
    import project_a.llm_compiled.rule_compiler as compiler

    output_file = tmp_path / "compiled_tax_rules.json"
    monkeypatch.setattr(compiler, "COMPILED_FILE", output_file)

    response = json.dumps({
        "financial_year": "2024-25",
        "old_regime": {"slabs": []},
        "new_regime": {"slabs": []}
    })

    result = save_compiled_rules(response)

    assert result["financial_year"] == "2024-25"
    assert output_file.exists()
