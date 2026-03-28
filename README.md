# Moodify

A full-stack Flask web application that recommends Spotify playlists based on your current mood. Select how you feel, get five live playlist suggestions from the Spotify API, save your favourites, and track your mood history on a personal dashboard.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.1-000000?logo=flask)
![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?logo=sqlite)
![Spotify](https://img.shields.io/badge/API-Spotify-1DB954?logo=spotify&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

---

## Features

- Mood selector — Happy, Sad, Energetic, Calm
- Live Spotify playlist recommendations via the Spotify Web API
- User registration and login with hashed passwords
- Save and unsave playlists to a personal library (AJAX, no page reload)
- Mood history dashboard with a Chart.js bar chart
- Account management — update email, change password, delete account
- Real-time client-side password validation hints
- Flash messages for all user feedback

---

## Tech stack

| Layer | Technology |
|---|---|
| Backend | Python 3.10+, Flask 3.1, Flask-Login, Flask-SQLAlchemy |
| Database | SQLite (dev) — swappable via `DATABASE_URL` env var |
| External API | Spotify Web API via [Spotipy](https://spotipy.readthedocs.io/) |
| Frontend | Jinja2 templates, hand-written CSS, Vanilla JS |
| Visualisation | [Chart.js](https://www.chartjs.org/) |
| Icons | [Bootstrap Icons](https://icons.getbootstrap.com/) |
| Auth | Werkzeug password hashing, Flask-Login session management |

---

## Project structure

```
moodify/
├── app.py                    # App factory, config, blueprints, context processor
├── requirements.txt
├── .env.example              # Required environment variable reference
│
├── models/
│   ├── user.py               # User — relationships to playlists and mood logs
│   ├── mood_log.py           # One entry per mood selection, per user
│   └── saved_playlist.py     # Bookmarked Spotify playlists per user
│
├── routes/
│   ├── auth.py               # /auth — register, login, logout, account management
│   ├── main.py               # / — home, about
│   ├── mood.py               # /mood — stats page and JSON data endpoint
│   └── playlist.py           # /playlist — generate, save, delete, library
│
├── services/
│   └── spotify_service.py    # Spotify API client, lazy-initialised
│
├── static/
│   ├── css/style.css
│   ├── js/app.js             # AJAX save/delete, password toggle, flash dismiss
│   └── js/charts.js          # Chart.js mood bar chart
│
└── templates/
    ├── base.html             # Layout, navbar, footer, global flash messages
    ├── home.html
    ├── about.html
    ├── login.html
    ├── register.html
    ├── account.html
    ├── results.html
    ├── my_playlists.html
    └── mood_stats.html
```

---

## Local setup

### Prerequisites

- Python 3.10 or higher
- A [Spotify Developer](https://developer.spotify.com/dashboard) account

### 1. Clone and create a virtual environment

```bash
git clone https://github.com/your-username/moodify.git
cd moodify

python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` with your values — see `.env.example` for descriptions.

**Getting Spotify credentials:**
1. Go to [developer.spotify.com/dashboard](https://developer.spotify.com/dashboard)
2. Create a new app — the name and redirect URI do not matter for this project
3. Copy the **Client ID** and **Client Secret**

This app uses Spotify's [Client Credentials Flow](https://developer.spotify.com/documentation/web-api/tutorials/client-credentials-flow). No user Spotify login is required.

### 4. Run

```bash
python app.py
```

The app starts at **http://127.0.0.1:5000**

The SQLite database is created automatically at `instance/moodify.db` on first run.

---

## Deployment

### Render (recommended)

1. Push the repo to GitHub
2. Create a new **Web Service** on [render.com](https://render.com) and connect the repo
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `gunicorn "app:create_app()"`
5. Add the three environment variables from `.env.example` in the Render dashboard

### PostgreSQL (production database)

Set `DATABASE_URL` to a `postgresql://` connection string in your environment. Flask-SQLAlchemy uses it automatically.

### Production checklist

- `SECRET_KEY` is set to a long random string (not the default fallback)
- `FLASK_DEBUG` is unset or `false`
- A production WSGI server (`gunicorn`) is used — not `python app.py`

---

## Known limitations

- No CSRF protection on forms (planned)
- No rate limiting on auth endpoints (planned)
- SQLite is not suitable for concurrent production traffic — use PostgreSQL

---

## License

MIT
