import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import re

class CustomerApp:
    def __init__(self, root):
        """
        Initialize the application window, database, and UI widgets.
        """
        self.root = root
        self.root.title("Customer Information Management System")
        self.root.geometry("450x400") # Set a default size for the window
        self.root.columnconfigure(1, weight=1) # Allow the entry column to expand

        # --- Database Setup ---
        self.setup_database()

        # --- UI Creation ---
        self.create_widgets()

    def setup_database(self):
        """
        Connects to the SQLite database and creates the 'customers' table
        if it doesn't already exist.
        """
        try:
            # Create or connect to a database file named 'customers.db'
            conn = sqlite3.connect('customers.db')
            cursor = conn.cursor()

            # Create the table with the required fields
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS customers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    birthday TEXT,
                    email TEXT NOT NULL,
                    phone TEXT,
                    address TEXT,
                    contact_method TEXT
                )
            ''')
            conn.commit()
        except sqlite3.Error as e:
            # Show an error message if the database can't be set up
            messagebox.showerror("Database Error", f"An error occurred: {e}")
            self.root.destroy() # Close the app if DB fails
        finally:
            if conn:
                conn.close()

    def create_widgets(self):
        """
        Creates and arranges all the GUI elements (labels, entry fields, etc.).
        """
        # Use a frame for better organization and padding
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- Input Fields and Labels ---
        fields = {
            "Name:": "name_entry",
            "Birthday (YYYY-MM-DD):": "birthday_entry",
            "Email:": "email_entry",
            "Phone Number:": "phone_entry",
            "Address:": "address_entry"
        }

        # Create and place labels and entry widgets in a loop
        for i, (text, attr_name) in enumerate(fields.items()):
            label = ttk.Label(main_frame, text=text)
            label.grid(row=i, column=0, sticky=tk.W, padx=5, pady=5)
            
            entry = ttk.Entry(main_frame, width=40)
            entry.grid(row=i, column=1, sticky=tk.EW, padx=5, pady=5)
            setattr(self, attr_name, entry) # Dynamically create self.name_entry, etc.

        # --- Preferred Contact Method Dropdown ---
        contact_label = ttk.Label(main_frame, text="Preferred Contact Method:")
        contact_label.grid(row=5, column=0, sticky=tk.W, padx=5, pady=5)

        self.contact_method_var = tk.StringVar()
        contact_options = ["Email", "Phone", "Mail"]
        self.contact_method_menu = ttk.Combobox(
            main_frame,
            textvariable=self.contact_method_var,
            values=contact_options,
            state="readonly" # Prevents user from typing a custom value
        )
        self.contact_method_menu.grid(row=5, column=1, sticky=tk.EW, padx=5, pady=5)
        self.contact_method_menu.set(contact_options[0]) # Set default value

        # --- Submit Button ---
        submit_button = ttk.Button(
            main_frame,
            text="Submit",
            command=self.submit_data
        )
        # Place the button below the fields, spanning both columns
        submit_button.grid(row=6, column=0, columnspan=2, pady=20)

    def is_valid_email(self, email):
        """
        A simple regex check to validate the email format.
        """
        # This is a basic regex, can be improved for more complex cases
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return re.match(pattern, email)

    def submit_data(self):
        """
        Handles the logic for the submit button click.
        Validates input, saves to the database, and clears the form.
        """
        # --- Retrieve Data from Fields ---
        name = self.name_entry.get().strip()
        birthday = self.birthday_entry.get().strip()
        email = self.email_entry.get().strip()
        phone = self.phone_entry.get().strip()
        address = self.address_entry.get().strip()
        contact_method = self.contact_method_var.get()

        # --- Data Validation ---
        if not name or not email:
            messagebox.showwarning("Validation Error", "Name and Email are required fields.")
            return

        if not self.is_valid_email(email):
            messagebox.showwarning("Validation Error", "Please enter a valid email address.")
            return
        
        # --- Store in Database ---
        try:
            conn = sqlite3.connect('customers.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO customers (name, birthday, email, phone, address, contact_method)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (name, birthday, email, phone, address, contact_method))
            conn.commit()
            messagebox.showinfo("Success", "Customer information saved successfully!")
            self.clear_form()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to save data: {e}")
        finally:
            if conn:
                conn.close()

    def clear_form(self):
        """
        Clears all the input fields after successful submission.
        """
        self.name_entry.delete(0, tk.END)
        self.birthday_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)
        self.contact_method_menu.set("Email") # Reset dropdown to default

# --- Main Application Execution ---
if __name__ == "__main__":
    root = tk.Tk()
    app = CustomerApp(root)
    root.mainloop()
