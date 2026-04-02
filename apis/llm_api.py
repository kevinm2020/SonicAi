from openai import OpenAI
import os
import json

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
You are a music analysis engine.

Given song metadata and audio features, generate a structured musical analysis.

Return your response in clean markdown format using the following sections:

## Tempo & Energy
## Danceability & Mood
## Harmony
## Overall Character

Guidelines:
- Base your analysis ONLY on the provided data.
- If something is unknown, state it briefly.
- Be concise but insightful.
- Do NOT return JSON.
- Do NOT include code blocks.
- Do NOT include metadata.
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
        return content

    except Exception as e:
        print("LLM error:", e)
        return "Error generating analysis."
    
#challenges
#AcosticBrains was shut down in 2022, so we need to handle that gracefully.
#update frontend
#have to change prompt and temparture