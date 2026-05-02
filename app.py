from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

# ✅ Use this path for local
conn = sqlite3.connect(DB_PATH)
# 🔥 IMPORTANT (for Render deployment)
# Uncomment this and comment above line when deploying
# DB_PATH = "/data/responses.db"


# ---------------------------
# ✅ Initialize Database
# ---------------------------
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

# Run once at startup
init_db()


# ---------------------------
# ✅ Home Route
# ---------------------------
@app.route('/')
def home():
    return render_template('Survey.html')


# ---------------------------
# ✅ Submit Route
# ---------------------------
@app.route('/submit', methods=['POST'])
def submit():
    try:
        data = request.get_json()
        answers = data.get("answers")

        if not answers:
            return jsonify({
                "status": "error",
                "message": "No answers received"
            }), 400

        print("Received:", answers)

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO responses (timestamp, answers)
            VALUES (?, ?)
        ''', (
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            str(answers)
        ))

        conn.commit()
        conn.close()

        return jsonify({
            "status": "success",
            "message": "Saved successfully"
        })

    except Exception as e:
        print("Error:", e)
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# ---------------------------
# ✅ View Responses (for testing/admin)
# ---------------------------
@app.route('/responses')
def view_responses():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM responses ORDER BY id DESC")
    rows = cursor.fetchall()

    conn.close()
    return str(rows)


# ---------------------------
# ✅ Run App
# ---------------------------
if __name__ == '__main__':
    app.run(debug=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
