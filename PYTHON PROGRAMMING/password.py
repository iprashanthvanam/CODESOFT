import tkinter as tk
from tkinter import ttk, messagebox
import random
import string

class PasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Generator")
        self.root.geometry("450x500")
        self.root.configure(bg="#e8eaf6")  # Light indigo background

        # Configure style
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Arial", 12, "bold"), padding=10)
        self.style.configure("TLabel", font=("Arial", 12), background="#e8eaf6")
        self.style.configure("TEntry", font=("Arial", 12))
        self.style.map("TButton", 
                      background=[('active', '#3f51b5')],  # Indigo on click
                      foreground=[('active', '#ffffff')])

        # GUI Components
        self.create_gui()

    def create_gui(self):
        """Create the styled GUI components."""
        main_frame = tk.Frame(self.root, bg="#e8eaf6", padx=20, pady=20)
        main_frame.pack(expand=True, fill="both")

        # Title
        tk.Label(main_frame, text="Password Generator", font=("Arial", 18, "bold"), 
                bg="#e8eaf6", fg="#1a237e").pack(pady=10)

        # Password length
        length_frame = tk.Frame(main_frame, bg="#e8eaf6")
        length_frame.pack(fill="x", pady=10)
        ttk.Label(length_frame, text="Password Length (6-50):").pack()
        self.length_entry = ttk.Entry(length_frame, width=10)
        self.length_entry.pack(pady=5)
        self.length_entry.insert(0, "12")  # Default length

        # Complexity options
        complexity_frame = tk.Frame(main_frame, bg="#e8eaf6", relief="groove", borderwidth=2)
        complexity_frame.pack(fill="x", pady=10)
        ttk.Label(complexity_frame, text="Include:").pack()

        self.upper_var = tk.BooleanVar(value=True)
        self.lower_var = tk.BooleanVar(value=True)
        self.digit_var = tk.BooleanVar(value=True)
        self.special_var = tk.BooleanVar(value=True)

        ttk.Checkbutton(complexity_frame, text="Uppercase (A-Z)", variable=self.upper_var).pack(anchor="w", padx=10)
        ttk.Checkbutton(complexity_frame, text="Lowercase (a-z)", variable=self.lower_var).pack(anchor="w", padx=10)
        ttk.Checkbutton(complexity_frame, text="Digits (0-9)", variable=self.digit_var).pack(anchor="w", padx=10)
        ttk.Checkbutton(complexity_frame, text="Special (!@#$%)", variable=self.special_var).pack(anchor="w", padx=10)

        # Generate button
        ttk.Button(main_frame, text="Generate Password", command=self.generate_password, 
                  style="TButton").pack(pady=10)

        # Result display
        self.result_var = tk.StringVar(value="Generated Password: ")
        result_label = tk.Label(main_frame, textvariable=self.result_var, 
                              font=("Arial", 12, "bold"), bg="#e8eaf6", fg="#d81b60", wraplength=400)  # Pink result text
        result_label.pack(pady=10)

        # Copy button
        ttk.Button(main_frame, text="Copy to Clipboard", command=self.copy_to_clipboard, 
                  style="TButton").pack(pady=5)

    def generate_password(self):
        """Generate a random password based on user input."""
        try:
            length = int(self.length_entry.get())
            if length < 6 or length > 50:
                messagebox.showerror("Input Error", "Length must be between 6 and 50!")
                return
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid number!")
            return

        if not (self.upper_var.get() or self.lower_var.get() or self.digit_var.get() or self.special_var.get()):
            messagebox.showerror("Input Error", "At least one character type must be selected!")
            return

        # Character sets
        characters = ""
        if self.upper_var.get():
            characters += string.ascii_uppercase
        if self.lower_var.get():
            characters += string.ascii_lowercase
        if self.digit_var.get():
            characters += string.digits
        if self.special_var.get():
            characters += string.punctuation

        # Ensure at least one character from each selected type
        password = []
        if self.upper_var.get():
            password.append(random.choice(string.ascii_uppercase))
        if self.lower_var.get():
            password.append(random.choice(string.ascii_lowercase))
        if self.digit_var.get():
            password.append(random.choice(string.digits))
        if self.special_var.get():
            password.append(random.choice(string.punctuation))

        # Fill remaining length with random characters
        remaining_length = length - len(password)
        password.extend(random.choice(characters) for _ in range(remaining_length))

        # Shuffle the password
        random.shuffle(password)
        password = ''.join(password)
        self.result_var.set(f"Generated Password: {password}")

    def copy_to_clipboard(self):
        """Copy the generated password to clipboard."""
        password = self.result_var.get().replace("Generated Password: ", "")
        if password:
            self.root.clipboard_clear()
            self.root.clipboard_append(password)
            messagebox.showinfo("Success", "Password copied to clipboard!")
        else:
            messagebox.showwarning("Error", "No password to copy!")

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGenerator(root)
    root.mainloop()