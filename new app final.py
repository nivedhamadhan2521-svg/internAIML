# Advanced Hospital Management System (Full CRU
# =========================================================
# ADVANCED HICHOSPITAL MANAGEMENT SYSTEM
# FULL CRUD PROJECT
# PYTHON + TKINTER + MYSQL
# =========================================================

# =========================================================
# INSTALL REQUIRED LIBRARIES
# =========================================================
# pip install pillow
# pip install mysql-connector-python
# pip install ttkbootstrap
# pip install tkcalendar
# pip install pandas
# pip install openpyxl

# =========================================================
# IMPORTS
# =========================================================

import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkcalendar import DateEntry
from PIL import Image, ImageTk
import mysql.connector
import pandas as pd

# =========================================================
# MYSQL CONNECTION
# =========================================================

con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="nive2530",
    database="hospitals_db"
)

cursor = con.cursor()

# =========================================================
# MAIN WINDOW
# =========================================================

root = tb.Window(themename="flatly")
root.title("NTHV CarePulse Hospital Management System")
root.state("zoomed")

SIDEBAR = "#0B2447"
MAIN_BG = "#F4F6F9"
CARD = "white"

# =========================================================
# LOGIN WINDOW
# =========================================================

login_window = tb.Toplevel(root)
login_window.geometry("900x500")
login_window.title("Hospital Login")
login_window.resizable(False, False)

left_frame = tk.Frame(login_window, bg="#0B2447", width=350)
left_frame.pack(side=LEFT, fill=Y)

right_frame = tk.Frame(login_window, bg="white")
right_frame.pack(side=RIGHT, fill=BOTH, expand=True)

# =========================================================
# LOGIN IMAGE
# =========================================================

# Add your image file in project folder
# Example image name: hospital.png

try:

    hospital_img = Image.open("hosp_bg1.jpg")
    hospital_img = hospital_img.resize((736, 487))

    hospital_photo = ImageTk.PhotoImage(hospital_img)

    image_lbl = tk.Label(
        left_frame,
        image=hospital_photo,
        bg="#0B2447"
    )

    image_lbl.place(x=20, y=20)

except:
    pass

logo_lbl = tk.Label(
    left_frame,
    text="🏥 NTHV CAREPULSE",
    font=("Segoe UI", 24, "bold"),
    bg="#0B2447",
    fg="white"
)
logo_lbl.place(x=20, y=180)

sub_lbl = tk.Label(
    left_frame,
    text="Hospital Management System",
    font=("Segoe UI", 14),
    bg="#0B2447",
    fg="white"
)
sub_lbl.place(x=40, y=240)

login_lbl = tk.Label(
    right_frame,
    text="LOGIN",
    font=("Segoe UI", 28, "bold"),
    bg="white"
)
login_lbl.pack(pady=40)

username_var = tk.StringVar()
password_var = tk.StringVar()

username_entry = tb.Entry(
    right_frame,
    textvariable=username_var,
    width=35,
    font=("Segoe UI", 12)
)
username_entry.pack(pady=15)

password_entry = tb.Entry(
    right_frame,
    textvariable=password_var,
    width=35,
    show="*",
    font=("Segoe UI", 12)
)
password_entry.pack(pady=15)

root.withdraw()

# =========================================================
# MAIN FRAMES
# =========================================================

sidebar = tk.Frame(root, bg=SIDEBAR, width=250)
sidebar.pack(side=LEFT, fill=Y)

content_frame = tk.Frame(root, bg=MAIN_BG)
content_frame.pack(side=RIGHT, fill=BOTH, expand=True)

# =========================================================
# FUNCTIONS
# =========================================================

def clear_frame():

    for widget in content_frame.winfo_children():
        widget.destroy()

# =========================================================
# LOGIN FUNCTION
# =========================================================

def login():

    username = username_var.get()
    password = password_var.get()

    query = "SELECT * FROM users WHERE username=%s AND password=%s"

    cursor.execute(query, (username, password))

    row = cursor.fetchone()

    if row:

        messagebox.showinfo("Success", "Login Successful")

        login_window.destroy()
        root.deiconify()

    else:

        messagebox.showerror(
            "Error",
            "Invalid Username or Password"
        )

login_btn = tb.Button(
    right_frame,
    text="LOGIN",
    bootstyle="primary",
    width=25,
    command=login
)
login_btn.pack(pady=30)

# =========================================================
# DASHBOARD
# =========================================================

