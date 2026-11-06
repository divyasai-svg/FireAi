
from project_a.llm_query.llm_client import client

print("Checking available Gemini models...\n")

for model in client.models.list():
    actions = model.supported_actions or []

    if "generateContent" in actions:
        print(model.name)
