from project_a.parser.nl_parser import parse_tax_query
from project_a.rules_engine.tax_calculator import calculate_salary_tax


def process_tax_query(text, is_resident=None):

    parsed = parse_tax_query(text)

    if parsed["status"] != "success":
        return parsed

    if is_resident is None:
        return {
            "status": "needs_clarification",
            "missing": ["residential status"],
            "message": "Are you a resident of India for tax purposes?"
        }

    result = calculate_salary_tax(
        gross_salary=parsed["gross_salary"],
        regime=parsed["regime"],
        data={"is_resident": is_resident}
    )

    return {
        "status": "success",
        "tax_result": result
    }