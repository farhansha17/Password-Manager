import sqlite3
import tkinter as tk
from tkinter import messagebox
import base64

# Database setup
def setup_db():
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            website TEXT,
            username TEXT,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

# Function to encrypt password
def encrypt_password(password):
    return base64.b64encode(password.encode()).decode()

# Function to decrypt password
def decrypt_password(encrypted_password):
    return base64.b64decode(encrypted_password.encode()).decode()

# Function to add password
def add_password(website, username, password):
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO passwords (website, username, password) VALUES (?, ?, ?)",
                   (website, username, encrypt_password(password)))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Password Saved!")
    update_password_list()

# Function to retrieve and display passwords
def get_passwords():
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute("SELECT website, username, password FROM passwords")
    data = cursor.fetchall()
    conn.close()
    return [(site, user, decrypt_password(pwd)) for site, user, pwd in data]

# Function to update listbox
def update_password_list():
    listbox.delete(0, tk.END)
    for site, user, pwd in get_passwords():
        listbox.insert(tk.END, f"{site} - {user} - {pwd}")

# GUI Setup
setup_db()
root = tk.Tk()
root.title("Password Manager")
root.geometry("400x300")

# UI Elements
tk.Label(root, text="Website").pack()
website_entry = tk.Entry(root)
website_entry.pack()

tk.Label(root, text="Username").pack()
username_entry = tk.Entry(root)
username_entry.pack()

tk.Label(root, text="Password").pack()
password_entry = tk.Entry(root, show="*")
password_entry.pack()

tk.Button(root, text="Add Password", command=lambda: add_password(
    website_entry.get(), username_entry.get(), password_entry.get())).pack()

listbox = tk.Listbox(root, width=50)
listbox.pack()

update_password_list()
root.mainloop()
