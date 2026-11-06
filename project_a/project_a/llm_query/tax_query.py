from project_a.llm_query.llm_client import ask_llm
from project_a.llm_query.tax_prompt import build_tax_prompt


def run_tax_query(user_query):

    prompt = build_tax_prompt(user_query)

    response = ask_llm(prompt)

    return response


if __name__ == "__main__":

    query = input("Enter your tax question: ")

    result = run_tax_query(query)

    print("\n===== LLM TAX RESPONSE =====")
    print(result)