def dashboard_home():

    clear_frame()

    heading = tk.Label(
        content_frame,
        text="Hospital Dashboard",
        font=("Segoe UI", 28, "bold"),
        bg=MAIN_BG
    )
    heading.pack(pady=20)

    card_frame = tk.Frame(content_frame, bg=MAIN_BG)
    card_frame.pack()

    tables = [
        ("Patients", "patient_s"),
        ("Doctors", "doctors"),
        ("Appointments", "appointments"),
        ("Billing", "billing"),
        ("Medicines", "medicines"),
        ("Rooms", "rooms"),
        ("Admissions", "admissions")
    ]

    for text, table in tables:

        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]

        card = tk.Frame(
            card_frame,
            bg=CARD,
            width=220,
            height=200
        )

        card.pack(side=LEFT, padx=10, pady=10)
        card.pack_propagate(False)

        tk.Label(
            card,
            text=text,
            font=("Segoe UI", 16, "bold"),
            bg=CARD
        ).pack(pady=15)

        tk.Label(
            card,
            text=count,
            font=("Segoe UI", 30, "bold"),
            fg="blue",
            bg=CARD
        ).pack()

# =========================================================
# GENERIC CRUD MODULE
# =========================================================

def open_module(title, table_name, columns):

    clear_frame()

    heading = tk.Label(
        content_frame,
        text=title,
        font=("Segoe UI", 24, "bold"),
        bg=MAIN_BG
    )
    heading.pack(pady=10)

    form_frame = tk.Frame(content_frame, bg="white")
    form_frame.pack(fill=X, padx=20, pady=10)

    variables = {}

    row = 0

    for col in columns[1:]:

        variables[col] = tk.StringVar()

        tk.Label(
            form_frame,
            text=col.upper(),
            font=("Segoe UI", 10, "bold"),
            bg="white"
        ).grid(row=row, column=0, padx=10, pady=8)

        if col == "gender":

            gender_combo = ttk.Combobox(
                form_frame,
                textvariable=variables[col],
                values=["Male", "Female", "Other"],
                width=33,
                state="readonly"
            )

            gender_combo.grid(row=row, column=1)

        elif col == "blood_group":

            blood_combo = ttk.Combobox(
                form_frame,
                textvariable=variables[col],
                values=[
                    "A+", "A-", "B+", "B-",
                    "O+", "O-", "AB+", "AB-"
                ],
                width=33,
                state="readonly"
            )

            blood_combo.grid(row=row, column=1)

        else:

            tk.Entry(
                form_frame,
                textvariable=variables[col],
                width=35
            ).grid(row=row, column=1)

        row += 1

    tree_frame = tk.Frame(content_frame)
    tree_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)

    scroll_y = ttk.Scrollbar(tree_frame, orient=VERTICAL)
    scroll_x = ttk.Scrollbar(tree_frame, orient=HORIZONTAL)

    style = ttk.Style()

    style.configure(
        "Treeview",
        rowheight=22,
        font=("Segoe UI", 10)
    )

    style.configure(
        "Treeview.Heading",
        font=("Segoe UI", 11, "bold")
    )

    tree = ttk.Treeview(
        tree_frame,
        columns=columns,
        yscrollcommand=scroll_y.set,
        xscrollcommand=scroll_x.set
    )

    scroll_y.config(command=tree.yview)
    scroll_x.config(command=tree.xview)

    scroll_y.pack(side=RIGHT, fill=Y)
    scroll_x.pack(side=BOTTOM, fill=X)

    tree.pack(fill=BOTH, expand=True)

    for col in columns:

        tree.heading(col, text=col.upper())
        tree.column(col, width=150)

    tree["show"] = "headings"

    # =====================================================
    # FETCH
    # =====================================================

    def fetch_data():

        for item in tree.get_children():
            tree.delete(item)

        cursor.execute(f"SELECT * FROM {table_name}")

        rows = cursor.fetchall()

        for row in rows:
            tree.insert("", END, values=row)

    fetch_data()

    # =====================================================
    # ADD
    # =====================================================

    def add_data():

        values = []

        for col in columns[1:]:
            values.append(variables[col].get())

        placeholders = ",".join(["%s"] * len(values))

        query = f"""
        INSERT INTO {table_name}
        ({','.join(columns[1:])})
        VALUES ({placeholders})
        """

        cursor.execute(query, tuple(values))
        con.commit()

        fetch_data()

        messagebox.showinfo(
            "Success",
            "Record Added Successfully"
        )

    # =====================================================
    # UPDATE
    # =====================================================

    def update_data():

        selected = tree.focus()

        values = tree.item(selected, "values")

        if not values:
            return

        update_query = []
        update_values = []

        for col in columns[1:]:

            update_query.append(f"{col}=%s")
            update_values.append(variables[col].get())

        update_values.append(values[0])

        query = f"""
        UPDATE {table_name}
        SET {','.join(update_query)}
        WHERE {columns[0]}=%s
        """

        cursor.execute(query, tuple(update_values))
        con.commit()

        fetch_data()

        messagebox.showinfo(
            "Updated",
            "Record Updated Successfully"
        )

    # =====================================================
    # DELETE
    # =====================================================

    def delete_data():

        selected = tree.focus()

        values = tree.item(selected, "values")

        if not values:
            return

        query = f"DELETE FROM {table_name} WHERE {columns[0]}=%s"

        cursor.execute(query, (values[0],))
        con.commit()

        fetch_data()

        messagebox.showinfo(
            "Deleted",
            "Record Deleted Successfully"
        )

    # =====================================================
    # SELECT
    # =====================================================

    def select_data(event):

        selected = tree.focus()

        values = tree.item(selected, "values")

        if values:

            for i, col in enumerate(columns[1:]):
                variables[col].set(values[i + 1])

    tree.bind("<ButtonRelease-1>", select_data)

    # =====================================================
    # BUTTONS
    # =====================================================

    btn_frame = tk.Frame(content_frame, bg=MAIN_BG)
    btn_frame.pack(pady=10)

    tb.Button(
        btn_frame,
        text="➕ Add",
        bootstyle="success",
        width=15,
        command=add_data
    ).pack(side=LEFT, padx=10)

    tb.Button(
        btn_frame,
        text="✏ Update",
        bootstyle="warning",
        width=15,
        command=update_data
    ).pack(side=LEFT, padx=10)

    tb.Button(
        btn_frame,
        text="❌ Delete",
        bootstyle="danger",
        width=15,
        command=delete_data
    ).pack(side=LEFT, padx=10)

