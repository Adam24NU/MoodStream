from flask import Blueprint, redirect, request, session, url_for
from services.spotify_service import get_oauth

spotify_auth_bp = Blueprint("spotify_auth", __name__)


@spotify_auth_bp.route("/spotify/login")
def spotify_login():
    session["spotify_next"] = request.args.get("next", url_for("main.home"))
    auth_url = get_oauth().get_authorize_url()
    return redirect(auth_url)


@spotify_auth_bp.route("/callback")
def callback():
    code = request.args.get("code")
    token_info = get_oauth().get_access_token(code, as_dict=True, check_cache=False)
    session["spotify_token"] = token_info
    next_url = session.pop("spotify_next", url_for("main.home"))
    return redirect(next_url)
