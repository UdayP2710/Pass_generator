import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector

from generator import generate_password
from database import save_record, get_history

window = tk.Tk()
window.title("Password Generator")
window.geometry("500x450")

generated_length = None
password=None

record_label = tk.Label(
    window,
    text="Record label (for example, 'Whatsapp'):"
)
record_label.pack(pady=10)

label_entry = tk.Entry(window, width=35)
label_entry.pack()

length_label = tk.Label(window, text="Password length (8 to 64):")
length_label.pack(pady=10)

length_entry = tk.Entry(window, width=10)
length_entry.pack()
length_entry.insert(0, "16")

result_label = tk.Label(
    window,
    text="Your password will appear here",
    font=("Arial", 14),
    wraplength=450
)
result_label.pack(pady=20)


##----------This Funtion will trigget the ""generate_password"" function and update the interface with the generated password ------------##
def show_password():
    global generated_length
    global password

    try:
        length = int(length_entry.get())
    except ValueError:
        messagebox.showerror(
            "Invalid length",
            "Enter a whole number, such as 16.",
            parent=window
        )
        return

    if length < 8 or length > 64:
        messagebox.showerror(
            "Invalid length",
            "Choose a length from 8 to 64.",
            parent=window
        )
        return

    password = generate_password(length)
    generated_length = len(password)

    result_label.config(text=password)
    save_button.config(state="normal")



##----------This Funtion saves Record in the database------------##
def save_history():
    label = label_entry.get().strip()

    if label == "":
        messagebox.showerror(
            "Missing label",
            "Enter a label, such as School demo.",
            parent=window
        )
        return

    if len(label) > 80:
        messagebox.showerror(
            "Label too long",
            "Use a label containing at most 80 characters.",
            parent=window
        )
        return

    try:
        save_record(label, generated_length, password)
    except mysql.connector.Error as error:
        messagebox.showerror(
            "Database error",
            str(error),
            parent=window
        )
        return

    save_button.config(state="disabled")

    messagebox.showinfo(
        "Saved",
        "Generation record saved successfully.",
        parent=window
    )



##-------------This functions let's user to view the records saved in the database----------------##
def show_history():
    try:
        rows = get_history()
    except mysql.connector.Error as error:
        messagebox.showerror(
            "Database error",
            str(error),
            parent=window
        )
        return

    if not rows:
        messagebox.showinfo(
            "History",
            "No records have been saved yet.",
            parent=window
        )
        return

    history_window = tk.Toplevel(window)
    history_window.title("Generation history")
    history_window.geometry("650x350")

    table = ttk.Treeview(
        history_window,
        columns=("record_id", "label", "password_length", "Actual_password"),
        show="headings"
    )

    table.heading("record_id", text="Record ID")
    table.heading("label", text="Label")
    table.heading("password_length", text="Password length")
    table.heading("Actual_password", text="Actual_password")

    table.column(
        "record_id", width=80, anchor="center", stretch=False
    )
    table.column("label", width=250,anchor="center")
    table.column(
        "password_length", width=160, anchor="center", stretch=False
    )
    table.column(
            "Actual_password", width=250, anchor="center",
        )

    scrollbar = ttk.Scrollbar(
        history_window,
        orient="vertical",
        command=table.yview
    )
    scrollbar.pack(side="right", fill="y")

    table.config(yscrollcommand=scrollbar.set)
    table.pack(
        side="left",
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

    for row in rows:
        table.insert("", "end", values=row)

##---------Buttons for generating password, it will trigger the ""show_password"" function-------------##
generate_button = tk.Button(
    window,
    text="Generate password",
    command=show_password
)
generate_button.pack(pady=10)


##-----------Buttons for Saving the record. it will trigger the ""save_history"" function-------------##
save_button = tk.Button(
    window,
    text="Save record",
    command=save_history,
    state="disabled"
)
save_button.pack(pady=5)

##-----------Buttons for displaying the Record history. it will trigger the ""show_history"" function-------------##
history_button = tk.Button(
    window,
    text="View history",
    command=show_history
)
history_button.pack(pady=5)

window.mainloop()
