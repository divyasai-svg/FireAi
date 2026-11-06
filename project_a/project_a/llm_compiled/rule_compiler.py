
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RULES_FILE = PROJECT_ROOT / "data" / "tax_rules_2024_25.json"
COMPILED_FILE = PROJECT_ROOT / "data" / "compiled_tax_rules.json"



def build_compilation_prompt():
    with open(RULES_FILE, "r", encoding="utf-8") as file:
        tax_rules = json.load(file)

    prompt = f"""
You are an Indian income tax rules compiler.

The applicable financial year is FY 2024-25.
The assessment year is AY 2025-26.

Convert the supplied tax rules into a structured JSON object.

Tax rules:
{json.dumps(tax_rules, indent=2)}

Instructions:
1. Preserve all tax slabs and standard deductions exactly.
2. Include the financial year and assessment year.
3. Keep old and new regimes separate.
4. Do not invent missing tax provisions.
5. Return valid JSON only.
6. Do not include Markdown code fences or explanations.
"""
    return prompt


def save_compiled_rules(response_text):
    cleaned_response = response_text.strip()

    if cleaned_response.startswith("```"):
        cleaned_response = cleaned_response.replace("```json", "", 1)
        cleaned_response = cleaned_response.replace("```", "").strip()

    compiled_rules = json.loads(cleaned_response)

    with open(COMPILED_FILE, "w", encoding="utf-8") as file:
        json.dump(compiled_rules, file, indent=2)

    return compiled_rules
