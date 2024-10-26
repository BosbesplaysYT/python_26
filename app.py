from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)
DB_FILE = "flashcards.db"  # Path to the SQLite database file on PythonAnywhere

def get_db_connection():
    """Connect to the SQLite database and return the connection object."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_database():
    """Create the flashcards table if it doesn't already exist."""
    if not os.path.exists(DB_FILE):  # Check if the database file exists
        conn = get_db_connection()
        conn.execute('''
            CREATE TABLE IF NOT EXISTS flashcards (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT NOT NULL,
                answer TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()
        print("Database initialized successfully.")

# Call the database initialization function
initialize_database()

# Define API endpoints
@app.route("/flashcard", methods=["GET"])
def get_random_flashcard():
    conn = get_db_connection()
    flashcard = conn.execute("SELECT * FROM flashcards ORDER BY RANDOM() LIMIT 1").fetchone()
    conn.close()
    if flashcard:
        return jsonify({"id": flashcard["id"], "question": flashcard["question"], "answer": flashcard["answer"]})
    return jsonify({"error": "No flashcards available"}), 404

@app.route("/flashcard", methods=["POST"])
def add_flashcard():
    data = request.get_json()
    question = data.get("question")
    answer = data.get("answer")
    if not question or not answer:
        return jsonify({"error": "Invalid data"}), 400
    conn = get_db_connection()
    conn.execute("INSERT INTO flashcards (question, answer) VALUES (?, ?)", (question, answer))
    conn.commit()
    conn.close()
    return jsonify({"message": "Flashcard added successfully"}), 201

@app.route("/flashcards", methods=["GET"])
def get_all_flashcards():
    conn = get_db_connection()
    flashcards = conn.execute("SELECT * FROM flashcards").fetchall()
    conn.close()
    return jsonify([{"id": fc["id"], "question": fc["question"], "answer": fc["answer"]} for fc in flashcards])

if __name__ == "__main__":
    app.run()
