import customtkinter as ctk
import sqlite3
from tkinter import messagebox

# Database setup
DB_FILE = "flashcards.db"

def create_table():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS flashcards (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT NOT NULL,
                answer TEXT NOT NULL
            )
        ''')
    print("Database initialized.")

class FlashcardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Flashcard App with SQLite and customtkinter")
        self.root.geometry("600x400")
        ctk.set_appearance_mode("dark")
        
        
        # Initialize database
        create_table()
        
        # Setup frames
        self.home_frame = None
        self.review_frame = None
        self.add_frame = None

        # Load Home Screen
        self.show_home_screen()

    def show_home_screen(self):
        self.clear_frames()
        
        self.home_frame = ctk.CTkFrame(self.root)
        self.home_frame.pack(expand=True, fill="both", padx=20, pady=20)

        title_label = ctk.CTkLabel(self.home_frame, text="Welcome to Flashcard App", font=("Arial", 24))
        title_label.pack(pady=20)

        review_button = ctk.CTkButton(self.home_frame, text="Review Flashcards", command=self.show_review_screen)
        review_button.pack(pady=10)

        add_button = ctk.CTkButton(self.home_frame, text="Add New Flashcard", command=self.show_add_screen)
        add_button.pack(pady=10)

    def show_review_screen(self):
        self.clear_frames()

        self.review_frame = ctk.CTkFrame(self.root)
        self.review_frame.pack(expand=True, fill="both", padx=20, pady=20)

        self.card_text = ctk.StringVar()
        self.current_card = None
        self.showing_answer = False

        card_label = ctk.CTkLabel(self.review_frame, textvariable=self.card_text, font=("Arial", 20), wraplength=400)
        card_label.pack(pady=20)

        show_button = ctk.CTkButton(self.review_frame, text="Show Answer", command=self.flip_card)
        show_button.pack(pady=10)

        next_button = ctk.CTkButton(self.review_frame, text="Next Card", command=self.next_card)
        next_button.pack(pady=10)

        home_button = ctk.CTkButton(self.review_frame, text="Back to Home", command=self.show_home_screen)
        home_button.pack(pady=10)

        # Load the first flashcard
        self.next_card()

    def show_add_screen(self):
        self.clear_frames()

        self.add_frame = ctk.CTkFrame(self.root)
        self.add_frame.pack(expand=True, fill="both", padx=20, pady=20)

        title_label = ctk.CTkLabel(self.add_frame, text="Add New Flashcard", font=("Arial", 24))
        title_label.pack(pady=20)

        question_label = ctk.CTkLabel(self.add_frame, text="Question:")
        question_label.pack(pady=5)
        question_entry = ctk.CTkEntry(self.add_frame, width=400)
        question_entry.pack(pady=5)

        answer_label = ctk.CTkLabel(self.add_frame, text="Answer:")
        answer_label.pack(pady=5)
        answer_entry = ctk.CTkEntry(self.add_frame, width=400)
        answer_entry.pack(pady=5)

        def save_card():
            question = question_entry.get().strip()
            answer = answer_entry.get().strip()
            if question and answer:
                with sqlite3.connect(DB_FILE) as conn:
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO flashcards (question, answer) VALUES (?, ?)", (question, answer))
                    conn.commit()
                messagebox.showinfo("Success", "Flashcard added successfully!")
                self.show_home_screen()
            else:
                messagebox.showwarning("Input Error", "Please enter both question and answer.")

        save_button = ctk.CTkButton(self.add_frame, text="Save Flashcard", command=save_card)
        save_button.pack(pady=10)

        home_button = ctk.CTkButton(self.add_frame, text="Back to Home", command=self.show_home_screen)
        home_button.pack(pady=10)

    def next_card(self):
        # Fetch a random flashcard from the database
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM flashcards ORDER BY RANDOM() LIMIT 1")
            row = cursor.fetchone()
            if row:
                self.current_card = {"id": row[0], "question": row[1], "answer": row[2]}
                self.card_text.set("Q: " + self.current_card["question"])
                self.showing_answer = False
            else:
                self.card_text.set("No flashcards available. Add some!")

    def flip_card(self):
        if self.current_card and not self.showing_answer:
            self.card_text.set("A: " + self.current_card["answer"])
            self.showing_answer = True

    def clear_frames(self):
        # Helper to clear all frames
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = ctk.CTk()
    app = FlashcardApp(root)
    root.mainloop()
