"""
CodeAlpha Backend Internship - Task 1: Simple URL Shortener
Stack: Flask (Python) + SQLite
"""
import os
import re
import secrets
import sqlite3
import string
from datetime import datetime, timezone
from urllib.parse import urlparse

from flask import Flask, g, jsonify, redirect, render_template, request

app = Flask(__name__)
DATABASE = os.environ.get(
    "DATABASE", os.path.join(os.path.dirname(os.path.abspath(__file__)), "urls.db")
)

ALPHABET = string.ascii_letters + string.digits
CODE_LENGTH = 6
RESERVED_CODES = {"api", "static"}
CUSTOM_CODE_RE = re.compile(r"^[A-Za-z0-9_-]{3,30}$")


# ---------- Database helpers ----------
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(_exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    with sqlite3.connect(DATABASE) as db:
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS urls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                short_code TEXT UNIQUE NOT NULL,
                original_url TEXT NOT NULL,
                clicks INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL
            )
            """
        )


# ---------- Utility functions ----------
def normalize_url(raw):
    """Add https:// if missing and validate. Returns clean URL or None."""
    raw = (raw or "").strip()
    if not raw:
        return None
    if not re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", raw):
        raw = "https://" + raw
    parsed = urlparse(raw)
    if parsed.scheme not in ("http", "https") or not parsed.netloc or "." not in parsed.netloc:
        return None
    return raw


def generate_code(db):
    """Generate a unique random short code."""
    while True:
        code = "".join(secrets.choice(ALPHABET) for _ in range(CODE_LENGTH))
        exists = db.execute("SELECT 1 FROM urls WHERE short_code = ?", (code,)).fetchone()
        if not exists and code not in RESERVED_CODES:
            return code


# ---------- Routes ----------
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/shorten", methods=["POST"])
def shorten():
    data = request.get_json(silent=True) or {}
    url = normalize_url(data.get("url"))
    if not url:
        return jsonify(error="Please provide a valid URL (http/https)."), 400

    db = get_db()
    custom = (data.get("custom_code") or "").strip()

    if custom:
        if not CUSTOM_CODE_RE.match(custom) or custom.lower() in RESERVED_CODES:
            return jsonify(error="Custom code must be 3-30 chars: letters, numbers, - or _."), 400
        if db.execute("SELECT 1 FROM urls WHERE short_code = ?", (custom,)).fetchone():
            return jsonify(error="That custom code is already taken."), 409
        code = custom
    else:
        # Re-use existing short code if this URL was already shortened
        row = db.execute(
            "SELECT short_code FROM urls WHERE original_url = ? ORDER BY id LIMIT 1", (url,)
        ).fetchone()
        if row:
            code = row["short_code"]
            return jsonify(short_code=code, short_url=request.host_url + code, original_url=url), 200
        code = generate_code(db)

    db.execute(
        "INSERT INTO urls (short_code, original_url, created_at) VALUES (?, ?, ?)",
        (code, url, datetime.now(timezone.utc).isoformat()),
    )
    db.commit()
    return jsonify(short_code=code, short_url=request.host_url + code, original_url=url), 201


@app.route("/api/stats/<code>")
def stats(code):
    row = get_db().execute("SELECT * FROM urls WHERE short_code = ?", (code,)).fetchone()
    if not row:
        return jsonify(error="Short code not found."), 404
    return jsonify(
        short_code=row["short_code"],
        original_url=row["original_url"],
        clicks=row["clicks"],
        created_at=row["created_at"],
    )


@app.route("/<code>")
def redirect_to_original(code):
    db = get_db()
    row = db.execute("SELECT original_url FROM urls WHERE short_code = ?", (code,)).fetchone()
    if not row:
        return jsonify(error="Short URL not found."), 404
    db.execute("UPDATE urls SET clicks = clicks + 1 WHERE short_code = ?", (code,))
    db.commit()
    return redirect(row["original_url"], code=302)


init_db()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
