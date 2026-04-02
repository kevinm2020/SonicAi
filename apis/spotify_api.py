import os
import requests
import base64

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

_token_cache = None


def get_access_token():
    global _token_cache

    if _token_cache:
        return _token_cache

    auth_str = f"{CLIENT_ID}:{CLIENT_SECRET}"
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
    response.raise_for_status()

    _token_cache = response.json()["access_token"]
    return _token_cache


def search_track(song_name, artist_name):
    token = get_access_token()

    url = "https://api.spotify.com/v1/search"
    headers = {"Authorization": f"Bearer {token}"}

    # Improved query (more reliable)
    params = {
        "q": f"{song_name} {artist_name}",
        "type": "track",
        "limit": 1
    }

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()

    items = response.json().get("tracks", {}).get("items", [])
    if not items:
        return None

    return items[0]


def get_audio_features(track_id):
    token = get_access_token()

    url = f"https://api.spotify.com/v1/audio-features/{track_id}"
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("❌ Audio features failed:", response.text)
        return None

    return response.json()


def get_spotify_features(song_name, artist_name):
    track = search_track(song_name, artist_name)

    if not track:
        print("❌ No track found")
        return {}

    track_id = track.get("id")

    # Base metadata
    features = {
        "title": track.get("name"),
        "artist": ", ".join([a["name"] for a in track.get("artists", [])]),
        "album": track.get("album", {}).get("name"),
        "duration_ms": track.get("duration_ms"),
        "explicit": track.get("explicit"),
        "popularity": track.get("popularity"),
    }

    if not track_id:
        print("❌ Missing track ID")
        return features

    audio = get_audio_features(track_id)

    if audio:
        features.update({
            "tempo": audio.get("tempo"),
            "energy": audio.get("energy"),
            "danceability": audio.get("danceability"),
            "valence": audio.get("valence"),
            "mode": "Major" if audio.get("mode") == 1 else "Minor",
            "key": audio.get("key"),
            "loudness": audio.get("loudness"),
            "speechiness": audio.get("speechiness"),
            "acousticness": audio.get("acousticness"),
            "instrumentalness": audio.get("instrumentalness"),
            "liveness": audio.get("liveness"),
            "time_signature": audio.get("time_signature"),
        })

    return features