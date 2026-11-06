from project_a.llm_query.tax_prompt import build_tax_prompt


def test_prompt_contains_tax_rules():
    prompt = build_tax_prompt("My salary is 12 lakh under new regime")

    assert "FY 2024-25" in prompt
    assert "12 lakh" in prompt
    assert "new_regime" in prompt


def test_prompt_requests_clarification():
    prompt = build_tax_prompt("Calculate my income tax")

    assert "Ask for clarification" in prompt
    assert "Do not invent" in prompt