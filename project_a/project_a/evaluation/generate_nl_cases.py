
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_FILE = PROJECT_ROOT / "data" / "natural_language_cases.json"

templates = [
    "Calculate my income tax for a salary of {salary} under the {regime} regime.",
    "My annual salary is {salary}. How much tax should I pay under the {regime} regime?",
    "I earn {salary} per year. Find my income tax using the {regime} regime.",
    "What will be my tax liability if my salary is {salary} under the {regime} regime?",
    "Please calculate tax on my yearly income of {salary} using the {regime} tax system."
]

salaries = ["5 lakh", "7 lakh", "10 lakh", "12 lakh", "15 lakh"]
regimes = ["old", "new"]

cases = []
case_id = 1

for salary in salaries:
    for regime in regimes:
        for template in templates:
            cases.append({
                "case_id": case_id,
                "query": template.format(
                    salary=salary,
                    regime=regime
                ),
                "expected_salary": salary,
                "expected_regime": regime
            })
            case_id += 1

with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
    json.dump(cases, file, indent=2)

print(f"Generated {len(cases)} natural-language cases.")
print(f"Saved to: {OUTPUT_FILE}")
