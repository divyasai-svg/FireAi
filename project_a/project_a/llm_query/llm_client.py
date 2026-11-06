import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv(override=True)

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")

print("GEMINI MODEL BEING USED:", MODEL)

if not API_KEY:
    raise ValueError("GEMINI_API_KEY is missing from .env")

client = genai.Client(
    api_key=API_KEY,
    http_options=types.HttpOptions(
        timeout=120000
    )
)

def ask_llm(prompt):
    print("Connecting to Gemini...")

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=prompt
            )
            return response.text

        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")

            if attempt == 2:
                raise

            wait_time = 10 * (2 ** attempt)
            print(f"Retrying after {wait_time} seconds...")
            time.sleep(wait_time)