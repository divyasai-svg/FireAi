
import json
from decimal import Decimal
from pathlib import Path

from project_a.rules_engine.deductions import calculate_deductions


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RULES_FILE = PROJECT_ROOT / "data" / "tax_rules_2024_25.json"

with open(RULES_FILE, "r", encoding="utf-8") as file:
    TAX_RULES = json.load(file)


def calculate_tax(income, regime):
    income = Decimal(str(income))

    if income < 0:
        raise ValueError("Income cannot be negative")

    if regime not in ("old_regime", "new_regime"):
        raise ValueError("Invalid tax regime")

    slabs = TAX_RULES[regime]["slabs"]
    tax = Decimal("0")

    for slab in slabs:
        lower = Decimal(str(slab["lower_limit"]))

        upper_value = slab["upper_limit"]

        if upper_value is None:
            upper = income
        else:
            upper = Decimal(str(upper_value))

        rate = Decimal(str(slab["rate"]))

        taxable_amount = max(
            Decimal("0"),
            min(income, upper) - lower
        )

        tax += taxable_amount * rate / Decimal("100")

    return tax


def calculate_taxable_salary(gross_salary, regime):
    gross_salary = Decimal(str(gross_salary))

    if gross_salary < 0:
        raise ValueError("Salary cannot be negative")

    standard_deduction = (
        Decimal("50000")
        if regime == "old_regime"
        else Decimal("75000")
    )

    return max(Decimal("0"), gross_salary - standard_deduction)


def calculate_rebate(taxable_income, tax, regime, is_resident):
    income = Decimal(str(taxable_income))
    tax = Decimal(str(tax))

    if not isinstance(is_resident, bool):
        raise ValueError("Resident status must be specified")

    if not is_resident:
        return Decimal("0")

    if regime == "old_regime":
        if income <= Decimal("500000"):
            return min(tax, Decimal("12500"))

    elif regime == "new_regime":
        if income <= Decimal("700000"):
            return min(tax, Decimal("25000"))

        # Marginal relief under Section 87A
        excess_income = income - Decimal("700000")

        if tax > excess_income:
            return tax - excess_income

    else:
        raise ValueError("Invalid tax regime")

    return Decimal("0")


def calculate_surcharge(taxable_income, tax, regime):
    income = Decimal(str(taxable_income))
    tax = Decimal(str(tax))

    if regime not in ("old_regime", "new_regime"):
        raise ValueError("Invalid tax regime")

    if income <= Decimal("5000000"):
        return Decimal("0")

    if income <= Decimal("10000000"):
        rate = Decimal("0.10")
        threshold = Decimal("5000000")
        threshold_rate = Decimal("0")

    elif income <= Decimal("20000000"):
        rate = Decimal("0.15")
        threshold = Decimal("10000000")
        threshold_rate = Decimal("0.10")

    elif income <= Decimal("50000000"):
        rate = Decimal("0.25")
        threshold = Decimal("20000000")
        threshold_rate = Decimal("0.15")

    else:
        threshold = Decimal("50000000")
        threshold_rate = Decimal("0.25")
        rate = (
            Decimal("0.25")
            if regime == "new_regime"
            else Decimal("0.37")
        )

    normal_surcharge = tax * rate
    tax_with_surcharge = tax + normal_surcharge

    tax_at_threshold = calculate_tax(threshold, regime)

    tax_at_threshold_with_surcharge = (
        tax_at_threshold
        + tax_at_threshold * threshold_rate
    )

    maximum_tax_with_marginal_relief = (
        tax_at_threshold_with_surcharge
        + income - threshold
    )

    allowed_total_tax = min(
        tax_with_surcharge,
        maximum_tax_with_marginal_relief
    )

    return max(Decimal("0"), allowed_total_tax - tax)


def calculate_salary_tax(gross_salary, regime, data=None):
    if data is None or "is_resident" not in data:
        raise ValueError("Please specify is_resident in taxpayer data")

    gross_salary = Decimal(str(gross_salary))

    if gross_salary < 0:
        raise ValueError("Salary cannot be negative")

    standard_deduction = (
        Decimal("50000")
        if regime == "old_regime"
        else Decimal("75000")
    )

    deductions = calculate_deductions(data, regime)

    total_deductions = Decimal(
        str(deductions["total_deductions"])
    )

    taxable_income = max(
        Decimal("0"),
        gross_salary - standard_deduction - total_deductions
    )

    tax_before_rebate = calculate_tax(taxable_income, regime)

    rebate = calculate_rebate(
        taxable_income,
        tax_before_rebate,
        regime,
        data["is_resident"]
    )

    tax_after_rebate = max(
        Decimal("0"),
        tax_before_rebate - rebate
    )

    surcharge = calculate_surcharge(
        taxable_income,
        tax_after_rebate,
        regime
    )

    cess = (
        tax_after_rebate + surcharge
    ) * Decimal("0.04")

    total_tax = (
        tax_after_rebate + surcharge + cess
    )

    return {
        "gross_salary": gross_salary,
        "standard_deduction": standard_deduction,
        "deductions": deductions,
        "taxable_income": taxable_income,
        "tax_before_rebate": tax_before_rebate,
        "rebate": rebate,
        "tax_after_rebate": tax_after_rebate,
        "surcharge": surcharge,
        "cess": cess,
        "total_tax": total_tax
    }


if __name__ == "__main__":
    salary = 1200000

    taxpayer_data = {
        "is_resident": True
    }

    old_result = calculate_salary_tax(
        salary,
        "old_regime",
        taxpayer_data
    )

    new_result = calculate_salary_tax(
        salary,
        "new_regime",
        taxpayer_data
    )

    print("OLD REGIME")
    for key, value in old_result.items():
        print(f"{key}: {value}")

    print("\nNEW REGIME")
    for key, value in new_result.items():
        print(f"{key}: {value}")
