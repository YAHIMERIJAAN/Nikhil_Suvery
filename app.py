from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime
import json
import os

app = Flask(__name__)

# ✅ Database path (Render-safe)
DB_PATH = os.path.join(os.getcwd(), "responses.db")


# ✅ Initialize database
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            answers TEXT
        )
    ''')

    conn.commit()
    conn.close()


# Run DB setup at startup
init_db()


# ✅ Home route
@app.route('/')
def home():
    return render_template('Survey.html')


# ✅ Submit route
@app.route('/submit', methods=['POST'])
def submit():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"status": "error", "message": "No data received"}), 400

        answers = data.get("answers")

        if not answers:
            return jsonify({"status": "error", "message": "No answers received"}), 400

        print("Received answers:", answers)

        # ✅ Save to SQLite (store as JSON string → readable later)
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO responses (timestamp, answers) VALUES (?, ?)",
            (
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                json.dumps(answers)   # 👈 important improvement
            )
        )

        conn.commit()
        conn.close()

        return jsonify({
            "status": "success",
            "message": "Data saved successfully"
        })

    except Exception as e:
        print("Error:", e)
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# ✅ Optional: View responses in browser (VERY USEFUL)
@app.route('/responses')
def view_responses():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM responses ORDER BY id DESC")
    rows = cursor.fetchall()

    conn.close()

    # Convert JSON string back to list
    formatted = []
    for row in rows:
        formatted.append({
            "id": row[0],
            "timestamp": row[1],
            "answers": json.loads(row[2])
        })

    return jsonify(formatted)


# ✅ Local run only
if __name__ == '__main__':
    app.run(debug=True)
