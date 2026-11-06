
import json
from pathlib import Path

from project_a.llm_query.llm_client import ask_llm

PROJECT_ROOT = Path(__file__).resolve().parents[2]
COMPILED_FILE = PROJECT_ROOT / "data" / "compiled_tax_rules.json"


def run_compiled_query(user_query):
    if not COMPILED_FILE.exists():
        raise FileNotFoundError(
            "Compiled tax rules not found. Run compile_rules.py first."
        )

    with open(COMPILED_FILE, "r", encoding="utf-8") as file:
        compiled_rules = json.load(file)

    prompt = f"""
You are an Indian income tax assistant.

Use these previously compiled tax rules:

{json.dumps(compiled_rules, indent=2)}

User question:
{user_query}

Instructions:
1. Identify salary and tax regime.
2. Ask for clarification if information is missing.
3. Use only the supplied rules.
4. Do not invent tax provisions or deductions.
5. Explain calculations step by step.
6. Clearly mention when information is insufficient.
"""

    return ask_llm(prompt)


if __name__ == "__main__":
    query = input("Enter your tax question: ")
    result = run_compiled_query(query)

    print("\n===== COMPILED-RULES RESPONSE =====")
    print(result)
