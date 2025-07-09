import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import os
import random

class SalesPredictor:
    def __init__(self, root):
        self.root = root
        self.root.title("Sales Predictor")
        self.root.geometry("500x600")
        self.root.configure(bg="#f3e5f5")  # Light purple background

        # Sample categories for synthetic data or dropdowns
        self.age_groups = ['Young', 'Adult', 'Senior']
        self.platforms = ['TV', 'Social Media', 'Print', 'Online']

        # Load and train model
        self.model, self.scaler, self.feature_columns = self.train_model()

        # Configure style
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Arial", 12, "bold"), padding=10)
        self.style.configure("TLabel", font=("Arial", 12), background="#f3e5f5")
        self.style.configure("TCombobox", font=("Arial", 12))
        self.style.map("TButton", 
                      background=[('active', '#7b1fa2')],  # Purple on click
                      foreground=[('active', '#ffffff')])

        # GUI Components
        self.create_gui()

    def train_model(self):
        """Load or generate dataset and train Random Forest model."""
        try:
            # Check for dataset
            file_path = "sales.csv"
            if not os.path.exists(file_path):
                messagebox.showinfo("Info", "sales.csv not found! Generating synthetic dataset.")
                df = self.generate_synthetic_data()
            else:
                df = pd.read_csv(file_path)

            # Select features and target
            features = ['TV', 'Radio', 'Newspaper', 'AgeGroup', 'Platform']
            X = df[features]
            y = df['Sales']

            # Preprocess data: Encode categorical variables
            X = pd.get_dummies(X, columns=['AgeGroup', 'Platform'], drop_first=True)
            feature_columns = X.columns.tolist()

            # Handle missing values
            for col in ['TV', 'Radio', 'Newspaper']:
                X.loc[:, col] = X[col].fillna(X[col].median())

            # Split data
            X_train, _, y_train, _ = train_test_split(X, y, test_size=0.2, random_state=42)

            # Scale numerical features
            scaler = StandardScaler()
            X_train[['TV', 'Radio', 'Newspaper']] = scaler.fit_transform(X_train[['TV', 'Radio', 'Newspaper']])

            # Train Random Forest Regressor
            model = RandomForestRegressor(n_estimators=100, random_state=42)
            model.fit(X_train, y_train)

            return model, scaler, feature_columns
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load/train model: {str(e)}")
            return None, None, None

    def generate_synthetic_data(self):
        """Generate a synthetic dataset in INR for demonstration."""
        data = {
            'TV': [random.uniform(100000, 3000000) for _ in range(1000)],  # Ad spend in rupees (1-30 lakhs)
            'Radio': [random.uniform(0, 1000000) for _ in range(1000)],  # 0-10 lakhs
            'Newspaper': [random.uniform(0, 800000) for _ in range(1000)],  # 0-8 lakhs
            'AgeGroup': [random.choice(self.age_groups) for _ in range(1000)],
            'Platform': [random.choice(self.platforms) for _ in range(1000)],
            'Sales': [random.uniform(100000, 5000000) for _ in range(1000)]  # Sales in rupees (1-50 lakhs)
        }
        df = pd.DataFrame(data)
        # Add some correlation to make the model realistic
        df['Sales'] = (0.4 * df['TV'] * 0.00001 + 0.3 * df['Radio'] * 0.00001 + 0.2 * df['Newspaper'] * 0.00001 + 
                       np.random.normal(0, 50000, 1000))
        df['Sales'] = df['Sales'].clip(100000, 5000000)  # Keep sales in range
        df.to_csv("sales.csv", index=False)
        return df

    def create_gui(self):
        """Create the styled GUI components."""
        if self.model is None or self.scaler is None:
            return

        main_frame = tk.Frame(self.root, bg="#f3e5f5", padx=20, pady=20)
        main_frame.pack(expand=True, fill="both")

        # Title
        tk.Label(main_frame, text="Sales Predictor", font=("Arial", 18, "bold"), 
                bg="#f3e5f5", fg="#4a148c").pack(pady=10)

        # Input fields
        input_frame = tk.Frame(main_frame, bg="#f3e5f5")
        input_frame.pack(fill="x", pady=10)

        # Dropdowns and entries
        fields = [
            ("TV Ad Spend (₹)", "tv_entry", None, None),
            ("Radio Ad Spend (₹)", "radio_entry", None, None),
            ("Newspaper Ad Spend (₹)", "newspaper_entry", None, None),
            ("Target Age Group", "age_group_combo", self.age_groups, tk.StringVar),
            ("Advertising Platform", "platform_combo", self.platforms, tk.StringVar)
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
        ttk.Button(main_frame, text="Predict Sales", command=self.predict, 
                  style="TButton").pack(pady=10)

        # Result display
        self.result_var = tk.StringVar(value="Enter details and click Predict")
        result_label = tk.Label(main_frame, textvariable=self.result_var, 
                              font=("Arial", 12, "bold"), bg="#f3e5f5", fg="#d81b60", wraplength=400)
        result_label.pack(pady=10)

        # Clear button
        ttk.Button(main_frame, text="Clear", command=self.clear_entries, 
                  style="TButton").pack(pady=5)

    def predict(self):
        """Predict sales based on user input."""
        try:
            tv = float(self.tv_entry.get())
            if tv < 0:
                raise ValueError("TV Ad Spend must be non-negative")
            radio = float(self.radio_entry.get())
            if radio < 0:
                raise ValueError("Radio Ad Spend must be non-negative")
            newspaper = float(self.newspaper_entry.get())
            if newspaper < 0:
                raise ValueError("Newspaper Ad Spend must be non-negative")
            age_group = self.age_group_combo_var.get()
            platform = self.platform_combo_var.get()

            # Prepare input data
            input_data = pd.DataFrame({
                'TV': [tv],
                'Radio': [radio],
                'Newspaper': [newspaper],
                'AgeGroup': [age_group],
                'Platform': [platform]
            })

            # Encode categorical variables
            input_data = pd.get_dummies(input_data, columns=['AgeGroup', 'Platform'], drop_first=True)

            # Align columns with training data
            for col in self.feature_columns:
                if col not in input_data.columns:
                    input_data[col] = 0
            input_data = input_data[self.feature_columns]

            # Scale numerical features
            input_data[['TV', 'Radio', 'Newspaper']] = self.scaler.transform(input_data[['TV', 'Radio', 'Newspaper']])

            # Predict
            prediction = self.model.predict(input_data)[0]
            prediction = max(100000, prediction)  # Ensure minimum sales of 1 lakh
            self.result_var.set(f"Predicted Sales: ₹{prediction:,.2f}")
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def clear_entries(self):
        """Clear all input fields."""
        for attr in ['tv_entry', 'radio_entry', 'newspaper_entry']:
            getattr(self, attr).delete(0, tk.END)
        self.age_group_combo_var.set(self.age_groups[0])
        self.platform_combo_var.set(self.platforms[0])
        self.result_var.set("Enter details and click Predict")

if __name__ == "__main__":
    root = tk.Tk()
    app = SalesPredictor(root)
    root.mainloop()