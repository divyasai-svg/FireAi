
from project_a.llm_query.llm_client import ask_llm
from project_a.llm_compiled.rule_compiler import (
    build_compilation_prompt,
    save_compiled_rules
)


def compile_tax_rules():
    prompt = build_compilation_prompt()

    print("Compiling tax rules using Gemini...")

    response = ask_llm(prompt)

    compiled_rules = save_compiled_rules(response)

    print("Tax rules compiled and saved successfully!")

    return compiled_rules


if __name__ == "__main__":
    compile_tax_rules()
