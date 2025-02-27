
import os 
import time
import subprocess
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk


from reminder import remind

# Other functions like `create_rounded_rectangle`, `login`, etc., remain unchanged.

def run_detect1():
    """Run the detect1.py file."""
    try:
        # Use subprocess to run the file
        result = subprocess.run(["python", "detect1.py"], check=True, capture_output=True, text=True)
        # If successful, show output
        messagebox.showinfo("Success", "detect1.py executed successfully.\nOutput:\n" + result.stdout)
    except subprocess.CalledProcessError as e:
        # If there are errors during execution, show them
        messagebox.showerror("Error", f"Error while executing detect1.py:\n{e.stderr}")
    except Exception as e:
        # Handle unexpected exceptions
        messagebox.showerror("Error", f"Failed to execute detect1.py:\n{str(e)}")

def reminder():
    remind()




def create_rounded_rectangle(canvas, x1, y1, x2, y2, radius=20, color="#D3D3D3"):
    """Draws a rectangle with rounded corners on a canvas."""
    canvas.create_arc(x1, y1, x1 + 2 * radius, y1 + 2 * radius, start=90, extent=90, fill=color, outline=color)
    canvas.create_arc(x2 - 2 * radius, y1, x2, y1 + 2 * radius, start=0, extent=90, fill=color, outline=color)
    canvas.create_arc(x1, y2 - 2 * radius, x1 + 2 * radius, y2, start=180, extent=90, fill=color, outline=color)
    canvas.create_arc(x2 - 2 * radius, y2 - 2 * radius, x2, y2, start=270, extent=90, fill=color, outline=color)
    canvas.create_rectangle(x1 + radius, y1, x2 - radius, y2, fill=color, outline=color)
    canvas.create_rectangle(x1, y1 + radius, x2, y2 - radius, fill=color, outline=color)

def login():
    """Validate login credentials."""
    username = username_entry.get()
    password = password_entry.get()
    if username == "a" and password == "a":
        messagebox.showinfo("Login Successful", "Welcome to the dashboard!")
        clear_login_fields()  # Clear username and password fields
        open_dashboard()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")

def clear_login_fields():
    """Clear the username and password fields."""
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)


import time
import csv
from datetime import datetime, timedelta


