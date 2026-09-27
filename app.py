import os
import sqlite3
import uuid
from contextlib import closing
from flask import Flask, render_template, jsonify, request, session

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-only-key")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "equation.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with closing(get_db()) as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS equations (
            number INTEGER PRIMARY KEY,
            session_id TEXT NOT NULL,
            equation TEXT,
            result TEXT,
            time TEXT DEFAULT CURRENT_TIMESTAMP
        )""")
        conn.commit()


init_db()


def get_session_id():
    if "sid" not in session:
        session["sid"] = str(uuid.uuid4())
    return session["sid"]


@app.route("/")
def runapp():
    session["sid"] = str(uuid.uuid4())
    with closing(get_db()) as conn:
        conn.execute("DELETE FROM equations WHERE time < datetime('now', '-1 hour')")
        conn.commit()
    return render_template("index.html")


@app.route("/api/calculations")
def getcalcs():
    with closing(get_db()) as conn:
        rows = conn.execute(
            "SELECT number, equation, result, time FROM equations "
            "WHERE session_id = ? ORDER BY number",
            (get_session_id(),),
        ).fetchall()
    return jsonify([dict(row) for row in rows])


@app.route("/api/calculations", methods=["POST"])
def addcalcs():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "request body must be a JSON object"}), 400

    equation_value = data.get("equation")
    result_value = data.get("result")
    if equation_value is None or result_value is None:
        return jsonify({"error": "equation and result are required"}), 400

    with closing(get_db()) as conn:
        conn.execute(
            "INSERT INTO equations (session_id, equation, result) VALUES (?, ?, ?)",
            (get_session_id(), equation_value, str(result_value)),
        )
        conn.commit()
    return jsonify({"status": "success"}), 201


if __name__ == "__main__":
    app.run(debug=True)