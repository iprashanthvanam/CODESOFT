import tkinter as tk
from tkinter import ttk, messagebox

class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Calculator")
        self.root.geometry("400x500")
        self.root.configure(bg="#e3f2fd")  # Light blue background

        # Configure style
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Arial", 12, "bold"), padding=10)
        self.style.configure("TLabel", font=("Arial", 14), background="#e3f2fd")
        self.style.configure("TEntry", font=("Arial", 12))
        self.style.map("TButton", 
                      background=[('active', '#0288d1')],  # Blue on click
                      foreground=[('active', '#ffffff')])

        # GUI Components
        self.create_gui()

    def create_gui(self):
        """Create the styled GUI components."""
        main_frame = tk.Frame(self.root, bg="#e3f2fd", padx=20, pady=20)
        main_frame.pack(expand=True, fill="both")

        # Title
        tk.Label(main_frame, text="Simple Calculator", font=("Arial", 18, "bold"), 
                bg="#e3f2fd", fg="#01579b").pack(pady=10)

        # Number inputs
        input_frame = tk.Frame(main_frame, bg="#e3f2fd")
        input_frame.pack(fill="x", pady=10)
        
        ttk.Label(input_frame, text="First Number:").pack()
        self.num1_entry = ttk.Entry(input_frame, width=20)
        self.num1_entry.pack(pady=5)

        ttk.Label(input_frame, text="Second Number:").pack()
        self.num2_entry = ttk.Entry(input_frame, width=20)
        self.num2_entry.pack(pady=5)

        # Operation selection
        operation_frame = tk.Frame(main_frame, bg="#e3f2fd", relief="groove", borderwidth=2)
        operation_frame.pack(fill="x", pady=10)
        ttk.Label(operation_frame, text="Select Operation:").pack()
        
        self.operation_var = tk.StringVar(value="+")
        operations = [
            ("Addition (+)", "+"),
            ("Subtraction (-)", "-"),
            ("Multiplication (×)", "*"),
            ("Division (÷)", "/")
        ]
        for text, value in operations:
            ttk.Radiobutton(operation_frame, text=text, variable=self.operation_var, 
                           value=value, style="TRadiobutton").pack(side="left", padx=10)

        # Calculate button
        ttk.Button(main_frame, text="Calculate", command=self.calculate, 
                  style="TButton").pack(pady=10)

        # Result display
        self.result_var = tk.StringVar(value="Result: ")
        result_label = tk.Label(main_frame, textvariable=self.result_var, 
                              font=("Arial", 14, "bold"), bg="#e3f2fd", fg="#d32f2f")  # Red result text
        result_label.pack(pady=10)

        # Clear button
        ttk.Button(main_frame, text="Clear", command=self.clear, 
                  style="TButton").pack(pady=5)

    def calculate(self):
        """Perform the selected arithmetic operation."""
        try:
            num1 = float(self.num1_entry.get())
            num2 = float(self.num2_entry.get())
            operation = self.operation_var.get()

            if operation == "+":
                result = num1 + num2
            elif operation == "-":
                result = num1 - num2
            elif operation == "*":
                result = num1 * num2
            elif operation == "/":
                if num2 == 0:
                    messagebox.showerror("Error", "Division by zero is not allowed!")
                    return
                result = num1 / num2
            else:
                messagebox.showerror("Error", "Invalid operation!")
                return

            self.result_var.set(f"Result: {result:.2f}")
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def clear(self):
        """Clear input fields and result."""
        self.num1_entry.delete(0, tk.END)
        self.num2_entry.delete(0, tk.END)
        self.operation_var.set("+")
        self.result_var.set("Result: ")

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()