# =========================================================
# ALL TABLE MODULES
# EVERY MODULE BELOW HAS:
# ✔ ADD
# ✔ UPDATE
# ✔ DELETE
# ✔ VIEW
# ✔ TREEVIEW
# =========================================================
# =========================================================

def patient_module():

    open_module(
        "Patient Management",
        "patient_s",
        (
            "patient_id",
            "patient_name",
            "age",
            "gender",
            "phone",
            "address",
            "blood_group",
            "disease",
            "date_registered"
        )
    )

def doctor_module():

    open_module(
        "Doctor Management",
        "doctors",
        (
            "doctor_id",
            "doctor_name",
            "specialization",
            "phone",
            "email",
            "salary"
        )
    )

def appointment_module():

    open_module(
        "Appointment Management",
        "appointments",
        (
            "appointment_id",
            "patient_id",
            "doctor_id",
            "appointment_date",
            "appointment_time",
            "status"
        )
    )

def billing_module():

    open_module(
        "Billing Management",
        "billing",
        (
            "bill_id",
            "patient_id",
            "total_amount",
            "payment_status",
            "bill_date"
        )
    )

def medicine_module():

    open_module(
        "Medicine Management",
        "medicines",
        (
            "medicine_id",
            "medicine_name",
            "company",
            "price",
            "stock",
            "expiry_date"
        )
    )

def prescription_module():

    open_module(
        "Prescription Management",
        "prescriptions",
        (
            "prescription_id",
            "patient_id",
            "doctor_id",
            "medicine_id",
            "dosage",
            "prescription_date"
        )
    )

def room_module():

    open_module(
        "Room Management",
        "rooms",
        (
            "room_id",
            "room_number",
            "room_type",
            "status"
        )
    )

def admission_module():

    open_module(
        "Admission Management",
        "admissions",
        (
            "admission_id",
            "patient_id",
            "room_id",
            "admission_date",
            "discharge_date"
        )
    )

# =========================================================
# BILL RECEIPT SYSTEM
# =========================================================

