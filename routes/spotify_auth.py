from flask import Blueprint, redirect, request, session, url_for
from services.spotify_service import get_auth_url, exchange_code

spotify_auth_bp = Blueprint("spotify_auth", __name__)


@spotify_auth_bp.route("/spotify/login")
def spotify_login():
    # Encode the next URL into the OAuth state param — no session needed
    next_url = request.args.get("next", url_for("main.home"))
    return redirect(get_auth_url(state=next_url))


@spotify_auth_bp.route("/callback")
def callback():
    if request.args.get("error"):
        return redirect(url_for("main.home"))

    code = request.args.get("code")
    next_url = request.args.get("state") or url_for("main.home")

    if not code:
        return redirect(url_for("main.home"))

    try:
        token_info = exchange_code(code)
        session["spotify_token"] = token_info
        session.modified = True
    except Exception as e:
        print(f"[Spotify] Token exchange failed: {e}")
        return redirect(url_for("main.home"))

    return redirect(next_url)
