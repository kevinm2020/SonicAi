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
            return "❌ Song not found or API error. Try a different input."

        # Step 2: Spotify features
        spotify_features = get_spotify_features(song_name, artist_name)
        print("SPOTIFY FEATURES:", spotify_features)
        if spotify_features is None:
            spotify_features = {}

        # Step 3: Chords
        chords = get_chords(metadata)
        if chords is None:
            chords = {"chords": []}

        # Step 4: Combine data (THIS is the key fix)
        combined_data = {
            "metadata": metadata,
            "features": {
                "spotify": spotify_features
            },
            "chords": chords
        }

        # Step 5: Format for LLM
        formatted = format_for_llm(combined_data)

        # Step 6: LLM analysis
        analysis_raw = analyze_with_llm(formatted)

        if isinstance(analysis_raw, dict):
            analysis_text = analysis_raw.get("analysis", "")
        else:
            analysis_text = analysis_raw


        # Step 7: Return FULL STRUCTURE (not just string)
        return {
            "metadata": metadata,
            "features": {
                "spotify": spotify_features
            },
            "chords": chords,
            "analysis": analysis_text
        }


#This is the main agent. It orchestrates the entire process of fetching data from various APIs, 
# combining it, and then sending it to the LLM for analysis. 
# Each step includes error handling and debug logging to ensure we can trace the flow of data 
# and identify any issues that arise.