def open_dashboard():
    """Opens the dashboard window with a real-time clock and CSV entry checks."""
    # Create the dashboard window
    dashboard = tk.Toplevel(root)
    dashboard.geometry("800x400")
    dashboard.title("Dashboard")

    # Set the background image
    bg_label_dashboard = tk.Label(dashboard, image=bg_photo)
    bg_label_dashboard.place(relwidth=1, relheight=1)

    # Real-time clock display
    clock_label = tk.Label(dashboard, font=("Arial", 14), bg="grey", fg="white")
    clock_label.place(relx=0.85, rely=0.05, anchor="ne")  # Top-right corner

    def update_clock_and_check_csv():
        """Update the clock and check the CSV file for overdue tasks."""
        # Update the clock
        current_time = datetime.now()
        formatted_time = current_time.strftime("%I:%M:%S %p").upper()  # Ensure uppercase AM/PM
        clock_label.config(text=formatted_time)

        # Check the CSV file for overdue tasks
        check_overdue_tasks(current_time)

        # Schedule the function to run every second
        dashboard.after(1000, update_clock_and_check_csv)

    def check_overdue_tasks(current_time):
        """Check the CSV for incomplete tasks with overdue times."""
        overdue_tasks = []
        try:
            CSV_FILE="todo_list.csv"
            with open(CSV_FILE, "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row["Completed"].strip().upper() == "NO":
                        # Standardize time format in the CSV
                        task_time_str = row["Time"].strip().upper()
                        task_time = datetime.strptime(task_time_str, "%I:%M %p")

                        # Add a 2-minute buffer to the task time
                        task_time_with_buffer = task_time + timedelta(minutes=2)

                        # Check if the current time is within the buffer
                        if task_time <= current_time <= task_time_with_buffer:
                            overdue_tasks.append(row["Task"])
        except Exception as e:
            print(f"Error reading CSV: {e}")

        # Notify for overdue tasks
        if overdue_tasks:
            messagebox.showwarning(
                "Overdue Tasks",
                f"The following tasks are overdue:\n" + "\n".join(overdue_tasks),
            )

    update_clock_and_check_csv()  # Start the real-time clock and task checker

    # Create the frame for buttons with rounded corners
    canvas_dashboard = tk.Canvas(dashboard, width=350, height=250, highlightthickness=0, bg="grey")
    canvas_dashboard.place(relx=0.5, rely=0.5, anchor="center")
    create_rounded_rectangle(canvas_dashboard, 0, 0, 350, 250, radius=25, color="#D3D3D3")

    # Place buttons on top of the rounded rectangle
    button_frame = tk.Frame(canvas_dashboard, bg="#D3D3D3")
    button_frame.place(relx=0.5, rely=0.5, anchor="center", width=340, height=240)

    # Add buttons
    health_button = tk.Button(button_frame, text="Reminder", bg="#1E90FF", fg="white", font=("Arial", 12, "bold"), command=reminder)
    health_button.place(x=100, y=30, width=140, height=40)

    threat_button = tk.Button(
        button_frame,
        text="Threat Alert",
        bg="#1E90FF",
        fg="white",
        font=("Arial", 12, "bold"),
        command=run_detect1  # Run the detect1.py file
    )
    threat_button.place(x=100, y=90, width=140, height=40)

    close_button = tk.Button(button_frame, text="Close Ones", bg="#1E90FF", fg="white", font=("Arial", 12, "bold"))
    close_button.place(x=100, y=150, width=140, height=40)

def run_detect1():
    """Run the detect1.py file."""
    try:
        os.system("python detect1.py")  # Executes the detect1.py file
    except Exception as e:
        messagebox.showerror("Error", f"Failed to execute detect1.py:\n{e}")

# Create the main window
root = tk.Tk()
root.geometry("800x400")
root.title("Login Page")

# Load the background image using Pillow
bg_image = Image.open("images/bg.jpg")  # Ensure the file path is correct
bg_image = bg_image.resize((800, 400), Image.BICUBIC)  # Resize with bicubic interpolation
bg_photo = ImageTk.PhotoImage(bg_image)

# Set the background image
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)

# Create a canvas for the rounded rectangle background
canvas = tk.Canvas(root, width=350, height=250, highlightthickness=0, bg="grey")
canvas.place(relx=0.5, rely=0.5, anchor="center")
create_rounded_rectangle(canvas, 0, 0, 350, 250, radius=25, color="#D3D3D3")  # Gray background

# Create a frame on top of the rounded rectangle for the login form
frame = tk.Frame(canvas, bg="#D3D3D3")
frame.place(relx=0.5, rely=0.5, anchor="center", width=340, height=240)

# Add a welcome text
welcome_label = tk.Label(
    frame, text="Welcome back . . .", fg="black", bg="#D3D3D3", font=("Arial", 16, "bold")
)
welcome_label.place(x=80, y=10)

# Username label and entry
username_label = tk.Label(frame, text="Username:", fg="black", bg="#D3D3D3", font=("Arial", 12))
username_label.place(x=20, y=60)
username_entry = tk.Entry(frame, width=25, font=("Arial", 12))
username_entry.place(x=120, y=60)

# Password label and entry
password_label = tk.Label(frame, text="Password:", fg="black", bg="#D3D3D3", font=("Arial", 12))
password_label.place(x=20, y=100)
password_entry = tk.Entry(frame, show="*", width=25, font=("Arial", 12))
password_entry.place(x=120, y=100)

# Terms and conditions checkbox
terms_var = tk.IntVar()
terms_checkbox = tk.Checkbutton(
    frame,
    text="I agree with terms and conditions.",
    variable=terms_var,
    fg="black",
    bg="#D3D3D3",
    font=("Arial", 10),
)
terms_checkbox.place(x=20, y=140)

# Login button
login_button = tk.Button(
    frame, text="Login", bg="#1E90FF", fg="white", font=("Arial", 12, "bold"), width=12, command=login
)
login_button.place(x=120, y=170)

# Run the application
root.mainloop()
