from flask import Blueprint, jsonify, render_template
from flask_login import login_required, current_user
from models.mood_log import MoodLog


mood_bp = Blueprint("mood", __name__, url_prefix="/mood")


@mood_bp.route("/stats")
@login_required
def mood_stats():
    return render_template("mood_stats.html")


@mood_bp.route("/data")
@login_required
def mood_data():
    logs = MoodLog.query.filter_by(user_id=current_user.id).all()

    mood_counts = {}
    for log in logs:
        mood_counts[log.mood] = mood_counts.get(log.mood, 0) + 1

    return jsonify(mood_counts)
