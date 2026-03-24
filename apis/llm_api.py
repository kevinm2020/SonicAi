from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_with_llm(prompt: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a music intelligence engine. Analyze songs based on metadata, chords, and structure."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7
        )

        return response.choices[0].message.content

    except Exception as e:
        print("OpenAI request failed:", e)
        return "--- Sonic AI Analysis (Fallback) ---\nLLM failed"