from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from apis.spotify_api import get_spotify_features
from agent import analyze_with_llm

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


@app.post("/analyze")
async def analyze_song(request: SongRequest):
    try:
        # Step 1: Get Spotify features
        features = get_spotify_features(request.song, request.artist)

        # Step 2: Run LLM analysis (expects dict → returns string)
        analysis_text = analyze_with_llm(features)

        # Step 3: Build response matching frontend expectations
        return {
            "metadata": {
                "title": features.get("title"),
                "artist": features.get("artist"),
                "album": features.get("album"),
                "release_date": features.get("release_date"),
            },
            "features": {
                "spotify": {
                    "duration_ms": features.get("duration_ms"),
                    "explicit": features.get("explicit"),
                    "popularity": features.get("popularity"),
                    "tempo": features.get("tempo"),
                    "energy": features.get("energy"),
                    "danceability": features.get("danceability"),
                    "valence": features.get("valence"),
                    "mode": features.get("mode"),
                    "key": features.get("key"),
                    "loudness": features.get("loudness"),
                    "speechiness": features.get("speechiness"),
                    "acousticness": features.get("acousticness"),
                    "instrumentalness": features.get("instrumentalness"),
                    "liveness": features.get("liveness"),
                    "time_signature": features.get("time_signature"),
                }
            },
            "chords": {
                "chords": features.get("chords", [])
            },
            "analysis": analysis_text
        }

    except Exception as e:
        return {
            "error": str(e)
        }


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