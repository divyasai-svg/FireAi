
import json
from pathlib import Path
from decimal import Decimal

from project_a.parser.nl_parser import parse_tax_query

PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = PROJECT_ROOT / "data" / "natural_language_cases.json"
OUTPUT_FILE = PROJECT_ROOT / "data" / "parser_results.json"


def convert_salary(value):
    number, unit = value.split()
    return Decimal(number) * Decimal("100000")


def evaluate_parser():
    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        cases = json.load(file)

    results = []
    correct = 0

    for case in cases:
        parsed = parse_tax_query(case["query"])

        expected_salary = convert_salary(case["expected_salary"])
        expected_regime = case["expected_regime"] + "_regime"

        salary_correct = (
            parsed.get("gross_salary") == expected_salary
        )

        regime_correct = (
            parsed.get("regime") == expected_regime
        )

        passed = (
            parsed.get("status") == "success"
            and salary_correct
            and regime_correct
        )

        if passed:
            correct += 1

        results.append({
            "case_id": case["case_id"],
            "query": case["query"],
            "parsed_result": parsed,
            "passed": passed
        })

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(results, file, indent=2, default=str)

    accuracy = correct / len(cases) * 100

    print(f"Total queries: {len(cases)}")
    print(f"Correctly parsed: {correct}")
    print(f"Parser accuracy: {accuracy:.2f}%")
    print(f"Results saved to: {OUTPUT_FILE}")

    return results


if __name__ == "__main__":
    evaluate_parser()
