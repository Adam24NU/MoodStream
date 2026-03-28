import os
import random

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import MemoryCacheHandler

MOOD_KEYWORDS: dict[str, list[str]] = {
    "happy": ["happy", "joyful", "cheerful", "uplifting", "feel good"],
    "sad": ["sad", "melancholy", "blue", "emotional"],
    "calm": ["calm", "relaxing", "ambient", "chill"],
    "energetic": ["energetic", "workout", "hype", "pump up"],
}


def get_oauth() -> SpotifyOAuth:
    return SpotifyOAuth(
        client_id=os.environ.get("SPOTIFY_CLIENT_ID"),
        client_secret=os.environ.get("SPOTIFY_CLIENT_SECRET"),
        redirect_uri=os.environ.get("SPOTIFY_REDIRECT_URI", "http://127.0.0.1:5000/callback"),
        scope="playlist-read-public",
        cache_handler=MemoryCacheHandler(),
        show_dialog=False,
    )


def search_playlists_by_mood(mood: str, access_token: str, limit: int = 50) -> list[dict]:
    """
    Search Spotify for playlists matching the given mood using a user access token.

    Returns up to 5 randomly selected results, or an empty list if the mood
    is unrecognised or the Spotify request fails.
    """
    if mood not in MOOD_KEYWORDS:
        return []

    keywords = MOOD_KEYWORDS[mood]
    query = "(" + " OR ".join(f'"{k}"' for k in keywords) + ") playlist"

    try:
        sp = spotipy.Spotify(auth=access_token)
        results = sp.search(q=query, type="playlist", limit=limit)
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
