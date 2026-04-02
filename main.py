from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent import SonicAgent

app = FastAPI(title="Sonic AI API")
agent = SonicAgent()

print("🎧 Sonic AI Local Test\n")

song = input("Enter song name: ")
artist = input("Enter artist name: ")

print("\nAnalyzing...\n")

result = agent.analyze(song, artist)

print("\n===== RESULT =====\n")
print(result)

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


@app.post("/analyze")
async def analyze_song(request: SongRequest):
    try:
        result = agent.analyze(request.song, request.artist)

        # If agent fails and returns a string error
        if isinstance(result, str):
            return {
                "metadata": {
                    "title": request.song,
                    "artist": request.artist,
                    "album": "Unknown"
                },
                "features": {
                    "spotify": {}
                },
                "chords": {
                    "chords": []
                },
                "analysis": result
            }

        return result

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
        "agent_loaded": True
    }


