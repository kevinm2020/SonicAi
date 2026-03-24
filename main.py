from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent import SonicAgent

app = FastAPI(title="Sonic AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://kevin-martinez-portfolio-frontend.onrender.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SongRequest(BaseModel):
    song: str
    artist: str

agent = SonicAgent()

@app.post("/analyze")
async def analyze_song(request: SongRequest):
    try:
        result = agent.analyze(request.song, request.artist)
        return result
    except Exception as e:
        return {"error": str(e)}