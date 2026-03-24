import requests
import logging
from utils.helpers import debug_log

BASE_URL = "https://acousticbrainz.org/api/v1/low-level/{}"

logging.basicConfig(level=logging.DEBUG)

def get_acoustic_features(mbid):
    """
    Retrieve acoustic features from AcousticBrainz.
    Returns {} if the API fails or track not found.
    """
    if not mbid:
        debug_log("AcousticBrainz", "No MBID provided")
        return {}

    try:
        response = requests.get(BASE_URL.format(mbid))
        response.raise_for_status()
        data = response.json()
        # Example mapping: adjust keys if needed for your LLM
        features = {
            "tempo": data.get("rhythm", {}).get("bpm"),
            "energy": data.get("lowlevel", {}).get("dynamic_complexity"),
            "danceability": data.get("rhythm", {}).get("danceability"),
            "valence": data.get("tonal", {}).get("chords_key_strength")
        }
        debug_log("Acoustic Features", features)
        return features
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            logging.warning(f"AcousticBrainz: Track MBID {mbid} not found. Returning empty features.")
            return {}
        else:
            logging.error(f"AcousticBrainz API error: {e}")
            return {}
    except Exception as e:
        logging.error(f"AcousticBrainz request failed: {e}")
        return {}