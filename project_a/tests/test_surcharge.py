from decimal import Decimal
from project_a.rules_engine.tax_calculator import calculate_surcharge


def test_no_surcharge_below_50_lakh():
    result = calculate_surcharge(4000000, 800000, "old_regime")
    assert result == Decimal("0")


def test_surcharge_above_50_lakh():
    result = calculate_surcharge(6000000, 1500000, "old_regime")
    assert result == Decimal("150000")


def test_new_regime_surcharge_above_5_crore():
    result = calculate_surcharge(60000000, 17000000, "new_regime")
    assert result == Decimal("4250000")


def test_old_regime_surcharge_above_5_crore():
    result = calculate_surcharge(60000000, 17000000, "old_regime")
    assert result == Decimal("6290000")