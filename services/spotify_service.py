import os
import random

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

MOOD_KEYWORDS: dict[str, list[str]] = {
    "happy": ["happy", "joyful", "cheerful", "uplifting", "feel good"],
    "sad": ["sad", "melancholy", "blue", "emotional"],
    "calm": ["calm", "relaxing", "ambient", "chill"],
    "energetic": ["energetic", "workout", "hype", "pump up"],
}

# Initialised on first use so that missing credentials do not crash app startup.
_client: spotipy.Spotify | None = None


def _get_client() -> spotipy.Spotify:
    global _client
    if _client is None:
        client_id = os.environ.get("SPOTIFY_CLIENT_ID")
        client_secret = os.environ.get("SPOTIFY_CLIENT_SECRET")
        if not client_id or not client_secret:
            raise RuntimeError(
                "SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET must be set in the environment."
            )
        _client = spotipy.Spotify(
            client_credentials_manager=SpotifyClientCredentials(
                client_id=client_id,
                client_secret=client_secret,
            )
        )
    return _client


def search_playlists_by_mood(mood: str, limit: int = 50) -> list[dict]:
    """
    Search Spotify for playlists matching the given mood.

    Returns up to 5 randomly selected results, or an empty list if the mood
    is unrecognised or the Spotify request fails.
    """
    if mood not in MOOD_KEYWORDS:
        return []

    keywords = MOOD_KEYWORDS[mood]
    query = "(" + " OR ".join(f'"{k}"' for k in keywords) + ") playlist"

    try:
        results = _get_client().search(q=query, type="playlist", limit=limit)
    except Exception:
        return []

    playlists = [
        {
            "name": item["name"],
            "url": item["external_urls"]["spotify"],
            "image": item["images"][0]["url"] if item["images"] else None,
        }
        for item in results["playlists"]["items"]
        if item
    ]

    random.shuffle(playlists)
    return playlists[:5]
