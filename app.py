from flask import Flask, render_template, request, send_from_directory, jsonify
import sqlite3
import os

app = Flask(__name__)

DB_FILE = "annotations.db"

def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute('''
        CREATE TABLE IF NOT EXISTS annotations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sound_file TEXT,
            start_time REAL,
            end_time REAL,
            label TEXT,
            description TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        conn.commit()

@app.route("/")
def index():
    return render_template("index.html", sound_file="goro_goro.mp3")

@app.route("/sounds/<filename>")
def sounds(filename):
    return send_from_directory("static/sounds", filename)

@app.route("/save_annotation", methods=["POST"])
def save_annotation():
    data = request.json
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute('''
        INSERT INTO annotations (sound_file, start_time, end_time, label, description)
        VALUES (?, ?, ?, ?, ?)
        ''', (
            data["sound_file"],
            data["start_time"],
            data["end_time"],
            data["label"],
            data["description"]
        ))
        conn.commit()
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
