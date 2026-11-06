
from decimal import Decimal


def calculate_deductions(data, regime):

    if regime not in ["old_regime", "new_regime"]:
        raise ValueError("Invalid tax regime")

    # New regime does not allow these deductions
    if regime == "new_regime":
        return {
            "hra_exemption": Decimal("0"),
            "section_80c": Decimal("0"),
            "section_80ccd_1b": Decimal("0"),
            "section_80d": Decimal("0"),
            "home_loan_interest": Decimal("0"),
            "total_deductions": Decimal("0")
        }

    # Convert inputs into Decimal
    basic_salary = Decimal(str(data.get("basic_salary", 0)))
    da = Decimal(str(data.get("da", 0)))
    hra_received = Decimal(str(data.get("hra_received", 0)))
    rent_paid = Decimal(str(data.get("rent_paid", 0)))

    section_80c = Decimal(str(data.get("section_80c", 0)))
    section_80ccd_1b = Decimal(str(data.get("section_80ccd_1b", 0)))

    health_self = Decimal(str(data.get("health_self", 0)))
    health_parents = Decimal(str(data.get("health_parents", 0)))

    home_loan_interest = Decimal(
        str(data.get("home_loan_interest", 0))
    )

    # Validate non-negative amounts
    amounts = [
        basic_salary, da, hra_received, rent_paid,
        section_80c, section_80ccd_1b,
        health_self, health_parents, home_loan_interest
    ]

    if any(amount < 0 for amount in amounts):
        raise ValueError("Amounts cannot be negative")

    # HRA exemption calculation
    hra_exemption = Decimal("0")

    if rent_paid > 0:
        salary_for_hra = basic_salary + da

        metro = data.get("is_metro", False)

        metro_percentage = Decimal("0.50") if metro else Decimal("0.40")

        hra_limit_1 = hra_received
        hra_limit_2 = rent_paid - (salary_for_hra * Decimal("0.10"))
        hra_limit_3 = salary_for_hra * metro_percentage

        hra_exemption = max(
            Decimal("0"),
            min(hra_limit_1, hra_limit_2, hra_limit_3)
        )

    # Section 80C maximum limit
    section_80c = min(
        section_80c,
        Decimal("150000")
    )

    # Section 80CCD(1B) maximum limit
    section_80ccd_1b = min(
        section_80ccd_1b,
        Decimal("50000")
    )

    # Section 80D
    self_is_senior = data.get("self_is_senior", False)
    parents_are_senior = data.get("parents_are_senior", False)

    self_limit = Decimal("50000") if self_is_senior else Decimal("25000")
    parents_limit = Decimal("50000") if parents_are_senior else Decimal("25000")

    allowed_self = min(health_self, self_limit)
    allowed_parents = min(health_parents, parents_limit)

    section_80d = allowed_self + allowed_parents

    # Home loan interest for self-occupied property
    home_loan_interest = min(
        home_loan_interest,
        Decimal("200000")
    )

    # Total deductions and exemptions
    total_deductions = (
        hra_exemption
        + section_80c
        + section_80ccd_1b
        + section_80d
        + home_loan_interest
    )

    return {
        "hra_exemption": hra_exemption,
        "section_80c": section_80c,
        "section_80ccd_1b": section_80ccd_1b,
        "section_80d": section_80d,
        "home_loan_interest": home_loan_interest,
        "total_deductions": total_deductions
    }
