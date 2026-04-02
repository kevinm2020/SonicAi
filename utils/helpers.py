KEY_MAP = {
    0: "C", 1: "C#", 2: "D", 3: "D#", 4: "E", 5: "F",
    6: "F#", 7: "G", 8: "G#", 9: "A", 10: "A#", 11: "B"
}

def clean_song_name(song_name: str) -> str:
    return song_name.strip().lower()

def safe_get(d, key, default=None):
    return d.get(key, default) if isinstance(d, dict) else default

def format_for_llm(data: dict) -> str:
    features = data.get("features", {})
    metadata = data.get("metadata", {})
    spotify = features.get("spotify", {})
    acoustic = features.get("acoustic", {})

    # Acoustic / audio features (now sourced from Spotify)
    tempo = acoustic.get("tempo", "Unknown")
    energy = acoustic.get("energy", "Unknown")
    danceability = acoustic.get("danceability", "Unknown")
    valence = acoustic.get("valence", "Unknown")
    mode = acoustic.get("mode", "Unknown")
    loudness = acoustic.get("loudness", "Unknown")
    speechiness = acoustic.get("speechiness", "Unknown")
    acousticness = acoustic.get("acousticness", "Unknown")
    instrumentalness = acoustic.get("instrumentalness", "Unknown")
    liveness = acoustic.get("liveness", "Unknown")
    time_signature = acoustic.get("time_signature", "Unknown")

    # Key: convert integer to note name
    key_num = acoustic.get("key")
    key_name = KEY_MAP.get(key_num, "Unknown") if key_num is not None else "Unknown"

    # Track metadata
    album = spotify.get("album") or metadata.get("album", "Unknown")
    duration_ms = spotify.get("duration_ms")
    duration_sec = round(duration_ms / 1000, 1) if duration_ms else "Unknown"
    popularity = spotify.get("popularity", "Unknown")
    explicit = "Yes" if spotify.get("explicit") else "No"

    # Chords — safely handle None or missing
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
Key: {key_name} {mode}
Time Signature: {time_signature}/4
Loudness: {loudness} dB

Energy: {energy}
Danceability: {danceability}
Valence: {valence}
Speechiness: {speechiness}
Acousticness: {acousticness}
Instrumentalness: {instrumentalness}
Liveness: {liveness}

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