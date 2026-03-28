import base64
import os
import random
import time
import urllib.parse

import requests
import spotipy

MOOD_KEYWORDS: dict[str, list[str]] = {
    "happy": ["happy", "joyful", "cheerful", "uplifting", "feel good"],
    "sad": ["sad", "melancholy", "blue", "emotional"],
    "calm": ["calm", "relaxing", "ambient", "chill"],
    "energetic": ["energetic", "workout", "hype", "pump up"],
}

SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SCOPE = "playlist-read-public"


def _credentials_header() -> str:
    client_id = os.environ.get("SPOTIFY_CLIENT_ID", "")
    client_secret = os.environ.get("SPOTIFY_CLIENT_SECRET", "")
    return "Basic " + base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()


def get_auth_url(state: str = "") -> str:
    """Build the Spotify authorization URL."""
    params = {
        "client_id": os.environ.get("SPOTIFY_CLIENT_ID", ""),
        "response_type": "code",
        "redirect_uri": os.environ.get("SPOTIFY_REDIRECT_URI", "http://127.0.0.1:5000/callback"),
        "scope": SCOPE,
        "state": state,
    }
    return SPOTIFY_AUTH_URL + "?" + urllib.parse.urlencode(params)


def exchange_code(code: str) -> dict:
    """Exchange an authorization code for a token dict."""
    resp = requests.post(
        SPOTIFY_TOKEN_URL,
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": os.environ.get("SPOTIFY_REDIRECT_URI", "http://127.0.0.1:5000/callback"),
        },
        headers={
            "Authorization": _credentials_header(),
            "Content-Type": "application/x-www-form-urlencoded",
        },
        timeout=10,
    )
    resp.raise_for_status()
    token = resp.json()
    token["expires_at"] = int(time.time()) + token.get("expires_in", 3600)
    return token


def refresh_token(token_info: dict) -> dict:
    """Refresh an expired token. Returns updated token dict."""
    resp = requests.post(
        SPOTIFY_TOKEN_URL,
        data={
            "grant_type": "refresh_token",
            "refresh_token": token_info["refresh_token"],
        },
        headers={
            "Authorization": _credentials_header(),
            "Content-Type": "application/x-www-form-urlencoded",
        },
        timeout=10,
    )
    resp.raise_for_status()
    new_token = resp.json()
    new_token["expires_at"] = int(time.time()) + new_token.get("expires_in", 3600)
    # Spotify doesn't always return a new refresh_token — keep the old one
    if "refresh_token" not in new_token:
        new_token["refresh_token"] = token_info["refresh_token"]
    return new_token


def is_token_expired(token_info: dict) -> bool:
    return int(time.time()) > token_info.get("expires_at", 0) - 60


def search_playlists_by_mood(mood: str, access_token: str, limit: int = 50) -> list[dict]:
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
        sp = spotipy.Spotify(auth=access_token)
        results = sp.search(q=query, type="playlist", limit=limit)
    except Exception as e:
        print(f"[Spotify] Search error: {e}")
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
