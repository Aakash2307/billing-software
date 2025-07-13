# main.py

import os
import datetime
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from invoice_generator import generate_invoice

DEFAULT_FOLDER = os.path.join(os.path.expanduser("~"), "Desktop", "Invoices")
selected_folder = DEFAULT_FOLDER

all_fee_types = [
    "Admission Fee", "Tuition Fee", "Exam Fee",
    "Stationary Charges", "Security Deposits", "Activity Charges"
]

used_fee_types = set()
particular_rows = []

payment_modes = ["Cash", "Credit", "Debit", "UPI", "Netbanking", "Cheque", "Demand Draft"]

def update_add_particular_button():
    remaining = [item for item in all_fee_types if item not in used_fee_types]
    add_particular_btn.config(state='normal' if remaining else 'disabled')

def add_dropdown_particular():
    remaining = [item for item in all_fee_types if item not in used_fee_types]
    if not remaining:
        return

    selected = remaining[0]
    used_fee_types.add(selected)
    update_add_particular_button()

    row_frame = tk.Frame(particulars_frame)
    row_frame.pack(fill='x', pady=2)

    fee_label = tk.Label(row_frame, text=selected, width=30, anchor='w')
    fee_label.pack(side='left', padx=5)

    amount_entry = tk.Entry(row_frame, width=15)
    amount_entry.pack(side='left', padx=5)

    def delete_row():
        used_fee_types.remove(selected)
        particular_rows.remove((row_frame, selected, amount_entry))
        row_frame.destroy()
        update_add_particular_button()

    delete_btn = tk.Button(row_frame, text="Delete", command=delete_row)
    delete_btn.pack(side='left', padx=5)

    particular_rows.append((row_frame, selected, amount_entry))

def add_custom_particular():
    row_frame = tk.Frame(particulars_frame)
    row_frame.pack(fill='x', pady=2)

    custom_entry = tk.Entry(row_frame, width=30)
    custom_entry.insert(0, "Custom Fee Name")
    custom_entry.pack(side='left', padx=5)

    amount_entry = tk.Entry(row_frame, width=15)
    amount_entry.pack(side='left', padx=5)

    def delete_row():
        particular_rows.remove((row_frame, custom_entry, amount_entry))
        row_frame.destroy()

    delete_btn = tk.Button(row_frame, text="Delete", command=delete_row)
    delete_btn.pack(side='left', padx=5)

    particular_rows.append((row_frame, custom_entry, amount_entry))

def browse_folder():
    global selected_folder
    path = filedialog.askdirectory(title="Select Invoice Save Folder")
    if path:
        selected_folder = path
        folder_path_label.config(text=selected_folder)

def submit_invoice():
    name = name_entry.get().strip()
    course = course_entry.get().strip()
    duration = duration_entry.get().strip()
    date = datetime.datetime.now().strftime("%d-%m-%Y")
    payment_mode = payment_mode_var.get().strip()
    balance = balance_entry.get().strip()

    if not name or not course or not duration or not payment_mode:
        messagebox.showerror("Input Error", "All fields are required.")
        return

    particulars = []
    total = 0
    for row in particular_rows:
        _, pname_widget, amount_widget = row
        pname = pname_widget if isinstance(pname_widget, str) else pname_widget.get().strip()
        amt = amount_widget.get().strip()

        if pname and amt:
            try:
                amt_float = float(amt)
                particulars.append((pname, amt_float))
                total += amt_float
            except ValueError:
                messagebox.showerror("Input Error", f"Invalid amount: {amt}")
                return

    try:
        balance_amt = float(balance) if balance else 0
    except ValueError:
        messagebox.showerror("Input Error", "Balance must be a number.")
        return

    if not particulars:
        messagebox.showerror("Input Error", "Add at least one fee item.")
        return

    invoice_path = generate_invoice(
        student_name=name,
        course=course,
        duration=duration,
        date=date,
        particulars=particulars,
        total=total,
        payment_mode=payment_mode,
        balance=balance_amt,
        save_folder=selected_folder
    )

    messagebox.showinfo("Invoice Generated", f"Invoice saved to:\n{invoice_path}")

# ========== UI ==========

app = tk.Tk()
app.title("Little Sky Kids Billing Software")
app.geometry("700x850")
app.resizable(False, False)

tk.Label(app, text="Student Name").pack()
name_entry = tk.Entry(app, width=50)
name_entry.pack()

tk.Label(app, text="Course").pack()
course_entry = tk.Entry(app, width=50)
course_entry.pack()

tk.Label(app, text="Course Duration").pack()
duration_entry = tk.Entry(app, width=50)
duration_entry.pack()

tk.Label(app, text="Date of Payment (Auto-filled)").pack()
tk.Label(app, text=datetime.datetime.now().strftime("%d-%m-%Y")).pack()

tk.Label(app, text="Fee Particulars").pack(pady=10)
particulars_frame = tk.Frame(app)
particulars_frame.pack()

add_particular_btn = tk.Button(app, text="Add Particular", command=add_dropdown_particular)
add_particular_btn.pack(pady=5)

add_custom_btn = tk.Button(app, text="Add Custom Particular", command=add_custom_particular)
add_custom_btn.pack(pady=5)

tk.Label(app, text="Payment Mode").pack()
payment_mode_var = tk.StringVar()
payment_mode_combo = ttk.Combobox(app, textvariable=payment_mode_var, values=payment_modes, state='readonly', width=30)
payment_mode_combo.pack()
payment_mode_combo.set(payment_modes[0])

tk.Label(app, text="Balance (if any)").pack()
balance_entry = tk.Entry(app, width=50)
balance_entry.pack()

tk.Label(app, text="Invoice Save Folder:").pack(pady=(20, 5))
folder_path_label = tk.Label(app, text=selected_folder, fg="blue", wraplength=600)
folder_path_label.pack()
tk.Button(app, text="Browse Folder", command=browse_folder).pack(pady=5)

tk.Button(app, text="Generate Invoice", command=submit_invoice, bg="green", fg="white").pack(pady=20)

update_add_particular_button()
app.mainloop()
