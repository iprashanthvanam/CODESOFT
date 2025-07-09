import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import re

class ContactBook:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Book")
        self.root.geometry("700x500")
        self.root.configure(bg="#e0f7fa")  # Light cyan background

        # Contact storage
        self.filename = "contacts.json"
        self.contacts = self.load_contacts()

        # Configure style
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Arial", 11, "bold"), padding=8)
        self.style.configure("TLabel", font=("Arial", 11), background="#e0f7fa")
        self.style.configure("TEntry", font=("Arial", 11))
        self.style.map("TButton", 
                      background=[('active', '#0288d1')],  # Blue on click
                      foreground=[('active', '#ffffff')])

        # GUI Components
        self.create_gui()

    def load_contacts(self):
        """Load contacts from JSON file."""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as file:
                    return json.load(file)
            except json.JSONDecodeError:
                return []
        return []

    def save_contacts(self):
        """Save contacts to JSON file."""
        with open(self.filename, 'w') as file:
            json.dump(self.contacts, file, indent=4)

    def add_contact(self):
        """Add a new contact."""
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        email = self.email_entry.get().strip()
        address = self.address_entry.get().strip()

        if not name or not phone:
            messagebox.showwarning("Input Error", "Name and phone number are required!")
            return
        if not re.match(r'^\+?\d{10,15}$', phone.replace(" ", "")):
            messagebox.showwarning("Input Error", "Invalid phone number! Use 10-15 digits, optionally starting with +.")
            return
        if email and not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            messagebox.showwarning("Input Error", "Invalid email format!")
            return

        contact = {
            'id': len(self.contacts) + 1,
            'name': name,
            'phone': phone,
            'email': email,
            'address': address
        }
        self.contacts.append(contact)
        self.save_contacts()
        self.clear_entries()
        self.update_contact_list()
        messagebox.showinfo("Success", f"Contact {name} added!")

    def update_contact(self):
        """Update selected contact's details."""
        selected = self.contact_list.curselection()
        if not selected:
            messagebox.showwarning("Selection Error", "Please select a contact to update!")
            return
        contact_id = int(self.contact_list.get(selected[0]).split("|")[0].strip()[4:])
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        email = self.email_entry.get().strip()
        address = self.address_entry.get().strip()

        if not name or not phone:
            messagebox.showwarning("Input Error", "Name and phone number are required!")
            return
        if not re.match(r'^\+?\d{10,15}$', phone.replace(" ", "")):
            messagebox.showwarning("Input Error", "Invalid phone number! Use 10-15 digits, optionally starting with +.")
            return
        if email and not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            messagebox.showwarning("Input Error", "Invalid email format!")
            return

        for contact in self.contacts:
            if contact['id'] == contact_id:
                contact['name'] = name
                contact['phone'] = phone
                contact['email'] = email
                contact['address'] = address
                self.save_contacts()
                self.clear_entries()
                self.update_contact_list()
                messagebox.showinfo("Success", f"Contact {name} updated!")
                return

    def delete_contact(self):
        """Delete selected contact."""
        selected = self.contact_list.curselection()
        if not selected:
            messagebox.showwarning("Selection Error", "Please select a contact to delete!")
            return
        contact_id = int(self.contact_list.get(selected[0]).split("|")[0].strip()[4:])
        for i, contact in enumerate(self.contacts):
            if contact['id'] == contact_id:
                name = contact['name']
                self.contacts.pop(i)
                self.save_contacts()
                self.clear_entries()
                self.update_contact_list()
                messagebox.showinfo("Success", f"Contact {name} deleted!")
                return

    def search_contacts(self):
        """Search contacts by name or phone."""
        query = self.search_entry.get().strip().lower()
        self.contact_list.delete(0, tk.END)
        for contact in self.contacts:
            if query in contact['name'].lower() or query in contact['phone'].lower():
                self.contact_list.insert(tk.END, 
                    f"[ID: {contact['id']}] | Name: {contact['name']} | Phone: {contact['phone']}")

    def update_contact_list(self):
        """Update the contact list display."""
        self.contact_list.delete(0, tk.END)
        for contact in self.contacts:
            self.contact_list.insert(tk.END, 
                f"[ID: {contact['id']}] | Name: {contact['name']} | Phone: {contact['phone']}")
            self.contact_list.itemconfig(tk.END, {'fg': '#37474f', 'bg': '#ffffff'})  # Dark gray text on white

    def clear_entries(self):
        """Clear all input fields."""
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)
        self.search_entry.delete(0, tk.END)

    def select_contact(self, event):
        """Populate input fields when a contact is selected."""
        selected = self.contact_list.curselection()
        if selected:
            contact_id = int(self.contact_list.get(selected[0]).split("|")[0].strip()[4:])
            for contact in self.contacts:
                if contact['id'] == contact_id:
                    self.clear_entries()
                    self.name_entry.insert(0, contact['name'])
                    self.phone_entry.insert(0, contact['phone'])
                    self.email_entry.insert(0, contact['email'])
                    self.address_entry.insert(0, contact['address'])
                    break

    def create_gui(self):
        """Create the styled GUI components."""
        main_frame = tk.Frame(self.root, bg="#e0f7fa", padx=20, pady=20)
        main_frame.pack(expand=True, fill="both")

        # Title
        tk.Label(main_frame, text="Contact Book", font=("Arial", 18, "bold"), 
                bg="#e0f7fa", fg="#006064").pack(pady=10)

        # Input fields
        input_frame = tk.Frame(main_frame, bg="#e0f7fa")
        input_frame.pack(fill="x", pady=10)
        fields = [("Name:", "name_entry"), ("Phone:", "phone_entry"), 
                 ("Email:", "email_entry"), ("Address:", "address_entry")]
        for label, attr in fields:
            ttk.Label(input_frame, text=label).pack(anchor="w")
            setattr(self, attr, ttk.Entry(input_frame, width=30))
            getattr(self, attr).pack(pady=2)

        # Buttons
        button_frame = tk.Frame(main_frame, bg="#e0f7fa")
        button_frame.pack(fill="x", pady=10)
        ttk.Button(button_frame, text="Add Contact", command=self.add_contact).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Update Contact", command=self.update_contact).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Delete Contact", command=self.delete_contact).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Clear", command=self.clear_entries).pack(side="left", padx=5)

        # Search
        search_frame = tk.Frame(main_frame, bg="#e0f7fa", relief="groove", borderwidth=2)
        search_frame.pack(fill="x", pady=10)
        ttk.Label(search_frame, text="Search by Name/Phone:").pack(side="left")
        self.search_entry = ttk.Entry(search_frame, width=20)
        self.search_entry.pack(side="left", padx=5)
        self.search_entry.bind("<KeyRelease>", lambda event: self.search_contacts())

        # Contact list with scrollbar
        list_frame = tk.Frame(main_frame, bg="#e0f7fa")
        list_frame.pack(fill="both", expand=True, pady=10)
        self.contact_list = tk.Listbox(list_frame, width=60, height=10, font=("Arial", 11), 
                                    bg="#ffffff", fg="#37474f", selectbackground="#80deea")
        self.contact_list.pack(side="left", fill="both", expand=True)
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.contact_list.yview)
        scrollbar.pack(side="right", fill="y")
        self.contact_list.config(yscrollcommand=scrollbar.set)
        self.contact_list.bind('<<ListboxSelect>>', self.select_contact)
        self.update_contact_list()

if __name__ == "__main__":
    root = tk.Tk()
    app = ContactBook(root)
    root.mainloop()