def generate_bill_receipt():

    selected = tk.Toplevel(root)
    selected.title("Generate Bill Receipt")
    selected.geometry("500x400")

    tk.Label(
        selected,
        text="Enter Patient ID",
        font=("Segoe UI", 12, "bold")
    ).pack(pady=10)

    patient_id_var = tk.StringVar()

    patient_entry = tk.Entry(
        selected,
        textvariable=patient_id_var,
        font=("Segoe UI", 12),
        width=25
    )
    patient_entry.pack(pady=10)

    def show_receipt():

        patient_id = patient_id_var.get()

        receipt_window = tk.Toplevel(root)
        receipt_window.title("Hospital Bill Receipt")
        receipt_window.geometry("700x700")
        receipt_window.config(bg="white")

        receipt_text = tk.Text(
            receipt_window,
            font=("Courier New", 11),
            bg="white"
        )

        receipt_text.pack(fill=BOTH, expand=True)

        # =====================================================
        # PATIENT DETAILS
        # =====================================================

        cursor.execute(
            "SELECT patient_name,disease FROM patient_s WHERE patient_id=%s",
            (patient_id,)
        )

        patient = cursor.fetchone()

        if not patient:

            messagebox.showerror(
                "Error",
                "Patient Not Found"
            )
            return

        patient_name = patient[0]
        disease = patient[1]

        # =====================================================
        # DOCTOR DETAILS
        # =====================================================

        cursor.execute(
            """
            SELECT doctors.doctor_name
            FROM appointments
            INNER JOIN doctors
            ON appointments.doctor_id = doctors.doctor_id
            WHERE appointments.patient_id=%s
            LIMIT 1
            """,
            (patient_id,)
        )

        doctor = cursor.fetchone()

        doctor_name = "Not Assigned"

        if doctor:
            doctor_name = doctor[0]

        # =====================================================
        # MEDICINE TOTAL
        # =====================================================

        cursor.execute(
            """
            SELECT SUM(medicines.price)
            FROM prescriptions
            INNER JOIN medicines
            ON prescriptions.medicine_id = medicines.medicine_id
            WHERE prescriptions.patient_id=%s
            """,
            (patient_id,)
        )

        medicine_total = cursor.fetchone()[0]

        if medicine_total is None:
            medicine_total = 0

        # =====================================================
        # ROOM CHARGE
        # =====================================================

        room_charge = 0

        cursor.execute(
            """
            SELECT rooms.room_type
            FROM admissions
            INNER JOIN rooms
            ON admissions.room_id = rooms.room_id
            WHERE admissions.patient_id=%s
            LIMIT 1
            """,
            (patient_id,)
        )

        room = cursor.fetchone()

        room_type = "No Room"

        if room:

            room_type = room[0]

            if room_type == "General":
                room_charge = 2000

            elif room_type == "Deluxe":
                room_charge = 5000

            elif room_type == "ICU":
                room_charge = 10000

        # =====================================================
        # CONSULTATION CHARGE
        # =====================================================

        consultation_charge = 500

        total_amount = (
            consultation_charge +
            medicine_total +
            room_charge
        )

        # =====================================================
        # RECEIPT FORMAT
        # =====================================================

        receipt = f"""
=======================================================
                NTHV CAREPULSE HOSPITAL
=======================================================

Patient ID        : {patient_id}
Patient Name      : {patient_name}
Disease           : {disease}
Doctor Name       : {doctor_name}

-------------------------------------------------------
CONSULTATION CHARGE : ₹ {consultation_charge}
MEDICINE CHARGE     : ₹ {medicine_total}
ROOM TYPE            : {room_type}
ROOM CHARGE          : ₹ {room_charge}
-------------------------------------------------------
TOTAL AMOUNT         : ₹ {total_amount}
-------------------------------------------------------

Thank You For Visiting
Get Well Soon

=======================================================
        """

        receipt_text.insert(END, receipt)

    tb.Button(
        selected,
        text="Generate Receipt",
        bootstyle="success",
        width=20,
        command=show_receipt
    ).pack(pady=20)

# =========================================================
# EXPORT EXCEL
# =========================================================

def export_excel():

    df = pd.read_sql("SELECT * FROM patient_s", con)

    df.to_excel("patients.xlsx", index=False)

    messagebox.showinfo(
        "Exported",
        "Excel Export Successful"
    )

# =========================================================
# LOGOUT
# =========================================================

def logout():

    confirm = messagebox.askyesno(
        "Logout",
        "Do you want to logout?"
    )

    if confirm:
        root.destroy()

# =========================================================
# SIDEBAR
# =========================================================

# =========================================================
# SIDEBAR BUTTONS
# ALL DATABASE TABLES INCLUDED
# =========================================================

buttons = [

    ("🏠 Dashboard", dashboard_home),
    ("🧑 Patients", patient_module),
    ("👨‍⚕ Doctors", doctor_module),
    ("📅 Appointments", appointment_module),
    ("💰 Billing", billing_module),
    ("💊 Medicines", medicine_module),
    ("📝 Prescriptions", prescription_module),
    ("🛏 Rooms", room_module),
    ("🏥 Admissions", admission_module),
    ("🧾 Bill Receipt", generate_bill_receipt),
    ("📤 Export Excel", export_excel),
    ("🚪 Logout", logout)
]

for text, command in buttons:

    btn = tk.Button(
        sidebar,
        text=text,
        font=("Segoe UI", 12, "bold"),
        bg=SIDEBAR,
        fg="white",
        activebackground="#19376D",
        activeforeground="white",
        bd=0,
        padx=20,
        pady=15,
        anchor="w",
        command=command
    )

    btn.pack(fill=X)

# =========================================================
# FOOTER
# =========================================================

footer = tk.Label(
    sidebar,
    text="© 2026 NTHV CarePulse",
    font=("Segoe UI", 10),
    bg=SIDEBAR,
    fg="white"
)
footer.pack(side=BOTTOM, pady=20)

# =========================================================
# DEFAULT PAGE
# =========================================================

dashboard_home()

# =========================================================
# MAIN LOOP
# =========================================================

root.mainloop()