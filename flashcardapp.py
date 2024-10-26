import tkinter as tk
from tkinter import messagebox
import json
import random

# File to store flashcards
FLASHCARD_FILE = "flashcards.json"

# Load flashcards from file
def load_flashcards():
    try:
        with open(FLASHCARD_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Save flashcards to file
def save_flashcards(flashcards):
    with open(FLASHCARD_FILE, "w") as file:
        json.dump(flashcards, file)

class FlashcardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Flashcard App")
        self.flashcards = load_flashcards()
        self.current_card = None
        self.showing_answer = False

        # Main frame
        self.frame = tk.Frame(self.root, padx=20, pady=20)
        self.frame.pack()

        # Card display area
        self.card_text = tk.StringVar()
        self.card_label = tk.Label(self.frame, textvariable=self.card_text, font=("Arial", 24), wraplength=400)
        self.card_label.pack()

        # Buttons
        self.show_button = tk.Button(self.frame, text="Show Answer", command=self.flip_card)
        self.show_button.pack(pady=5)

        self.next_button = tk.Button(self.frame, text="Next Card", command=self.next_card)
        self.next_button.pack(pady=5)

        self.add_button = tk.Button(self.frame, text="Add Flashcard", command=self.add_flashcard)
        self.add_button.pack(pady=5)

        # Start by showing the first card
        self.next_card()

    def next_card(self):
        if self.flashcards:
            self.current_card = random.choice(self.flashcards)
            self.card_text.set("Q: " + self.current_card["question"])
            self.showing_answer = False
            self.show_button.config(state="normal")
        else:
            self.card_text.set("No flashcards available. Add some!")

    def flip_card(self):
        if self.current_card and not self.showing_answer:
            self.card_text.set("A: " + self.current_card["answer"])
            self.showing_answer = True
            self.show_button.config(state="disabled")

    def add_flashcard(self):
        # New window for adding a flashcard
        add_window = tk.Toplevel(self.root)
        add_window.title("Add New Flashcard")

        tk.Label(add_window, text="Question:").pack(pady=5)
        question_entry = tk.Entry(add_window, width=50)
        question_entry.pack(pady=5)

        tk.Label(add_window, text="Answer:").pack(pady=5)
        answer_entry = tk.Entry(add_window, width=50)
        answer_entry.pack(pady=5)

        def save_card():
            question = question_entry.get().strip()
            answer = answer_entry.get().strip()
            if question and answer:
                self.flashcards.append({"question": question, "answer": answer})
                save_flashcards(self.flashcards)
                messagebox.showinfo("Success", "Flashcard added successfully!")
                add_window.destroy()
                self.next_card()
            else:
                messagebox.showwarning("Input Error", "Please enter both question and answer.")

        tk.Button(add_window, text="Save Flashcard", command=save_card).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = FlashcardApp(root)
    root.mainloop()
