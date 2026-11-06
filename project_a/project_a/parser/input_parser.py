import re


def parse_salary_input(user_input):
    text = user_input.lower()

    result = {
        "gross_salary": None,
        "regime": None,
        "missing_fields": []
    }

    # Extract salary
    salary_pattern = (
        r"(?:annual\s+salary|salary|income|earning|₹|rs\.?)"
        r"\s*(?:is|of|:)?\s*₹?\s*"
        r"([\d,]+(?:\.\d+)?)\s*"
        r"(lakhs?|lacs?|l|crores?|cr)?"
    )

    match = re.search(salary_pattern, text)

    if match:
        amount = float(match.group(1).replace(",", ""))
        unit = match.group(2)

        if unit in ("lakh", "lakhs", "lac", "lacs", "l"):
            amount *= 100000
        elif unit in ("crore", "crores", "cr"):
            amount *= 10000000

        result["gross_salary"] = int(amount)

    # Extract tax regime
    if "new regime" in text:
        result["regime"] = "new_regime"
    elif "old regime" in text:
        result["regime"] = "old_regime"

    # Identify missing information
    if result["gross_salary"] is None:
        result["missing_fields"].append("annual salary")

    if result["regime"] is None:
        result["missing_fields"].append("tax regime")

    return result