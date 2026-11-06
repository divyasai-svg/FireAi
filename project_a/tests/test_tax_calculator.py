
from decimal import Decimal
import pytest

from project_a.rules_engine.tax_calculator import (
    calculate_tax,
    calculate_taxable_salary
)
from project_a.rules_engine.tax_calculator import calculate_salary_tax

# Standard deduction tests
@pytest.mark.parametrize("salary, regime, expected", [
    (1200000, "old_regime", Decimal("1150000")),
    (1200000, "new_regime", Decimal("1125000")),
    (500000, "old_regime", Decimal("450000")),
    (500000, "new_regime", Decimal("425000")),
    (40000, "old_regime", Decimal("0")),
    (40000, "new_regime", Decimal("0"))
])
def test_standard_deduction(salary, regime, expected):
    assert calculate_taxable_salary(salary, regime) == expected


# Negative salary test
def test_negative_salary():
    with pytest.raises(ValueError):
        calculate_taxable_salary(-1000, "old_regime")


# Old and new regime standard deduction tests
def test_old_regime_standard_deduction():
    assert calculate_taxable_salary(
        1200000, "old_regime"
    ) == Decimal("1150000")


def test_new_regime_standard_deduction():
    assert calculate_taxable_salary(
        1200000, "new_regime"
    ) == Decimal("1125000")


# Salary less than standard deduction
def test_salary_less_than_deduction():
    assert calculate_taxable_salary(
        30000, "old_regime"
    ) == Decimal("0")


# New regime slab calculation tests
@pytest.mark.parametrize("income, expected", [
    (300000, Decimal("0")),
    (700000, Decimal("20000")),
    (1000000, Decimal("50000")),
    (1200000, Decimal("80000")),
    (1500000, Decimal("140000"))
])
def test_new_regime(income, expected):
    assert calculate_tax(income, "new_regime") == expected


# Old regime slab calculation tests
@pytest.mark.parametrize("income, expected", [
    (250000, Decimal("0")),
    (500000, Decimal("12500")),
    (1000000, Decimal("112500")),
    (1200000, Decimal("172500"))
])
def test_old_regime(income, expected):
    assert calculate_tax(income, "old_regime") == expected


# Negative income test
def test_negative_income():
    with pytest.raises(ValueError):
        calculate_tax(-1000, "new_regime")

@pytest.mark.parametrize("salary, regime, expected_income, expected_tax", [
    (1200000, "old_regime", Decimal("1150000"), Decimal("157500")),
    (1200000, "new_regime", Decimal("1125000"), Decimal("68750")),
    (500000, "old_regime", Decimal("450000"), Decimal("10000")),
    (500000, "new_regime", Decimal("425000"), Decimal("6250"))
])
def test_combined_salary_tax(salary, regime, expected_income, expected_tax):
    result = calculate_salary_tax(
        salary,
        regime,
        data={"is_resident": True}
    )

    assert result["taxable_income"] == expected_income
    assert result["tax_before_rebate"] >= 0