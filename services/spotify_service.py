import base64
import os
import random
import time
import urllib.parse

import requests

MOOD_KEYWORDS: dict[str, list[str]] = {
    "happy": ["happy", "joyful", "cheerful", "uplifting", "feel good"],
    "sad": ["sad", "melancholy", "blue", "emotional"],
    "calm": ["calm", "relaxing", "ambient", "chill"],
    "energetic": ["energetic", "workout", "hype", "pump up"],
}

# Simple single-term queries per mood — reliable with Spotify's search API.
# Complex boolean OR syntax is not officially supported and returns 0 results
# for most moods.
MOOD_QUERIES: dict[str, str] = {
    "happy": "happy upbeat feel good",
    "sad": "sad emotional melancholy",
    "calm": "calm relaxing chill ambient",
    "energetic": "energetic workout pump up hype",
}

SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SCOPE = ""  # public playlist search requires no scope


def _credentials_header() -> str:
    client_id = os.environ.get("SPOTIFY_CLIENT_ID", "")
    client_secret = os.environ.get("SPOTIFY_CLIENT_SECRET", "")
    return "Basic " + base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()


def get_auth_url(state: str = "") -> str:
    params = {
        "client_id": os.environ.get("SPOTIFY_CLIENT_ID", ""),
        "response_type": "code",
        "redirect_uri": os.environ.get("SPOTIFY_REDIRECT_URI", "http://127.0.0.1:5000/callback"),
        "state": state,
    }
    return SPOTIFY_AUTH_URL + "?" + urllib.parse.urlencode(params)


def exchange_code(code: str) -> dict:
    redirect_uri = os.environ.get("SPOTIFY_REDIRECT_URI", "http://127.0.0.1:5000/callback")
    print(f"[TOKEN] exchanging code, redirect_uri={redirect_uri!r}")

    resp = requests.post(
        SPOTIFY_TOKEN_URL,
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri,
        },
        headers={
            "Authorization": _credentials_header(),
            "Content-Type": "application/x-www-form-urlencoded",
        },
        timeout=10,
    )

    print(f"[TOKEN] Spotify response status: {resp.status_code}")
    if not resp.ok:
        print(f"[TOKEN] Error body: {resp.text}")
    resp.raise_for_status()

    token = resp.json()
    token["expires_at"] = int(time.time()) + token.get("expires_in", 3600)
    return token


def refresh_token(token_info: dict) -> dict:
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
    print(f"[REFRESH] status: {resp.status_code}")
    resp.raise_for_status()
    new_token = resp.json()
    new_token["expires_at"] = int(time.time()) + new_token.get("expires_in", 3600)
    if "refresh_token" not in new_token:
        new_token["refresh_token"] = token_info["refresh_token"]
    return new_token


def is_token_expired(token_info: dict) -> bool:
    expires_at = token_info.get("expires_at")
    if not expires_at:
        return False  # no expiry info — assume valid rather than deleting token
    return int(time.time()) > expires_at - 60


def search_playlists_by_mood(mood: str, access_token: str, limit: int = 50) -> list[dict]:
    """
    Search Spotify for playlists matching the given mood.
    Raises RuntimeError with the exact Spotify error message on failure
    so callers can surface it to the user.
    """
    if mood not in MOOD_QUERIES:
        print(f"[SEARCH] unknown mood: {mood!r}")
        return []

    query = MOOD_QUERIES[mood]
    print(f"[SEARCH] mood={mood!r} query={query!r}")

    resp = requests.get(
        "https://api.spotify.com/v1/search",
        params={"q": query, "type": "playlist", "limit": limit},
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=10,
    )

    print(f"[SEARCH] HTTP {resp.status_code}")

    if not resp.ok:
        try:
            error_msg = resp.json().get("error", {}).get("message", resp.text)
        except Exception:
            error_msg = resp.text
        print(f"[SEARCH] error: {error_msg}")
        raise RuntimeError(f"Spotify {resp.status_code}: {error_msg}")

    items = resp.json().get("playlists", {}).get("items", [])
    print(f"[SEARCH] raw items: {len(items)}")

    playlists = [
        {
            "name": item["name"],
            "url": item["external_urls"]["spotify"],
            "image": item["images"][0]["url"] if item.get("images") else None,
        }
        for item in items
        if item and item.get("name") and item.get("external_urls", {}).get("spotify")
    ]

    random.shuffle(playlists)
    result = playlists[:5]
    print(f"[SEARCH] returning {len(result)} playlists")
    return result
