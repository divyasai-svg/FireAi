
from decimal import Decimal
import pytest

from project_a.rules_engine.tax_calculator import calculate_rebate


@pytest.mark.parametrize("income, tax, regime, expected", [
    (500000, 12500, "old_regime", 12500),
    (400000, 7500, "old_regime", 7500),
    (700000, 25000, "new_regime", 25000),
    (700100, 20010, "new_regime", 19910),
    (800000, 30000, "new_regime", 0)
])
def test_rebate(income, tax, regime, expected):

    result = calculate_rebate(
        income, tax, regime, True
    )

    assert result == Decimal(str(expected))


def test_non_resident_no_rebate():

    result = calculate_rebate(
        500000, 12500, "old_regime", False
    )

    assert result == Decimal("0")
