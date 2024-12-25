import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Database setup
def create_table():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roll_number TEXT NOT NULL UNIQUE,
            student_class TEXT NOT NULL,
            student_year INTEGER NOT NULL DEFAULT 2024
        )
    """)
    conn.commit()
    conn.close()

# Functions
def add_student():
    name = name_entry.get()
    roll_number = roll_number_entry.get()
    student_class = class_entry.get()
    student_year = year_entry.get()

    if name == "" or roll_number == "" or student_class == "" or student_year == "":
        messagebox.showerror("Error", "All fields are required!")
        return

    try:
        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO students (name, roll_number, student_class, student_year) VALUES (?, ?, ?, ?)",
                       (name, roll_number, student_class, student_year))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Student added successfully!")
        clear_inputs()
        fetch_students()
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Roll Number must be unique!")

def fetch_students():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    conn.close()

    for row in student_table.get_children():
        student_table.delete(row)

    for row in rows:
        student_table.insert("", tk.END, values=row)

def delete_student():
    selected_item = student_table.focus()
    if not selected_item:
        messagebox.showerror("Error", "Please select a student to delete!")
        return

    student_id = student_table.item(selected_item)["values"][0]
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "Student deleted successfully!")
    fetch_students()

def update_student():
    selected_item = student_table.focus()
    if not selected_item:
        messagebox.showerror("Error", "Please select a student to update!")
        return

    student_id = student_table.item(selected_item)["values"][0]
    name = name_entry.get()
    roll_number = roll_number_entry.get()
    student_class = class_entry.get()
    student_year = year_entry.get()

    if name == "" or roll_number == "" or student_class == "" or student_year == "":
        messagebox.showerror("Error", "All fields are required!")
        return

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE students
        SET name = ?, roll_number = ?, student_class = ?, student_year = ?
        WHERE id = ?
    """, (name, roll_number, student_class, student_year, student_id))
    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "Student updated successfully!")
    clear_inputs()
    fetch_students()

def clear_inputs():
    name_entry.delete(0, tk.END)
    roll_number_entry.delete(0, tk.END)
    class_entry.delete(0, tk.END)
    year_entry.delete(0, tk.END)

def on_row_select(event):
    selected_item = student_table.focus()
    if not selected_item:
        return

    values = student_table.item(selected_item)["values"]
    name_entry.delete(0, tk.END)
    roll_number_entry.delete(0, tk.END)
    class_entry.delete(0, tk.END)
    year_entry.delete(0, tk.END)

    name_entry.insert(0, values[1])
    roll_number_entry.insert(0, values[2])
    class_entry.insert(0, values[3])
    year_entry.insert(0, values[4])

# GUI Setup
app = tk.Tk()
app.title("Student Management System")
app.geometry("700x500")

# Input Fields
tk.Label(app, text="Name").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
name_entry = tk.Entry(app, width=30)
name_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(app, text="Roll Number").grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
roll_number_entry = tk.Entry(app, width=30)
roll_number_entry.grid(row=1, column=1, padx=10, pady=10)

tk.Label(app, text="Class").grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
class_entry = tk.Entry(app, width=30)
class_entry.grid(row=2, column=1, padx=10, pady=10)

tk.Label(app, text="Year").grid(row=3, column=0, padx=10, pady=10, sticky=tk.W)
year_entry = tk.Entry(app, width=30)
year_entry.grid(row=3, column=1, padx=10, pady=10)

# Buttons
tk.Button(app, text="Add Student", command=add_student, width=15).grid(row=4, column=0, pady=10, padx=10)
tk.Button(app, text="Update Student", command=update_student, width=15).grid(row=4, column=1, pady=10, padx=10)
tk.Button(app, text="Delete Student", command=delete_student, width=15).grid(row=5, column=0, pady=10, padx=10)
tk.Button(app, text="Clear", command=clear_inputs, width=15).grid(row=5, column=1, pady=10, padx=10)

# Student Table
student_table = ttk.Treeview(app, columns=("ID", "Name", "Roll Number", "Class", "Year"), show="headings")
student_table.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky=tk.W + tk.E)

student_table.heading("ID", text="ID")
student_table.heading("Name", text="Name")
student_table.heading("Roll Number", text="Roll Number")
student_table.heading("Class", text="Class")
student_table.heading("Year", text="Year")

student_table.bind("<<TreeviewSelect>>", on_row_select)

# Fetch students on startup
create_table()
fetch_students()

# Start the GUI
app.mainloop()