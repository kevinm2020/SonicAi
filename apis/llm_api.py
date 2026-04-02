from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """You are a music intelligence engine that produces structured, data-driven song analyses.

You will be given real metadata and audio features for a song. Your job is to:
1. Report ONLY what the data actually says — never guess or fabricate values that are marked Unknown.
2. Interpret the numbers meaningfully (e.g. explain what a danceability of 0.85 implies, or what a high energy reading means in context).
3. Structure your response clearly using these sections:
   - Metadata Summary
   - Tempo & Energy
   - Danceability & Mood
   - Chord Progression & Harmonic Character
   - Overall Character & Use Cases

If a field is Unknown, say so briefly and move on — do NOT invent a plausible-sounding substitute.
Be specific, concise, and insightful. Avoid generic filler like "pop songs often..." unless it directly applies."""

def analyze_with_llm(prompt: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.4  # lower = more factual, less hallucination
        )

        return response.choices[0].message.content

    except Exception as e:
        print("OpenAI request failed:", e)
        return "--- Sonic AI Analysis (Fallback) ---\nLLM failed"
    
#challenges
#AcosticBrains was shut down in 2022, so we need to handle that gracefully.
#update frontend
#have to change prompt and temparture