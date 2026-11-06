
import json
import time
from pathlib import Path

from project_a.llm_query.tax_query import run_tax_query
from project_a.llm_compiled.compiled_query import run_compiled_query

PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = PROJECT_ROOT / "data" / "natural_language_cases.json"
OUTPUT_FILE = PROJECT_ROOT / "data" / "llm_evaluation_results.json"


def evaluate_llm():
    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        cases = json.load(file)

    selected_cases = cases[:10]

    results = {
        "llm_query_time": [],
        "llm_compiled_rules": []
    }

    approaches = [
        ("llm_query_time", run_tax_query),
        ("llm_compiled_rules", run_compiled_query)
    ]

    total_calls = 0

    for approach_name, run_function in approaches:
        print(f"\nEvaluating {approach_name}...")

        for case in selected_cases:

            if total_calls > 0 and total_calls % 5 == 0:
                print("\nWaiting 65 seconds to respect Gemini API quota...")
                time.sleep(65)

            total_calls += 1
            query = case["query"]

            print(f"Running case {case['case_id']}...")

            start_time = time.perf_counter()

            try:
                response = run_function(query)
                elapsed_time = time.perf_counter() - start_time

                results[approach_name].append({
                    "case_id": case["case_id"],
                    "query": query,
                    "response": response,
                    "latency_seconds": round(elapsed_time, 3),
                    "status": "success"
                })

            except Exception as error:
                elapsed_time = time.perf_counter() - start_time

                results[approach_name].append({
                    "case_id": case["case_id"],
                    "query": query,
                    "error": str(error),
                    "latency_seconds": round(elapsed_time, 3),
                    "status": "error"
                })

    for approach_name in ["llm_query_time", "llm_compiled_rules"]:
        successful = [
            item for item in results[approach_name]
            if item["status"] == "success"
        ]

        average_latency = (
            sum(item["latency_seconds"] for item in successful)
            / len(successful)
            if successful else 0
        )

        results[approach_name + "_summary"] = {
            "total_cases": len(results[approach_name]),
            "successful_cases": len(successful),
            "failed_cases": len(results[approach_name]) - len(successful),
            "average_latency_seconds": round(average_latency, 3)
        }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(results, file, indent=2)

    print("\n===== LLM EVALUATION SUMMARY =====")

    for approach_name in ["llm_query_time", "llm_compiled_rules"]:
        print(f"\n{approach_name}:")
        print(json.dumps(results[approach_name + "_summary"], indent=2))

    print(f"\nResults saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    evaluate_llm()
