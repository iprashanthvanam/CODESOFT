import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import numpy as np
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

class IrisFlowerClassifier:
    def __init__(self, root):
        self.root = root
        self.root.title("Iris Flower Classifier")
        self.root.geometry("500x500")
        self.root.configure(bg="#e1f5fe")  # Light blue background

        # Load and train model
        self.model, self.scaler, self.species = self.train_model()

        # Configure style
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Arial", 12, "bold"), padding=10)
        self.style.configure("TLabel", font=("Arial", 12), background="#e1f5fe")
        self.style.configure("TEntry", font=("Arial", 12))
        self.style.map("TButton", 
                      background=[('active', '#0288d1')],  # Blue on click
                      foreground=[('active', '#ffffff')])

        # GUI Components
        self.create_gui()

    def train_model(self):
        """Load Iris dataset and train Random Forest model."""
        try:
            # Load Iris dataset
            iris = load_iris()
            X = pd.DataFrame(iris.data, columns=iris.feature_names)
            y = iris.target
            species = iris.target_names  # ['setosa', 'versicolor', 'virginica']

            # Split data
            X_train, _, y_train, _ = train_test_split(X, y, test_size=0.2, random_state=42)

            # Scale features
            scaler = StandardScaler()
            X_train = scaler.fit_transform(X_train)

            # Train Random Forest Classifier
            model = RandomForestClassifier(n_estimators=100, random_state=42)
            model.fit(X_train, y_train)

            return model, scaler, species
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load/train model: {str(e)}")
            return None, None, None

    def create_gui(self):
        """Create the styled GUI components."""
        if self.model is None or self.scaler is None:
            return

        main_frame = tk.Frame(self.root, bg="#e1f5fe", padx=20, pady=20)
        main_frame.pack(expand=True, fill="both")

        # Title
        tk.Label(main_frame, text="Iris Flower Classifier", font=("Arial", 18, "bold"), 
                bg="#e1f5fe", fg="#01579b").pack(pady=10)

        # Input fields
        input_frame = tk.Frame(main_frame, bg="#e1f5fe")
        input_frame.pack(fill="x", pady=10)

        fields = [
            ("Sepal Length (cm)", "sepal_length_entry"),
            ("Sepal Width (cm)", "sepal_width_entry"),
            ("Petal Length (cm)", "petal_length_entry"),
            ("Petal Width (cm)", "petal_width_entry")
        ]
        for label, attr in fields:
            ttk.Label(input_frame, text=label).pack(anchor="w")
            setattr(self, attr, ttk.Entry(input_frame, width=20))
            getattr(self, attr).pack(pady=2)

        # Predict button
        ttk.Button(main_frame, text="Predict Species", command=self.predict, 
                  style="TButton").pack(pady=10)

        # Result display
        self.result_var = tk.StringVar(value="Enter measurements and click Predict")
        result_label = tk.Label(main_frame, textvariable=self.result_var, 
                              font=("Arial", 12, "bold"), bg="#e1f5fe", fg="#d32f2f", wraplength=400)
        result_label.pack(pady=10)

        # Clear button
        ttk.Button(main_frame, text="Clear", command=self.clear_entries, 
                  style="TButton").pack(pady=5)

    def predict(self):
        """Predict Iris species based on user input."""
        try:
            sepal_length = float(self.sepal_length_entry.get())
            if sepal_length <= 0:
                raise ValueError("Sepal Length must be positive")
            sepal_width = float(self.sepal_width_entry.get())
            if sepal_width <= 0:
                raise ValueError("Sepal Width must be positive")
            petal_length = float(self.petal_length_entry.get())
            if petal_length <= 0:
                raise ValueError("Petal Length must be positive")
            petal_width = float(self.petal_width_entry.get())
            if petal_width <= 0:
                raise ValueError("Petal Width must be positive")

            # Prepare input data
            input_data = np.array([[sepal_length, sepal_width, petal_length, petal_width]])
            input_data = self.scaler.transform(input_data)

            # Predict
            prediction = self.model.predict(input_data)[0]
            probabilities = self.model.predict_proba(input_data)[0]
            species = self.species[prediction]
            prob = probabilities[prediction] * 100

            self.result_var.set(f"Predicted Species: {species.capitalize()}\nConfidence: {prob:.2f}%")
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def clear_entries(self):
        """Clear all input fields."""
        for attr in ['sepal_length_entry', 'sepal_width_entry', 'petal_length_entry', 'petal_width_entry']:
            getattr(self, attr).delete(0, tk.END)
        self.result_var.set("Enter measurements and click Predict")

if __name__ == "__main__":
    root = tk.Tk()
    app = IrisFlowerClassifier(root)
    root.mainloop()