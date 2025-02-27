import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os
import re

# CSV file to store to-do data
CSV_FILE = "todo_list.csv"


def initialize_csv():
    """Ensure the CSV file exists and has the required headers."""
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["S.No", "Time", "Task", "Completed"])


def load_todo_data():
    """Load the to-do data from the CSV file."""
    todo_data = []
    with open(CSV_FILE, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            todo_data.append(row)
    return todo_data


def save_todo_data(data):
    """Save the to-do data to the CSV file."""
    with open(CSV_FILE, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["S.No", "Time", "Task", "Completed"])
        writer.writeheader()
        writer.writerows(data)


def is_valid_time_format(time_str):
    """Validate the time format as HH:MM AM/PM."""
    pattern = r"^(0[1-9]|1[0-2]):[0-5][0-9] (AM|PM|am|pm|Am|Pm|aM|pM)$"
    return re.match(pattern, time_str) is not None


def reminder1():
    """Function to manage the reminder dashboard."""
    reminder_window = tk.Tk()
    reminder_window.geometry("800x400")
    reminder_window.title("Reminder Dashboard")

    # Table frame
    table_frame = tk.Frame(reminder_window)
    table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    # Scrollbar for the table
    scrollbar = tk.Scrollbar(table_frame, orient=tk.VERTICAL)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Create a Treeview
    tree = ttk.Treeview(
        table_frame,
        columns=("S.No", "Time", "Task", "Completed"),
        show="headings",
        yscrollcommand=scrollbar.set,
    )
    tree.pack(fill=tk.BOTH, expand=True)
    scrollbar.config(command=tree.yview)

    # Set column headings
    tree.heading("S.No", text="S.No")
    tree.heading("Time", text="Time")
    tree.heading("Task", text="Task")
    tree.heading("Completed", text="Completed")

    tree.column("S.No", width=50, anchor="center")
    tree.column("Time", width=100, anchor="center")
    tree.column("Task", width=500, anchor="w")
    tree.column("Completed", width=100, anchor="center")

    def refresh_data():
        """Refresh the table with current data."""
        for item in tree.get_children():
            tree.delete(item)

        data = load_todo_data()
        for item in data:
            completed_status = "Yes" if item["Completed"] == "Yes" else "No"
            tree.insert("", "end", values=(item["S.No"], item["Time"], item["Task"], completed_status))

    def update_task_completion(event):
        """Toggle the completed status of the selected task."""
        selected_item = tree.selection()
        if selected_item:
            item_values = tree.item(selected_item[0], "values")
            sno = item_values[0]

            # Update completion status in the CSV
            data = load_todo_data()
            for row in data:
                if row["S.No"] == sno:
                    row["Completed"] = "No" if row["Completed"] == "Yes" else "Yes"
                    break
            save_todo_data(data)
            refresh_data()

    def add_task():
        """Open a popup to add a new task."""
        add_window = tk.Toplevel(reminder_window)
        add_window.geometry("400x200")
        add_window.title("Add New Task")

        tk.Label(add_window, text="Time:").grid(row=0, column=0, padx=10, pady=10)
        time_entry = tk.Entry(add_window)
        time_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(add_window, text="Task:").grid(row=1, column=0, padx=10, pady=10)
        task_entry = tk.Entry(add_window)
        task_entry.grid(row=1, column=1, padx=10, pady=10)

        def save_task():
            time = time_entry.get().strip()
            task = task_entry.get().strip()

            if not time or not task:
                messagebox.showerror("Error", "Both fields are required!")
                return

            if not is_valid_time_format(time):
                messagebox.showerror("Error", "Invalid time format! Use HH:MM AM/PM (e.g., 12:30 PM).")
                return

            data = load_todo_data()
            sno = str(len(data) + 1)
            data.append({"S.No": sno, "Time": time, "Task": task, "Completed": "No"})
            save_todo_data(data)
            refresh_data()
            add_window.destroy()

        tk.Button(add_window, text="Save", command=save_task).grid(row=2, column=1, pady=10)

    def delete_task():
        """Delete the selected task."""
        selected_item = tree.selection()
        if selected_item:
            item_values = tree.item(selected_item[0], "values")
            sno = item_values[0]

            # Remove the task from CSV
            data = load_todo_data()
            data = [row for row in data if row["S.No"] != sno]
            save_todo_data(data)
            refresh_data()
        else:
            messagebox.showerror("Error", "No task selected to delete!")

    # Add event binding for double-click to toggle completion
    tree.bind("<Double-1>", update_task_completion)

    # Buttons for Add and Delete
    button_frame = tk.Frame(reminder_window)
    button_frame.pack(fill=tk.X, padx=20, pady=10)

    tk.Button(button_frame, text="Add Task", command=add_task).pack(side=tk.LEFT, padx=10, pady=5)
    tk.Button(button_frame, text="Delete Task", command=delete_task).pack(side=tk.LEFT, padx=10, pady=5)

    refresh_data()
    reminder_window.mainloop()

def remind():
    initialize_csv()
    reminder1()

# Initialize CSV and open the reminder dashboard
if __name__ == "__main__":
    remind()
