from pathlib import Path
import json
import sqlite3

from flask import Flask, jsonify, request
from reviewer import review_code

app = Flask(__name__)
DB_PATH = Path(__file__).with_name("reviews.db")
SCHEMA_PATH = Path(__file__).parents[1] / "database" / "schema.sql"


def connect_db():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    with connect_db() as connection:
        connection.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))


@app.get("/")
def home():
    return jsonify({
        "message": "Code Reviewer API is running",
        "supported_languages": ["java", "python"],
        "review_endpoint": "POST /review"
    })


@app.post("/review")
def create_review():
    data = request.get_json(silent=True) or {}
    language = str(data.get("language", "")).lower().strip()
    code = data.get("code", "")

    if language not in ("java", "python"):
        return jsonify({"error": "language must be java or python"}), 400
    if not isinstance(code, str) or not code.strip():
        return jsonify({"error": "code must be a non-empty string"}), 400

    try:
        result = review_code(language, code)
    except ValueError as error:
        return jsonify({"error": str(error)}), 400

    with connect_db() as connection:
        cursor = connection.execute(
            """INSERT INTO reviews
               (language, source_code, quality_score, issues_json)
               VALUES (?, ?, ?, ?)""",
            (language, code, result["quality_score"], json.dumps(result["issues"]))
        )
        review_id = cursor.lastrowid

    return jsonify({"review_id": review_id, "language": language, **result})


@app.get("/reviews")
def review_history():
    with connect_db() as connection:
        rows = connection.execute(
            "SELECT id, language, quality_score, created_at FROM reviews ORDER BY id DESC LIMIT 50"
        ).fetchall()
    return jsonify([dict(row) for row in rows])


if __name__ == "__main__":
    initialize_database()
    app.run(host="127.0.0.1", port=5000, debug=True)
