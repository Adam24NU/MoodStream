from extensions import db
from datetime import datetime


class SavedPlaylist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)

    playlist_name = db.Column(db.String(255), nullable=False)
    playlist_url = db.Column(db.String(500), nullable=False)
    playlist_image = db.Column(db.String(500))
    saved_at = db.Column(db.DateTime, default=datetime.utcnow)
