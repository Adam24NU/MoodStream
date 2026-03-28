"""
Demo playlist data for MoodStream.

5 curated playlists per mood.  Images are stable placeholder thumbnails;
URLs open Spotify's own search page for each playlist title so they are
real, clickable, and useful to visitors.

To switch back to the live Spotify API set DEMO_MODE=false in your
environment and supply SPOTIFY_CLIENT_ID / SPOTIFY_CLIENT_SECRET.
"""

DEMO_PLAYLISTS: dict[str, list[dict]] = {
    "happy": [
        {
            "name": "Good Vibes Only",
            "url": "https://open.spotify.com/search/good%20vibes%20only",
            "image": "https://placehold.co/300x300/FFD93D/333333?text=Good+Vibes",
        },
        {
            "name": "Sunshine Pop",
            "url": "https://open.spotify.com/search/sunshine%20pop",
            "image": "https://placehold.co/300x300/FF8C42/ffffff?text=Sunshine+Pop",
        },
        {
            "name": "Feel Good Hits",
            "url": "https://open.spotify.com/search/feel%20good%20hits",
            "image": "https://placehold.co/300x300/F4D35E/333333?text=Feel+Good+Hits",
        },
        {
            "name": "Happy Indie",
            "url": "https://open.spotify.com/search/happy%20indie",
            "image": "https://placehold.co/300x300/E63946/ffffff?text=Happy+Indie",
        },
        {
            "name": "Uplifting Anthems",
            "url": "https://open.spotify.com/search/uplifting%20anthems",
            "image": "https://placehold.co/300x300/06D6A0/333333?text=Uplifting+Anthems",
        },
    ],
    "sad": [
        {
            "name": "Late Night Feelings",
            "url": "https://open.spotify.com/search/late%20night%20feelings",
            "image": "https://placehold.co/300x300/4A4E69/ffffff?text=Late+Night+Feelings",
        },
        {
            "name": "Rainy Day Blues",
            "url": "https://open.spotify.com/search/rainy%20day%20blues",
            "image": "https://placehold.co/300x300/6B8CAE/ffffff?text=Rainy+Day+Blues",
        },
        {
            "name": "Melancholy Soul",
            "url": "https://open.spotify.com/search/melancholy%20soul",
            "image": "https://placehold.co/300x300/3D405B/ffffff?text=Melancholy+Soul",
        },
        {
            "name": "Heartbreak Hits",
            "url": "https://open.spotify.com/search/heartbreak%20hits",
            "image": "https://placehold.co/300x300/8B8C89/ffffff?text=Heartbreak+Hits",
        },
        {
            "name": "Quiet Storm",
            "url": "https://open.spotify.com/search/quiet%20storm",
            "image": "https://placehold.co/300x300/293241/ffffff?text=Quiet+Storm",
        },
    ],
    "calm": [
        {
            "name": "Deep Focus",
            "url": "https://open.spotify.com/search/deep%20focus",
            "image": "https://placehold.co/300x300/A8DADC/333333?text=Deep+Focus",
        },
        {
            "name": "Peaceful Piano",
            "url": "https://open.spotify.com/search/peaceful%20piano",
            "image": "https://placehold.co/300x300/C9F0CD/333333?text=Peaceful+Piano",
        },
        {
            "name": "Nature Sounds & Chill",
            "url": "https://open.spotify.com/search/nature%20sounds%20chill",
            "image": "https://placehold.co/300x300/95D5B2/333333?text=Nature+%26+Chill",
        },
        {
            "name": "Ambient Drift",
            "url": "https://open.spotify.com/search/ambient%20drift",
            "image": "https://placehold.co/300x300/74B3CE/ffffff?text=Ambient+Drift",
        },
        {
            "name": "Lo-Fi Study Beats",
            "url": "https://open.spotify.com/search/lofi%20study%20beats",
            "image": "https://placehold.co/300x300/B5C0D0/333333?text=Lo-Fi+Study",
        },
    ],
    "energetic": [
        {
            "name": "Ultimate Workout",
            "url": "https://open.spotify.com/search/ultimate%20workout",
            "image": "https://placehold.co/300x300/FF6B35/ffffff?text=Ultimate+Workout",
        },
        {
            "name": "Beast Mode",
            "url": "https://open.spotify.com/search/beast%20mode",
            "image": "https://placehold.co/300x300/E63946/ffffff?text=Beast+Mode",
        },
        {
            "name": "High Energy EDM",
            "url": "https://open.spotify.com/search/high%20energy%20edm",
            "image": "https://placehold.co/300x300/7B2D8B/ffffff?text=High+Energy+EDM",
        },
        {
            "name": "Power Run",
            "url": "https://open.spotify.com/search/power%20run",
            "image": "https://placehold.co/300x300/F72585/ffffff?text=Power+Run",
        },
        {
            "name": "Hype Anthems",
            "url": "https://open.spotify.com/search/hype%20anthems",
            "image": "https://placehold.co/300x300/FF9F1C/333333?text=Hype+Anthems",
        },
    ],
}
