from flask import Blueprint, redirect, request, session, url_for, flash
from services.spotify_service import get_auth_url, exchange_code

spotify_auth_bp = Blueprint("spotify_auth", __name__)


@spotify_auth_bp.route("/spotify/login")
def spotify_login():
    next_url = request.args.get("next", url_for("main.home"))
    return redirect(get_auth_url(state=next_url))


@spotify_auth_bp.route("/callback")
def callback():
    error = request.args.get("error")
    code = request.args.get("code")
    next_url = request.args.get("state") or url_for("main.home")

    print(f"[CB] error={error!r} code_present={bool(code)} next_url={next_url!r}")

    if error:
        flash(f"Spotify denied access: {error}", "error")
        return redirect(url_for("main.home"))

    if not code:
        flash("No authorization code received from Spotify.", "error")
        return redirect(url_for("main.home"))

    try:
        token_info = exchange_code(code)
        print(f"[CB] token exchange OK — keys={list(token_info.keys())}")
        session["spotify_token"] = token_info
        session.modified = True
        print(f"[CB] token stored in session — redirecting to {next_url!r}")
    except Exception as e:
        print(f"[CB] token exchange FAILED: {e}")
        flash(f"Spotify token exchange failed: {e}", "error")
        return redirect(url_for("main.home"))

    return redirect(next_url)


@spotify_auth_bp.route("/debug")
def debug():
    """Temporary debug endpoint — remove before deploying."""
    from flask import jsonify
    import time
    token_info = session.get("spotify_token")
    if not token_info:
        return jsonify({"session": "no spotify_token stored"})

    now = int(time.time())
    return jsonify({
        "token_present": True,
        "token_keys": list(token_info.keys()),
        "expires_at": token_info.get("expires_at"),
        "expired": now > token_info.get("expires_at", 0) - 60,
        "seconds_remaining": token_info.get("expires_at", 0) - now,
        "scope": token_info.get("scope"),
    })
