
import re
from decimal import Decimal


def parse_tax_query(text):
    text = text.lower().replace(",", "").strip()

    result = {
        "gross_salary": None,
        "regime": None
    }

    pattern = r"(?:₹|rs\.?\s*)?(\d+(?:\.\d+)?)\s*(lakh|lakhs|lac|lpa|crore|crores|cr|k)?"

    match = re.search(pattern, text)

    if match:
        amount = Decimal(match.group(1))
        unit = match.group(2)

        if unit in ("lakh", "lakhs", "lac", "lpa"):
            amount *= Decimal("100000")
        elif unit in ("crore", "crores", "cr"):
            amount *= Decimal("10000000")
        elif unit == "k":
            amount *= Decimal("1000")
        elif "₹" in text or "rs" in text:
            pass
        else:
            amount = None

        result["gross_salary"] = amount

    if (
        "new regime" in text
        or "new tax regime" in text
        or "new tax system" in text
    ):
        result["regime"] = "new_regime"

    elif (
        "old regime" in text
        or "old tax regime" in text
        or "old tax system" in text
    ):
        result["regime"] = "old_regime"

    missing = []

    if result["gross_salary"] is None:
        missing.append("annual gross salary with unit (for example, 12 lakh)")

    if result["regime"] is None:
        missing.append("tax regime (old or new)")

    if missing:
        return {
            "status": "needs_clarification",
            "missing": missing,
            "message": "Please provide your " + " and ".join(missing) + "."
        }

    if result["gross_salary"] <= 0:
        return {
            "status": "needs_clarification",
            "missing": ["valid positive annual salary"],
            "message": "Please provide a positive annual salary."
        }

    return {
        "status": "success",
        "gross_salary": result["gross_salary"],
        "regime": result["regime"]
    }
