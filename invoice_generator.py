# invoice_generator.py

import os
from fpdf import FPDF
from datetime import datetime

COUNTER_FILE = "data/invoice_counter.txt"

def get_next_invoice_number():
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(COUNTER_FILE):
        with open(COUNTER_FILE, "w") as f:
            f.write("1")
        return "LSK001"

    with open(COUNTER_FILE, "r+") as f:
        content = f.read().strip()
        if not content.isdigit():
            f.seek(0)
            f.write("1")
            f.truncate()
            return "LSK001"

        current = int(content)
        next_num = current + 1
        f.seek(0)
        f.write(str(next_num))
        f.truncate()
        return f"LSK{next_num:03d}"

def generate_invoice(student_name, course, duration, date, particulars, total, payment_mode, balance, save_folder):
    invoice_no = get_next_invoice_number()
    os.makedirs(save_folder, exist_ok=True)
    filename = os.path.join(save_folder, f"{invoice_no}.pdf")

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "LITTLE SKY KIDS", ln=True, align="C")
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 8, "Unit 236-237, Lodha Signet, Kolshet West, Thane, Maharashtra - 400607", ln=True, align="C")
    pdf.cell(0, 8, "www.littleskykids.com | info.littleskykids@gmail.com", ln=True, align="C")
    pdf.cell(0, 8, "+91 8097918044 / +91 8600333649", ln=True, align="C")

    pdf.ln(10)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(100, 10, f"Receipt No: {invoice_no}", ln=False)
    pdf.cell(0, 10, f"Date: {date}", ln=True)

    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Name of Student: {student_name}", ln=True)
    pdf.cell(0, 10, f"Course: {course}", ln=True)
    pdf.cell(0, 10, f"Course Duration: {duration}", ln=True)

    pdf.ln(5)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(10, 10, "Sr", border=1)
    pdf.cell(100, 10, "Particulars", border=1)
    pdf.cell(0, 10, "Amount", border=1, ln=True)

    pdf.set_font("Arial", "", 12)
    for i, (name, amt) in enumerate(particulars, start=1):
        pdf.cell(10, 10, str(i), border=1)
        pdf.cell(100, 10, name, border=1)
        pdf.cell(0, 10, f"{amt:.2f}", border=1, ln=True)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(110, 10, "Total", border=1)
    pdf.cell(0, 10, f"{total:.2f}", border=1, ln=True)

    pdf.ln(5)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Payment Mode: {payment_mode}", ln=True)
    pdf.cell(0, 10, f"Balance (if any): {balance:.2f}", ln=True)

    pdf.ln(20)
    pdf.cell(0, 10, "Sign & Stamp (Principal)", ln=False)
    pdf.cell(0, 10, "Sign (Parent/Guardian)", ln=True, align="R")

    pdf.output(filename)
    return filename
