import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List Application")
        self.root.geometry("650x500")
        self.root.configure(bg="#f0f4f8")  # Light blue-gray background
        self.filename = "tasks.json"
        self.tasks = self.load_tasks()

        # Configure style
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Helvetica", 10), padding=10)
        self.style.configure("TRadiobutton", font=("Helvetica", 10))
        self.style.configure("TLabel", font=("Helvetica", 12), background="#f0f4f8")
        self.style.map("TButton", background=[('active', '#4CAF50')], foreground=[('active', '#ffffff')])

        # GUI Components
        self.create_gui()

    def load_tasks(self):
        """Load tasks from JSON file."""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as file:
                    return json.load(file)
            except json.JSONDecodeError:
                return []
        return []

    def save_tasks(self):
        """Save tasks to JSON file."""
        with open(self.filename, 'w') as file:
            json.dump(self.tasks, file, indent=4)

    def add_task(self):
        """Add a new task."""
        description = self.entry.get().strip()
        if not description:
            messagebox.showwarning("Input Error", "Task description cannot be empty!")
            return
        task = {
            'id': len(self.tasks) + 1,
            'description': description,
            'completed': False,
            'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.tasks.append(task)
        self.save_tasks()
        self.entry.delete(0, tk.END)
        self.update_task_list()

    def update_task(self):
        """Update selected task's description."""
        selected = self.task_list.curselection()
        if not selected:
            messagebox.showwarning("Selection Error", "Please select a task to update!")
            return
        task_id = int(self.task_list.get(selected[0]).split("|")[0].strip()[4:])
        new_desc = self.entry.get().strip()
        if new_desc:
            for task in self.tasks:
                if task['id'] == task_id:
                    task['description'] = new_desc
                    self.save_tasks()
                    self.entry.delete(0, tk.END)
                    self.update_task_list()
                    messagebox.showinfo("Success", f"Task {task_id} updated")
                    return
        else:
            messagebox.showwarning("Input Error", "New description cannot be empty!")

    def toggle_status(self):
        """Toggle completion status of selected task."""
        selected = self.task_list.curselection()
        if not selected:
            messagebox.showwarning("Selection Error", "Please select a task to update!")
            return
        task_id = int(self.task_list.get(selected[0]).split("|")[0].strip()[4:])
        for task in self.tasks:
            if task['id'] == task_id:
                task['completed'] = not task['completed']
                self.save_tasks()
                self.update_task_list()
                messagebox.showinfo("Success", f"Task {task_id} status updated")
                return

    def delete_task(self):
        """Delete selected task."""
        selected = self.task_list.curselection()
        if not selected:
            messagebox.showwarning("Selection Error", "Please select a task to delete!")
            return
        task_id = int(self.task_list.get(selected[0]).split("|")[0].strip()[4:])
        for i, task in enumerate(self.tasks):
            if task['id'] == task_id:
                self.tasks.pop(i)
                self.save_tasks()
                self.update_task_list()
                messagebox.showinfo("Success", f"Task {task_id} deleted")
                return

    def update_task_list(self):
        """Update the task list display."""
        self.task_list.delete(0, tk.END)
        filter_completed = self.filter_var.get()
        for task in self.tasks:
            if filter_completed == 0 or (filter_completed == 1 and not task['completed']) or (filter_completed == 2 and task['completed']):
                status = "✓" if task['completed'] else " "
                task_text = f"[{status}] ID: {task['id']} | {task['description']} | Created: {task['created_at']}"
                self.task_list.insert(tk.END, task_text)
                # Color completed tasks differently
                if task['completed']:
                    self.task_list.itemconfig(tk.END, {'fg': '#2e7d32', 'bg': '#c8e6c9'})  # Green for completed
                else:
                    self.task_list.itemconfig(tk.END, {'fg': '#37474f', 'bg': '#ffffff'})  # Dark gray text on white

    def create_gui(self):
        """Create the styled GUI components."""
        # Main frame
        main_frame = tk.Frame(self.root, bg="#f0f4f8", padx=20, pady=20)
        main_frame.pack(expand=True, fill="both")

        # Title
        tk.Label(main_frame, text="To-Do List", font=("Helvetica", 16, "bold"), bg="#f0f4f8", fg="#37474f").pack(pady=10)

        # Task input
        input_frame = tk.Frame(main_frame, bg="#f0f4f8")
        input_frame.pack(fill="x", pady=5)
        ttk.Label(input_frame, text="Task Description:").pack(side="left")
        self.entry = ttk.Entry(input_frame, width=50, font=("Helvetica", 10))
        self.entry.pack(side="left", padx=10)

        # Buttons
        button_frame = tk.Frame(main_frame, bg="#f0f4f8")
        button_frame.pack(fill="x", pady=10)
        ttk.Button(button_frame, text="Add Task", command=self.add_task, style="TButton").pack(side="left", padx=5)
        ttk.Button(button_frame, text="Update Task", command=self.update_task, style="TButton").pack(side="left", padx=5)
        ttk.Button(button_frame, text="Toggle Status", command=self.toggle_status, style="TButton").pack(side="left", padx=5)
        ttk.Button(button_frame, text="Delete Task", command=self.delete_task, style="TButton").pack(side="left", padx=5)

        # Filter options
        filter_frame = tk.Frame(main_frame, bg="#f0f4f8", relief="groove", borderwidth=2)
        filter_frame.pack(fill="x", pady=10)
        self.filter_var = tk.IntVar(value=0)
        ttk.Radiobutton(filter_frame, text="All Tasks", variable=self.filter_var, value=0, command=self.update_task_list).pack(side="left", padx=10)
        ttk.Radiobutton(filter_frame, text="Pending", variable=self.filter_var, value=1, command=self.update_task_list).pack(side="left", padx=10)
        ttk.Radiobutton(filter_frame, text="Completed", variable=self.filter_var, value=2, command=self.update_task_list).pack(side="left", padx=10)

        # Task list with scrollbar
        list_frame = tk.Frame(main_frame, bg="#f0f4f8")
        list_frame.pack(fill="both", expand=True, pady=10)
        self.task_list = tk.Listbox(list_frame, width=80, height=15, font=("Helvetica", 10), bg="#ffffff", fg="#37474f", selectbackground="#90caf9", selectforeground="#000000")
        self.task_list.pack(side="left", fill="both", expand=True)
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.task_list.yview)
        scrollbar.pack(side="right", fill="y")
        self.task_list.config(yscrollcommand=scrollbar.set)
        self.update_task_list()

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()