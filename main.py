from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent import SonicAgent

app = FastAPI(title="Sonic AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "https://kevin-martinez-portfolio-frontend.onrender.com",
    "http://localhost:5173"
    ],
    
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
        return {
            "metadata": {
                "title": request.song,
                "artist": request.artist,
                "album": "...",  # extract from result
            },
            "features": {
                "duration": None,
                "explicit": None,
            },
            "chords": [],
            "mode": None,
            "analysis": result  # the raw string for now
        }
    except Exception as e:
        return {"error": str(e)}
    
@app.get("/ping")
async def ping():
    return {"status": "ok"}

@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "service": "sonic-ai",
        "agent_loaded": agent is not None
    }