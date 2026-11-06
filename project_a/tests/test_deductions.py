from decimal import Decimal
from project_a.rules_engine.deductions import calculate_deductions


def test_new_regime_no_old_regime_deductions():
    data = {
        "section_80c": 150000,
        "section_80ccd_1b": 50000,
        "health_self": 25000,
        "home_loan_interest": 200000
    }

    result = calculate_deductions(data, "new_regime")

    assert all(value == 0 for value in result.values())


def test_old_regime_80c_limit():
    data = {"section_80c": 200000}

    result = calculate_deductions(data, "old_regime")

    assert result["section_80c"] == Decimal("150000")


def test_old_regime_80ccd_1b_limit():
    data = {"section_80ccd_1b": 70000}

    result = calculate_deductions(data, "old_regime")

    assert result["section_80ccd_1b"] == Decimal("50000")


def test_old_regime_home_loan_interest_limit():
    data = {"home_loan_interest": 250000}

    result = calculate_deductions(data, "old_regime")

    assert result["home_loan_interest"] == Decimal("200000")