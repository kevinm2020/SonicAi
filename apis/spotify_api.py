import os
import json
import requests
from urllib.parse import urlencode
from flask import Flask, request
from utils.helpers import debug_log
import base64

# --------------------
# CONFIG
# --------------------
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI", "http://127.0.0.1:8888/callback")
TOKEN_FILE = ".spotify_token.json"

SCOPES = "user-read-private user-read-email"

app = Flask(__name__)

# --------------------
# AUTH HELPER FUNCTIONS
# --------------------

_token_cache = None

def get_access_token():
    global _token_cache

    if _token_cache:
        return _token_cache

    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

    if not client_id or not client_secret:
        raise Exception("Missing Spotify credentials")

    auth_str = f"{client_id}:{client_secret}"
    auth_base64 = base64.b64encode(auth_str.encode()).decode()

    url = "https://accounts.spotify.com/api/token"

    headers = {
        "Authorization": f"Basic {auth_base64}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type": "client_credentials"
    }

    response = requests.post(url, headers=headers, data=data)

    print("TOKEN STATUS:", response.status_code)
    print("TOKEN RESPONSE:", response.text[:200])

    response.raise_for_status()

    _token_cache = response.json()["access_token"]
    return _token_cache

def save_tokens(tokens: dict):
    with open(TOKEN_FILE, "w") as f:
        json.dump(tokens, f)

def load_tokens():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as f:
            return json.load(f)
    return {}

def get_auth_url():
    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPES,
    }
    return f"https://accounts.spotify.com/authorize?{urlencode(params)}"

def exchange_code_for_token(code):
    url = "https://accounts.spotify.com/api/token"
    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    response = requests.post(url, data=payload)
    response.raise_for_status()
    tokens = response.json()
    save_tokens(tokens)
    return tokens

def refresh_access_token():
    tokens = load_tokens()
    if "refresh_token" not in tokens:
        raise Exception("No refresh token available. Re-authorize.")
    payload = {
        "grant_type": "refresh_token",
        "refresh_token": tokens["refresh_token"],
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    response = requests.post("https://accounts.spotify.com/api/token", data=payload)
    response.raise_for_status()
    new_tokens = response.json()
    tokens["access_token"] = new_tokens["access_token"]
    save_tokens(tokens)
    return tokens["access_token"]

def get_valid_token():
    tokens = load_tokens()
    if not tokens or "access_token" not in tokens:
        print("Open this URL in your browser and log in:", get_auth_url())
        app.run(port=8888)
        tokens = load_tokens()
    return tokens.get("access_token") or refresh_access_token()

# --------------------
# FLASK CALLBACK
# --------------------
@app.route("/callback")
def callback():
    code = request.args.get("code")
    exchange_code_for_token(code)
    return "Authorization code received! You can close this window."

# --------------------
# SPOTIFY API FUNCTIONS
# --------------------
def search_track(song_name, artist_name):
    token = get_access_token()

    url = "https://api.spotify.com/v1/search"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    params = {
        "q": f"track:{song_name} artist:{artist_name}",
        "type": "track",
        "limit": 1
    }

    response = requests.get(url, headers=headers, params=params)

    print("DEBUG STATUS:", response.status_code)
    print("DEBUG RESPONSE:", response.text[:200])

    response.raise_for_status()

    data = response.json()

    items = data.get("tracks", {}).get("items", [])
    if not items:
        return None

    return items[0]

def get_audio_features(track_id):
    token = get_access_token()

    headers = {
        "Authorization": f"Bearer {token}"
    }

    url = f"https://api.spotify.com/v1/audio-features/{track_id}"

    response = requests.get(url, headers=headers)

    print("DEBUG AUDIO STATUS:", response.status_code)
    print("DEBUG AUDIO RESPONSE:", response.text[:200])

    if response.status_code != 200:
        return None

    return response.json()

def get_spotify_features(song_name, artist_name):
    track = search_track(song_name, artist_name)
    if not track:
        return {}

    track_id = track.get("id")

    # Base track metadata
    features = {
        "popularity": track.get("popularity"),
        "duration_ms": track.get("duration_ms"),
        "explicit": track.get("explicit"),
        "album": track.get("album", {}).get("name")
    }

    # Merge audio features from Spotify 
    audio = get_audio_features(track_id) or {}
    features["tempo"] = audio.get("tempo")
    features["energy"] = audio.get("energy")
    features["danceability"] = audio.get("danceability")
    features["valence"] = audio.get("valence")
    features["mode"] = "Major" if audio.get("mode") == 1 else "Minor"
    features["key"] = audio.get("key")
    features["loudness"] = audio.get("loudness")
    features["speechiness"] = audio.get("speechiness")
    features["acousticness"] = audio.get("acousticness")
    features["instrumentalness"] = audio.get("instrumentalness")
    features["liveness"] = audio.get("liveness")
    features["time_signature"] = audio.get("time_signature")

    debug_log("Spotify Features", features)
    return features