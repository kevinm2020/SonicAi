from fastapi import FastAPI
from pydantic import BaseModel
from agent import SonicAgent

# Initialize FastAPI app
app = FastAPI(title="Sonic AI API")

# Request payload schema
class SongRequest(BaseModel):
    song: str
    artist: str

# Minimal SonicAgent placeholder (importable)
agent = SonicAgent()

@app.post("/analyze")
async def analyze_song(request: SongRequest):
    try:
        # Call your SonicAgent (replace with your real logic)
        result = agent.analyze(request.song, request.artist)
        return result
    except Exception as e:
        return {"error": str(e)}