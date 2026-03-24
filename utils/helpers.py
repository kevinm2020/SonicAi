def clean_song_name(song_name: str ) -> str:
    return song_name.strip().lower()

def safe_get(d, key, default=None):
    return d.get(key, default) if isinstance(d, dict) else default

def format_for_llm(data: dict) -> str:
    features = data.get("features", {})
    metadata = data.get("metadata", {})
    spotify = features.get("spotify", {})  
    chords = data.get("chords", {}).get("chords", [])

    album = spotify.get("album") or metadata.get("album")  

    duration_ms = spotify.get("duration_ms")
    duration_sec = round(duration_ms / 1000, 1) if duration_ms else "Unknown"

    return f"""
    Song: {metadata.get('title', 'Unknown')}
    Artist: {metadata.get('artist', 'Unknown')}
    Album: {album or 'Unknown'}

    Tempo: {features.get('tempo', 'Unknown')} BPM
    Energy: {features.get('energy', 'Unknown')}
    Danceability: {features.get('danceability', 'Unknown')}

    Duration: {duration_sec} seconds
    Explicit: {"Yes" if spotify.get("explicit") else "No"}

    Chords: {', '.join(chords) if chords else 'Unknown'}
    """

def debug_log(label, data):
    print(f"\n[DEBUG] {label}:")
    print(data)

def validate_metadata(metadata):
    return metadata is not None and "title" in metadata

def load_prompt(file_path: str) -> str:
    with open(file_path, "r") as f:
        return f.read()