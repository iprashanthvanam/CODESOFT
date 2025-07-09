import tkinter as tk
from tkinter import ttk, messagebox
import random

class RockPaperScissors:
    def __init__(self, root):
        self.root = root
        self.root.title("Rock Paper Scissors")
        self.root.geometry("500x400")
        self.root.configure(bg="#e1f5fe")  # Light blue background

        # Score tracking
        self.user_score = 0
        self.computer_score = 0

        # Configure style
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Arial", 12, "bold"), padding=10)
        self.style.configure("TLabel", font=("Arial", 12), background="#e1f5fe")
        self.style.map("TButton", 
                      background=[('active', '#0288d1')],  # Blue on click
                      foreground=[('active', '#ffffff')])

        # GUI Components
        self.create_gui()

    def create_gui(self):
        """Create the styled GUI components."""
        main_frame = tk.Frame(self.root, bg="#e1f5fe", padx=20, pady=20)
        main_frame.pack(expand=True, fill="both")

        # Title
        tk.Label(main_frame, text="Rock Paper Scissors", font=("Arial", 18, "bold"), 
                bg="#e1f5fe", fg="#01579b").pack(pady=10)

        # Choice buttons
        choice_frame = tk.Frame(main_frame, bg="#e1f5fe", relief="groove", borderwidth=2)
        choice_frame.pack(fill="x", pady=10)
        ttk.Button(choice_frame, text="Rock", command=lambda: self.play("rock")).pack(side="left", padx=10)
        ttk.Button(choice_frame, text="Paper", command=lambda: self.play("paper")).pack(side="left", padx=10)
        ttk.Button(choice_frame, text="Scissors", command=lambda: self.play("scissors")).pack(side="left", padx=10)

        # Result display
        self.result_var = tk.StringVar(value="Make your choice!")
        result_label = tk.Label(main_frame, textvariable=self.result_var, 
                              font=("Arial", 12, "bold"), bg="#e1f5fe", fg="#d32f2f")  # Red result text
        result_label.pack(pady=10)

        # Score display
        self.score_var = tk.StringVar(value=f"Score - You: {self.user_score} | Computer: {self.computer_score}")
        score_label = tk.Label(main_frame, textvariable=self.score_var, 
                              font=("Arial", 12), bg="#e1f5fe", fg="#388e3c")  # Green score text
        score_label.pack(pady=5)

        # Play again and quit buttons
        button_frame = tk.Frame(main_frame, bg="#e1f5fe")
        button_frame.pack(pady=10)
        ttk.Button(button_frame, text="Play Again", command=self.reset_round).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Quit", command=self.quit_game).pack(side="left", padx=5)

    def play(self, user_choice):
        """Handle game logic and update display."""
        choices = ["rock", "paper", "scissors"]
        computer_choice = random.choice(choices)

        # Determine winner
        if user_choice == computer_choice:
            result = "It's a tie!"
        elif (user_choice == "rock" and computer_choice == "scissors") or \
             (user_choice == "paper" and computer_choice == "rock") or \
             (user_choice == "scissors" and computer_choice == "paper"):
            result = f"You win! {user_choice.capitalize()} beats {computer_choice.capitalize()}."
            self.user_score += 1
        else:
            result = f"You lose! {computer_choice.capitalize()} beats {user_choice.capitalize()}."
            self.computer_score += 1

        # Update display
        self.result_var.set(f"You chose: {user_choice.capitalize()} | Computer chose: {computer_choice.capitalize()}\n{result}")
        self.score_var.set(f"Score - You: {self.user_score} | Computer: {self.computer_score}")

    def reset_round(self):
        """Reset for a new round."""
        self.result_var.set("Make your choice!")
        self.score_var.set(f"Score - You: {self.user_score} | Computer: {self.computer_score}")

    def quit_game(self):
        """Quit the game with a confirmation."""
        if messagebox.askyesno("Quit", "Are you sure you want to quit?"):
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = RockPaperScissors(root)
    root.mainloop()