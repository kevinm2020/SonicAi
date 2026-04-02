from openai import OpenAI
import os
import json

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
You are a music analysis engine.

Given song metadata and audio features, generate a structured analysis.

Return ONLY valid JSON with this structure:

{
  "analysis": {
    "tempo_energy": "",
    "danceability_mood": "",
    "harmony": "",
    "overall_character": ""
  }
}

Rules:
- Use ONLY the provided data.
- If something is unknown, say so briefly.
- Do NOT include metadata in your response.
- Do NOT include any text outside JSON.
"""


def analyze_with_llm(features: dict) -> dict:
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": json.dumps(features)}
            ],
            temperature=0.3
        )

        content = response.choices[0].message.content
        return json.loads(content)

    except Exception as e:
        print("LLM error:", e)
        return {
            "analysis": {
                "tempo_energy": "N/A",
                "danceability_mood": "N/A",
                "harmony": "N/A",
                "overall_character": "N/A"
            }
        }
    
#challenges
#AcosticBrains was shut down in 2022, so we need to handle that gracefully.
#update frontend
#have to change prompt and temparture