import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import os
import random

class MovieRatingPredictor:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Rating Predictor")
        self.root.geometry("500x600")
        self.root.configure(bg="#e8f5e9")  # Light green background

        # Sample categories for synthetic data or dropdowns
        self.genres = ['Action', 'Comedy', 'Drama', 'Sci-Fi', 'Romance']
        self.directors = ['Spielberg', 'Nolan', 'Tarantino', 'Wong', 'Cameron']
        self.actors = ['DiCaprio', 'Streep', 'Cruise', 'Johansson', 'Hanks']

        # Load and train model
        self.model, self.scaler, self.feature_columns = self.train_model()

        # Configure style
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Arial", 12, "bold"), padding=10)
        self.style.configure("TLabel", font=("Arial", 12), background="#e8f5e9")
        self.style.configure("TCombobox", font=("Arial", 12))
        self.style.map("TButton", 
                      background=[('active', '#388e3c')],  # Green on click
                      foreground=[('active', '#ffffff')])

        # GUI Components
        self.create_gui()

    def train_model(self):
        """Load or generate dataset and train Random Forest model."""
        try:
            # Check for dataset
            file_path = "movies.csv"
            if not os.path.exists(file_path):
                messagebox.showinfo("Info", "movies.csv not found! Generating synthetic dataset.")
                df = self.generate_synthetic_data()
            else:
                df = pd.read_csv(file_path)

            # Select features and target
            features = ['Genre', 'Director', 'Actor1', 'Actor2', 'Year', 'Runtime']
            X = df[features]
            y = df['Rating']

            # Preprocess data: Encode categorical variables
            X = pd.get_dummies(X, columns=['Genre', 'Director', 'Actor1', 'Actor2'], drop_first=True)
            feature_columns = X.columns.tolist()

            # Handle missing values
            X.loc[:, 'Year'] = X['Year'].fillna(X['Year'].median())
            X.loc[:, 'Runtime'] = X['Runtime'].fillna(X['Runtime'].median())

            # Split data
            X_train, _, y_train, _ = train_test_split(X, y, test_size=0.2, random_state=42)

            # Scale numerical features
            scaler = StandardScaler()
            X_train[['Year', 'Runtime']] = scaler.fit_transform(X_train[['Year', 'Runtime']])

            # Train Random Forest Regressor
            model = RandomForestRegressor(n_estimators=100, random_state=42)
            model.fit(X_train, y_train)

            return model, scaler, feature_columns
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load/train model: {str(e)}")
            return None, None, None

    def generate_synthetic_data(self):
        """Generate a synthetic dataset for demonstration."""
        data = {
            'Genre': [random.choice(self.genres) for _ in range(1000)],
            'Director': [random.choice(self.directors) for _ in range(1000)],
            'Actor1': [random.choice(self.actors) for _ in range(1000)],
            'Actor2': [random.choice(self.actors) for _ in range(1000)],
            'Year': [random.randint(1980, 2023) for _ in range(1000)],
            'Runtime': [random.randint(80, 180) for _ in range(1000)],
            'Rating': [random.uniform(1, 10) for _ in range(1000)]
        }
        df = pd.DataFrame(data)
        df.to_csv("movies.csv", index=False)
        return df

    def create_gui(self):
        """Create the styled GUI components."""
        if self.model is None or self.scaler is None:
            return

        main_frame = tk.Frame(self.root, bg="#e8f5e9", padx=20, pady=20)
        main_frame.pack(expand=True, fill="both")

        # Title
        tk.Label(main_frame, text="Movie Rating Predictor", font=("Arial", 18, "bold"), 
                bg="#e8f5e9", fg="#2e7d32").pack(pady=10)

        # Input fields
        input_frame = tk.Frame(main_frame, bg="#e8f5e9")
        input_frame.pack(fill="x", pady=10)

        # Dropdowns and entries
        fields = [
            ("Genre", "genre_combo", self.genres, tk.StringVar),
            ("Director", "director_combo", self.directors, tk.StringVar),
            ("Actor 1", "actor1_combo", self.actors, tk.StringVar),
            ("Actor 2", "actor2_combo", self.actors, tk.StringVar),
            ("Year (e.g., 2020)", "year_entry", None, None),
            ("Runtime (minutes, e.g., 120)", "runtime_entry", None, None)
        ]
        for label, attr, values, var_type in fields:
            ttk.Label(input_frame, text=label).pack(anchor="w")
            if values:  # Combobox for categorical inputs
                var = var_type()
                setattr(self, f"{attr}_var", var)
                combo = ttk.Combobox(input_frame, textvariable=var, values=values, width=20, state="readonly")
                combo.pack(pady=2)
                combo.set(values[0])  # Default to first option
            else:  # Entry for numerical inputs
                setattr(self, attr, ttk.Entry(input_frame, width=20))
                getattr(self, attr).pack(pady=2)

        # Predict button
        ttk.Button(main_frame, text="Predict Rating", command=self.predict, 
                  style="TButton").pack(pady=10)

        # Result display
        self.result_var = tk.StringVar(value="Enter details and click Predict")
        result_label = tk.Label(main_frame, textvariable=self.result_var, 
                              font=("Arial", 12, "bold"), bg="#e8f5e9", fg="#d81b60", wraplength=400)
        result_label.pack(pady=10)

        # Clear button
        ttk.Button(main_frame, text="Clear", command=self.clear_entries, 
                  style="TButton").pack(pady=5)

    def predict(self):
        """Predict movie rating based on user input."""
        try:
            genre = self.genre_combo_var.get()
            director = self.director_combo_var.get()
            actor1 = self.actor1_combo_var.get()
            actor2 = self.actor2_combo_var.get()
            year = int(self.year_entry.get())
            if year < 1888 or year > 2025:
                raise ValueError("Year must be between 1888 and 2025")
            runtime = int(self.runtime_entry.get())
            if runtime < 1:
                raise ValueError("Runtime must be positive")

            # Prepare input data
            input_data = pd.DataFrame({
                'Genre': [genre],
                'Director': [director],
                'Actor1': [actor1],
                'Actor2': [actor2],
                'Year': [year],
                'Runtime': [runtime]
            })

            # Encode categorical variables
            input_data = pd.get_dummies(input_data, columns=['Genre', 'Director', 'Actor1', 'Actor2'], drop_first=True)

            # Align columns with training data
            for col in self.feature_columns:
                if col not in input_data.columns:
                    input_data[col] = 0
            input_data = input_data[self.feature_columns]

            # Scale numerical features
            input_data[['Year', 'Runtime']] = self.scaler.transform(input_data[['Year', 'Runtime']])

            # Predict
            prediction = self.model.predict(input_data)[0]
            prediction = max(1, min(10, prediction))  # Clip to 1-10 range
            self.result_var.set(f"Predicted Rating: {prediction:.1f}/10")
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def clear_entries(self):
        """Clear all input fields."""
        self.genre_combo_var.set(self.genres[0])
        self.director_combo_var.set(self.directors[0])
        self.actor1_combo_var.set(self.actors[0])
        self.actor2_combo_var.set(self.actors[0])
        self.year_entry.delete(0, tk.END)
        self.runtime_entry.delete(0, tk.END)
        self.result_var.set("Enter details and click Predict")

if __name__ == "__main__":
    root = tk.Tk()
    app = MovieRatingPredictor(root)
    root.mainloop()