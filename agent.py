from apis.musicbrainz_api import get_song_metadata
from apis.spotify_api import get_spotify_features
from apis.chords_api import get_chords
from apis.llm_api import analyze_with_llm
from utils.helpers import format_for_llm, debug_log

class SonicAgent:
    def analyze(self, song_name, artist_name):
        # Step 1: MusicBrainz metadata
        metadata = get_song_metadata(song_name, artist_name)
        if metadata is None:
            debug_log("Error", "MusicBrainz metadata not found")
            return "❌ Song not found or API error. Try a different input."

        # Step 2: Spotify features (includes acoustic data — replaces AcousticBrainz)
        spotify_features = get_spotify_features(song_name, artist_name)
        if spotify_features is None:
            spotify_features = {}

        debug_log("Spotify Features", spotify_features)

        # Step 3: Chords
        chords = get_chords(metadata)
        if chords is None:
            chords = {"chords": []}

        debug_log("Chords", chords)

        # Step 4: Combine Data
        combined_data = {
            "metadata": metadata,
            "features": {
                "spotify": spotify_features,
                "acoustic": spotify_features  
            },
            "chords": chords
        }
        debug_log("Combined Data", combined_data)

        # Step 5: Format for LLM
        formatted = format_for_llm(combined_data)
        debug_log("LLM Input", formatted)

        # Step 6: Analyze with LLM
        analysis = analyze_with_llm(formatted)
        debug_log("LLM Output", analysis)

        return analysis


#This is the main agent. It orchestrates the entire process of fetching data from various APIs, 
# combining it, and then sending it to the LLM for analysis. 
# Each step includes error handling and debug logging to ensure we can trace the flow of data 
# and identify any issues that arise.

