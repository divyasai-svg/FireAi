
import json
from pathlib import Path

from project_a.rules_engine.tax_calculator import calculate_salary_tax

PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = PROJECT_ROOT / "data" / "test_cases.json"
OUTPUT_FILE = PROJECT_ROOT / "data" / "rules_results.json"


def evaluate_rules_cases():
    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        test_cases = json.load(file)

    results = []

    for case in test_cases:
        data = {
            "is_resident": case["is_resident"],
            **case["deductions"]
        }

        try:
            tax_result = calculate_salary_tax(
                gross_salary=case["gross_salary"],
                regime=case["regime"],
                data=data
            )

            results.append({
                "case_id": case["case_id"],
                "gross_salary": case["gross_salary"],
                "regime": case["regime"],
                "status": "success",
                "result": tax_result
            })

        except Exception as error:
            results.append({
                "case_id": case["case_id"],
                "gross_salary": case["gross_salary"],
                "regime": case["regime"],
                "status": "error",
                "error": str(error)
            })

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(results, file, indent=2, default=str)

    successful = sum(
        1 for result in results
        if result["status"] == "success"
    )

    print(f"Total cases: {len(results)}")
    print(f"Successful: {successful}")
    print(f"Failed: {len(results) - successful}")
    print(f"Results saved to: {OUTPUT_FILE}")

    return results


if __name__ == "__main__":
    evaluate_rules_cases()
