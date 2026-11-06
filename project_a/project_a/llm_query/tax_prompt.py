import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

RULES_FILE = PROJECT_ROOT / "data" / "tax_rules_2024_25.json"


def build_tax_prompt(user_query):

    with open(RULES_FILE, "r", encoding="utf-8") as file:
        tax_rules = json.load(file)

    prompt = f"""
You are an Indian income tax assistant.

The financial year is FY 2024-25.
Assessment year is AY 2025-26.

Use the following tax rules provided to you:

{json.dumps(tax_rules, indent=2)}

User question:
{user_query}

Instructions:
1. Identify the user's salary and selected tax regime.
2. Ask for clarification if required information is missing.
3. Use only the supplied tax rules for slab calculations.
4. Do not invent tax provisions or deductions.
5. Explain your calculation step by step.
6. Clearly mention if information is insufficient.
7. Return the answer in a structured and understandable format.
"""

    return prompt