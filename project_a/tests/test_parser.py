from decimal import Decimal
from project_a.parser.nl_parser import parse_tax_query


def test_parse_new_regime():
    result = parse_tax_query("My salary is 12 lakh and I choose new regime")

    assert result["status"] == "success"
    assert result["gross_salary"] == Decimal("1200000")
    assert result["regime"] == "new_regime"


def test_parse_old_regime():
    result = parse_tax_query("My annual salary is 8 lakh under old regime")

    assert result["status"] == "success"
    assert result["gross_salary"] == Decimal("800000")
    assert result["regime"] == "old_regime"


def test_missing_regime():
    result = parse_tax_query("My salary is 12 lakh")

    assert result["status"] == "needs_clarification"


def test_missing_salary():
    result = parse_tax_query("Calculate my tax under new regime")

    assert result["status"] == "needs_clarification"