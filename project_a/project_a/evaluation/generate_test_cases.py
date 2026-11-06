
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_FILE = PROJECT_ROOT / "data" / "test_cases.json"

salaries = [
    300000, 400000, 500000, 600000, 700000,
    800000, 900000, 1000000, 1200000, 1500000,
    1800000, 2000000, 2500000, 3000000, 4000000,
    5000000, 6000000, 7500000, 10000000, 15000000
]

regimes = ["old_regime", "new_regime"]

deduction_scenarios = [
    {
        "section_80c": 0,
        "section_80ccd_1b": 0,
        "health_self": 0,
        "health_parents": 0,
        "home_loan_interest": 0
    },
    {
        "section_80c": 50000,
        "section_80ccd_1b": 0,
        "health_self": 0,
        "health_parents": 0,
        "home_loan_interest": 0
    },
    {
        "section_80c": 100000,
        "section_80ccd_1b": 25000,
        "health_self": 15000,
        "health_parents": 20000,
        "home_loan_interest": 100000
    },
    {
        "section_80c": 150000,
        "section_80ccd_1b": 50000,
        "health_self": 25000,
        "health_parents": 25000,
        "home_loan_interest": 200000
    },
    {
        "section_80c": 0,
        "section_80ccd_1b": 0,
        "health_self": 0,
        "health_parents": 0,
        "home_loan_interest": 0
    }
]

test_cases = []
case_id = 1

for salary in salaries:
    for regime in regimes:
        for scenario_index, deductions in enumerate(deduction_scenarios):
            test_cases.append({
                "case_id": case_id,
                "gross_salary": salary,
                "regime": regime,
                "is_resident": scenario_index != 4,
                "deductions": deductions,
                "expected_tax": None,
                "officially_verified": False
            })
            case_id += 1

with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
    json.dump(test_cases, file, indent=2)

print(f"Generated {len(test_cases)} test cases.")
print(f"Saved to: {OUTPUT_FILE}")
