from project_a.parser.input_parser import parse_salary_input


def test_salary_and_new_regime():
    result = parse_salary_input(
        "My annual salary is 1200000 and I want the new regime"
    )

    assert result["gross_salary"] == 1200000
    assert result["regime"] == "new_regime"
    assert result["missing_fields"] == []


def test_salary_in_lakhs():
    result = parse_salary_input(
        "My salary is 12 lakh under old regime"
    )

    assert result["gross_salary"] == 1200000
    assert result["regime"] == "old_regime"


def test_missing_salary():
    result = parse_salary_input("I want the new regime")

    assert result["gross_salary"] is None
    assert "annual salary" in result["missing_fields"]


def test_missing_regime():
    result = parse_salary_input("My salary is 1200000")

    assert result["gross_salary"] == 1200000
    assert "tax regime" in result["missing_fields"]