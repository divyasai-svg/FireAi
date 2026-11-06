from project_a.llm_query.llm_client import ask_llm

response = ask_llm(
    "Explain the purpose of income tax in India in two sentences."
)

print(response)