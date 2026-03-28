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
    params = {
        "client_id": os.environ.get("SPOTIFY_CLIENT_ID", ""),
        "response_type": "code",
        "redirect_uri": os.environ.get("SPOTIFY_REDIRECT_URI", "http://127.0.0.1:5000/callback"),
        "scope": SCOPE,
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
    return int(time.time()) > token_info.get("expires_at", 0) - 60


def search_playlists_by_mood(mood: str, access_token: str, limit: int = 50) -> list[dict]:
    if mood not in MOOD_KEYWORDS:
        print(f"[SEARCH] unknown mood: {mood!r}")
        return []

    keywords = MOOD_KEYWORDS[mood]
    query = "(" + " OR ".join(f'"{k}"' for k in keywords) + ") playlist"
    print(f"[SEARCH] query={query!r}")

    try:
        sp = spotipy.Spotify(auth=access_token)
        results = sp.search(q=query, type="playlist", limit=limit)
        raw_items = results["playlists"]["items"]
        print(f"[SEARCH] Spotify returned {len(raw_items)} raw items")
    except Exception as e:
        print(f"[SEARCH] FAILED: {e}")
        return []

    playlists = [
        {
            "name": item["name"],
            "url": item["external_urls"]["spotify"],
            "image": item["images"][0]["url"] if item["images"] else None,
        }
        for item in raw_items
        if item
    ]

    random.shuffle(playlists)
    result = playlists[:5]
    print(f"[SEARCH] returning {len(result)} playlists")
    return result
