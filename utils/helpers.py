def clean_song_name(song_name: str) -> str:
    return song_name.strip().lower()

def safe_get(d, key, default=None):
    return d.get(key, default) if isinstance(d, dict) else default

def format_for_llm(data: dict) -> str:
    features = data.get("features", {})
    metadata = data.get("metadata", {})
    spotify = features.get("spotify", {})
    acoustic = features.get("acoustic", {})  # ✅ FIX: pull acoustic as its own dict

    # ✅ FIX: read tempo/energy/danceability from acoustic, not top-level features
    tempo = acoustic.get("tempo", "Unknown")
    energy = acoustic.get("energy", "Unknown")
    danceability = acoustic.get("danceability", "Unknown")
    valence = acoustic.get("valence", "Unknown")

    album = spotify.get("album") or metadata.get("album", "Unknown")

    duration_ms = spotify.get("duration_ms")
    duration_sec = round(duration_ms / 1000, 1) if duration_ms else "Unknown"

    popularity = spotify.get("popularity", "Unknown")
    explicit = "Yes" if spotify.get("explicit") else "No"

    # ✅ FIX: safely handle chords — data["chords"] could be None or a dict
    chords_data = data.get("chords") or {}
    chords = chords_data.get("chords", []) if isinstance(chords_data, dict) else []

    return f"""
    Song: {metadata.get('title', 'Unknown')}
    Artist: {metadata.get('artist', 'Unknown')}
    Album: {album}
    Release Date: {metadata.get('release_date', 'Unknown')}

    Duration: {duration_sec} seconds
    Explicit: {explicit}
    Popularity (Spotify): {popularity}/100

    Tempo: {tempo} BPM
    Energy: {energy}
    Danceability: {danceability}
    Valence: {valence}

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