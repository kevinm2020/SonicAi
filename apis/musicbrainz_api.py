import requests

BASE_URL = "https://musicbrainz.org/ws/2/recording/"

HEADERS = {
    "User-Agent": "SonicAI/1.0 (kevinm2020@icloud.com)"
}



def get_song_metadata(song_name, artist_name=None):
    """
    Fetch song metadata from MusicBrainz.
    Returns a clean dictionary with key fields.
    """
    query = f"{song_name} {artist_name}" if artist_name else song_name

    params = {
        "query": f'recording:"{song_name}" AND artist:"{artist_name}"',
        "fmt": "json",
        "limit": 1
    }

    try:

        response = requests.get(
            BASE_URL,
            params=params,
            headers=HEADERS,
            verify=False  
        )
        data = response.json()

        if "recordings" not in data or len(data["recordings"]) == 0:
            return None

        recording = data["recordings"][0]

        # Safe extraction
        title = recording.get("title", "Unknown")

        artist = "Unknown"
        if "artist-credit" in recording and len(recording["artist-credit"]) > 0:
            artist = recording["artist-credit"][0].get("name", "Unknown")

        album = "Unknown"
        if "releases" in recording and len(recording["releases"]) > 0:
            album = recording["releases"][0].get("title", "Unknown")

        release_date = recording.get("first-release-date", "Unknown")

        mbid = recording.get("id", None)

        return {
            "id": mbid,
            "title": title,
            "artist": artist,
            "album": album,
            "release_date": release_date
        }
    

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] MusicBrainz API request failed: {e}")
        return None



#Music Brainz is a database we can hit with just GET requests
#Music Brainz is used for the factual release infromation about
# a song.