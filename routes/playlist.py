from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user, AnonymousUserMixin

from extensions import db
from models.mood_log import MoodLog
from models.saved_playlist import SavedPlaylist
from services.spotify_service import search_playlists_by_mood, MOOD_KEYWORDS


playlist_bp = Blueprint("playlist", __name__, url_prefix="/playlist")


@playlist_bp.route("/generate/<mood>")
def generate(mood: str):
    """
    Handle playlist recommendations for the given mood.

    :param mood: Mood chosen be the user.
    :return: Rendered results.html page.
    """
    if mood in MOOD_KEYWORDS and not isinstance(current_user, AnonymousUserMixin):
        log = MoodLog(user_id=current_user.id, mood=mood)
        db.session.add(log)
        db.session.commit()

    playlists = search_playlists_by_mood(mood)
    return render_template("results.html", mood=mood, playlists=playlists)


@playlist_bp.route("/save_playlist", methods=["POST"])
@login_required
def save_playlist():
    """
    Save a playlist.

    :return: 400 error if required fields are missing.
             {"status": "exists"} if the playlist is already saved.
             {"status": "ok"} on successful save.
    """
    data = request.json

    playlist_name = data.get("name")
    playlist_url = data.get("url")
    playlist_image = data.get("image")

    if not playlist_name or not playlist_url:
        return jsonify({"status": "error", "message": "Invalid playlist data"}), 400

    # avoid duplicates
    exists = SavedPlaylist.query.filter_by(
        user_id=current_user.id,
        playlist_url=playlist_url
    ).first()

    if exists:
        return jsonify({"status": "exists"})

    saved = SavedPlaylist(
        user_id=current_user.id,
        playlist_name=playlist_name,
        playlist_url=playlist_url,
        playlist_image=playlist_image,
    )
    db.session.add(saved)
    db.session.commit()

    return jsonify({"status": "ok"})


@playlist_bp.route("/my_playlists")
@login_required
def my_playlists():
    """
    Show user's saved playlists.

    :return: Rendered my_playlists.html page.
    """
    playlists = SavedPlaylist.query.filter_by(user_id=current_user.id).all()
    return render_template("my_playlists.html", playlists=playlists)


@playlist_bp.route("/delete", methods=["DELETE"])
@login_required
def delete_playlist():
    """
    Delete user's saved playlist.

    :return: 400 error if the URL is missing.
             404 error if no playlist exists for the given URL and user.
             {"status": "ok"} on successful deletion.
    """
    data = request.get_json()
    playlist_url = data.get("url")

    if not playlist_url:
        return jsonify({"status": "error", "message": "URL missing"}), 400

    playlist = SavedPlaylist.query.filter_by(
        playlist_url=playlist_url,
        user_id=current_user.id
    ).first()

    if not playlist:
        return jsonify({"status": "error", "message": "Playlist not found"}), 404

    db.session.delete(playlist)
    db.session.commit()

    return jsonify({"status": "ok"})
