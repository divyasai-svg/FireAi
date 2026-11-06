
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_FILE = DATA_DIR / "comparison_results.json"


def load_json(filename):
    file_path = DATA_DIR / filename

    if not file_path.exists():
        return []

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def compare_approaches():
    rules_results = load_json("rules_results.json")
    parser_results = load_json("parser_results.json")

    rules_success = sum(
        1 for item in rules_results
        if item.get("status") == "success"
    )

    parser_correct = sum(
        1 for item in parser_results
        if item.get("passed") is True
    )

    comparison = {
        "rules_based": {
            "total_cases": len(rules_results),
            "successful_cases": rules_success,
            "success_rate": (
                round(rules_success / len(rules_results) * 100, 2)
                if rules_results else None
            )
        },
        "llm_query_time": {
            "status": "Pending Gemini evaluation",
            "accuracy": None,
            "latency_seconds": None,
            "cost": None
        },
        "llm_compiled_rules": {
            "status": "Pending Gemini evaluation",
            "accuracy": None,
            "latency_seconds": None,
            "cost": None
        },
        "parser": {
            "total_cases": len(parser_results),
            "correct_cases": parser_correct,
            "accuracy": (
                round(parser_correct / len(parser_results) * 100, 2)
                if parser_results else None
            )
        }
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(comparison, file, indent=2)

    print(json.dumps(comparison, indent=2))
    print(f"Saved comparison to: {OUTPUT_FILE}")

    return comparison


if __name__ == "__main__":
    compare_approaches()
