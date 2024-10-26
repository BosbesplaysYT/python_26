from flask import Flask, request, jsonify
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
DB_FILE = "flashcards.db"  # Path to the SQLite database file

def get_db_connection():
    """Connect to the SQLite database and return the connection object."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_database():
    """Create the necessary tables if they don't already exist."""
    if not os.path.exists(DB_FILE):
        conn = get_db_connection()
        # Create the flashcards table
        conn.execute('''
            CREATE TABLE IF NOT EXISTS flashcards (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT NOT NULL,
                answer TEXT NOT NULL
            )
        ''')
        # Create the users table
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()
        print("Database initialized successfully.")

# Call the database initialization function
initialize_database()

# User Registration
@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required."}), 400

    hashed_password = generate_password_hash(password)
    
    try:
        conn = get_db_connection()
        conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        conn.close()
        return jsonify({"message": "User created successfully."}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Username already exists."}), 400

# User Login
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required."}), 400

    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    conn.close()

    if user and check_password_hash(user["password"], password):
        return jsonify({"message": "Login successful!"}), 200
    else:
        return jsonify({"error": "Invalid username or password."}), 401

# Existing API routes...

@app.route("/flashcard", methods=["GET"])
def get_random_flashcard():
    conn = get_db_connection()
    flashcard = conn.execute("SELECT * FROM flashcards ORDER BY RANDOM() LIMIT 1").fetchone()
    conn.close()
    if flashcard:
        return jsonify({"id": flashcard["id"], "question": flashcard["question"], "answer": flashcard["answer"]})
    return jsonify({"error": "No flashcards available."}), 404

@app.route("/flashcard", methods=["POST"])
def add_flashcard():
    data = request.get_json()
    question = data.get("question")
    answer = data.get("answer")
    if not question or not answer:
        return jsonify({"error": "Invalid data."}), 400
    conn = get_db_connection()
    conn.execute("INSERT INTO flashcards (question, answer) VALUES (?, ?)", (question, answer))
    conn.commit()
    conn.close()
    return jsonify({"message": "Flashcard added successfully."}), 201

@app.route("/flashcards", methods=["GET"])
def get_all_flashcards():
    conn = get_db_connection()
    flashcards = conn.execute("SELECT * FROM flashcards").fetchall()
    conn.close()
    return jsonify([{"id": fc["id"], "question": fc["question"], "answer": fc["answer"]} for fc in flashcards])

if __name__ == "__main__":
    app.run()
