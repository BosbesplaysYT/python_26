import customtkinter as ctk
import requests
from tkinter import messagebox

API_URL = "https://bosbes.eu.pythonanywhere.com"  # Base URL for the API

class FlashcardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Flashcard App with Authentication")
        self.root.geometry("600x400")
        ctk.set_appearance_mode("dark")

        self.show_login_screen()

    def show_login_screen(self):
        self.clear_frames()

        self.login_frame = ctk.CTkFrame(self.root)
        self.login_frame.pack(expand=True, fill="both", padx=20, pady=20)

        title_label = ctk.CTkLabel(self.login_frame, text="Login", font=("Arial", 24))
        title_label.pack(pady=20)

        username_label = ctk.CTkLabel(self.login_frame, text="Username:")
        username_label.pack(pady=5)
        self.username_entry = ctk.CTkEntry(self.login_frame, width=400)
        self.username_entry.pack(pady=5)

        password_label = ctk.CTkLabel(self.login_frame, text="Password:")
        password_label.pack(pady=5)
        self.password_entry = ctk.CTkEntry(self.login_frame, width=400, show="*")
        self.password_entry.pack(pady=5)

        login_button = ctk.CTkButton(self.login_frame, text="Login", command=self.login)
        login_button.pack(pady=10)

        signup_button = ctk.CTkButton(self.login_frame, text="Sign Up", command=self.show_signup_screen)
        signup_button.pack(pady=10)

    def show_signup_screen(self):
        self.clear_frames()

        self.signup_frame = ctk.CTkFrame(self.root)
        self.signup_frame.pack(expand=True, fill="both", padx=20, pady=20)

        title_label = ctk.CTkLabel(self.signup_frame, text="Sign Up", font=("Arial", 24))
        title_label.pack(pady=20)

        username_label = ctk.CTkLabel(self.signup_frame, text="Username:")
        username_label.pack(pady=5)
        self.signup_username_entry = ctk.CTkEntry(self.signup_frame, width=400)
        self.signup_username_entry.pack(pady=5)

        password_label = ctk.CTkLabel(self.signup_frame, text="Password:")
        password_label.pack(pady=5)
        self.signup_password_entry = ctk.CTkEntry(self.signup_frame, width=400, show="*")
        self.signup_password_entry.pack(pady=5)

        signup_button = ctk.CTkButton(self.signup_frame, text="Sign Up", command=self.signup)
        signup_button.pack(pady=10)

        back_button = ctk.CTkButton(self.signup_frame, text="Back to Login", command=self.show_login_screen)
        back_button.pack(pady=10)

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if username and password:
            response = requests.post(f"{API_URL}/login", json={"username": username, "password": password})
            if response.status_code == 200:
                messagebox.showinfo("Success", "Login successful!")
                self.show_home_screen()  # Proceed to the home screen
            else:
                messagebox.showerror("Error", response.json().get("error", "Login failed."))
        else:
            messagebox.showwarning("Input Error", "Please enter both username and password.")

    def signup(self):
        username = self.signup_username_entry.get().strip()
        password = self.signup_password_entry.get().strip()

        if username and password:
            response = requests.post(f"{API_URL}/signup", json={"username": username, "password": password})
            if response.status_code == 201:
                messagebox.showinfo("Success", "User created successfully! You can now log in.")
                self.show_login_screen()  # Return to login screen
            else:
                messagebox.showerror("Error", response.json().get("error", "Sign up failed."))
        else:
            messagebox.showwarning("Input Error", "Please enter both username and password.")

    def clear_frames(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_home_screen(self):
        self.clear_frames()
        home_frame = ctk.CTkFrame(self.root)
        home_frame.pack(expand=True, fill="both", padx=20, pady=20)

        welcome_label = ctk.CTkLabel(home_frame, text="Welcome to the Flashcard App!", font=("Arial", 24))
        welcome_label.pack(pady=20)

        # You can add additional home screen functionalities here

if __name__ == "__main__":
    root = ctk.CTk()
    app = FlashcardApp(root)
    root.mainloop()
