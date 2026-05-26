import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import mysql.connector

# =========================================================
# MYSQL DATABASE CONNECTION
# =========================================================

con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="nive2530",
    database="hospitals_db"
)

cursor = con.cursor()

# =========================================================
# LOGIN FUNCTION
# =========================================================

def login_system():

    username = username_entry.get()
    password = password_entry.get()

    query = """
    SELECT * FROM users
    WHERE username=%s AND password=%s
    """

    cursor.execute(query, (username, password))

    result = cursor.fetchone()

    if result:

        messagebox.showinfo("Success", "Login Successful")

        login_window.destroy()

        main_window()

    else:

        messagebox.showerror("Error", "Invalid Username or Password")

# =========================================================
# MAIN WINDOW
# =========================================================

def main_window():

    root = tk.Tk()

    root.title("NTHV CarePulse Hospital Management System")

    root.geometry("1500x800")

    root.state("zoomed")

    # =====================================================
    # BACKGROUND IMAGE
    # =====================================================

    bg_image = Image.open("hospital_bg.jpg")

    bg_image = bg_image.resize((1500, 800))

    bg_photo = ImageTk.PhotoImage(bg_image)

    bg_label = tk.Label(root, image=bg_photo)

    bg_label.image = bg_photo

    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # =====================================================
    # TITLE
    # =====================================================

    title = tk.Label(
        root,
        text="NTHV CAREPULSE HOSPITAL MANAGEMENT SYSTEM",
        font=("Arial", 25, "bold"),
        bg="#170b3d",
        fg="white",
        pady=15
    )

    title.pack(fill="x")

    # =====================================================
    # NOTEBOOK
    # =====================================================

    notebook = ttk.Notebook(root)

    notebook.pack(fill="both", expand=True, padx=10, pady=10)

    # =====================================================
    # GENERIC CRUD TAB FUNCTION
    # =====================================================

    def create_crud_tab(tab_name, table_name, columns, bg_color):

        frame = tk.Frame(notebook, bg=bg_color)

        notebook.add(frame, text=tab_name)

        # =================================================
        # ENTRY FRAME
        # =================================================

        entry_frame = tk.Frame(frame, bg=bg_color)

        entry_frame.pack(fill="x", pady=10)

        entries = {}

        row = 0
        col = 0

        for column in columns:

            tk.Label(
                entry_frame,
                text=column,
                font=("Arial", 11, "bold"),
                bg=bg_color
            ).grid(row=row, column=col, padx=10, pady=10)

            # =============================================
            # GENDER DROPDOWN
            # =============================================

            if column.lower() == "gender":

                combo = ttk.Combobox(
                    entry_frame,
                    values=["Male", "Female", "Other"],
                    width=22,
                    state="readonly"
                )

                combo.grid(row=row, column=col + 1)

                entries[column] = combo

            # =============================================
            # BLOOD GROUP DROPDOWN
            # =============================================

            elif column.lower() == "blood_group":

                combo = ttk.Combobox(
                    entry_frame,
                    values=[
                        "A+",
                        "A-",
                        "B+",
                        "B-",
                        "AB+",
                        "AB-",
                        "O+",
                        "O-"
                    ],
                    width=22,
                    state="readonly"
                )

                combo.grid(row=row, column=col + 1)

                entries[column] = combo

            # =============================================
            # NORMAL ENTRY BOX
            # =============================================

            else:

                entry = tk.Entry(entry_frame, width=25)

                entry.grid(row=row, column=col + 1)

                entries[column] = entry

            row += 1

            if row == 5:

                row = 0

                col += 2

        # =================================================
        # TREEVIEW FRAME
        # =================================================

        tree_frame = tk.Frame(frame)

        tree_frame.pack(fill="both", expand=True)

        scroll_y = tk.Scrollbar(tree_frame, orient="vertical")

        tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            yscrollcommand=scroll_y.set
        )

        scroll_y.config(command=tree.yview)

        scroll_y.pack(side="right", fill="y")

        tree.pack(fill="both", expand=True)

        for column in columns:

            tree.heading(column, text=column)

            tree.column(column, width=150)

        # =================================================
        # FETCH DATA
        # =================================================

        def fetch_data():

            tree.delete(*tree.get_children())

            cursor.execute(f"SELECT * FROM {table_name}")

            rows = cursor.fetchall()

            for row_data in rows:

                tree.insert("", tk.END, values=row_data)

        fetch_data()

        # =================================================
        # INSERT DATA
        # =================================================

        def insert_data():

            values = []

            for column in columns:

                values.append(entries[column].get())

            placeholders = ",".join(["%s"] * len(columns))

            query = f"""
            INSERT INTO {table_name}
            VALUES ({placeholders})
            """

            try:

                cursor.execute(query, values)

                con.commit()

                messagebox.showinfo(
                    "Success",
                    "Record Inserted Successfully"
                )

                fetch_data()

                clear_data()

            except Exception as e:

                messagebox.showerror("Error", str(e))

        # =================================================
        # SELECT DATA
        # =================================================

        def select_data(event):

            selected = tree.focus()

            values = tree.item(selected, "values")

            if values:

                for i, column in enumerate(columns):

                    widget = entries[column]

                    if isinstance(widget, ttk.Combobox):

                        widget.set(values[i])

                    else:

                        widget.delete(0, tk.END)

                        widget.insert(0, values[i])

        tree.bind("<ButtonRelease-1>", select_data)

        # =================================================
        # UPDATE DATA
        # =================================================

        def update_data():

            values = []

            for column in columns:

                values.append(entries[column].get())

            update_query = ", ".join(
                [f"{column}=%s" for column in columns[1:]]
            )

            query = f"""
            UPDATE {table_name}
            SET {update_query}
            WHERE {columns[0]}=%s
            """

            final_values = values[1:] + [values[0]]

            try:

                cursor.execute(query, final_values)

                con.commit()

                messagebox.showinfo(
                    "Success",
                    "Record Updated Successfully"
                )

                fetch_data()

                clear_data()

            except Exception as e:

                messagebox.showerror("Error", str(e))

        # =================================================
        # DELETE DATA
        # =================================================

        def delete_data():

            record_id = entries[columns[0]].get()

            query = f"""
            DELETE FROM {table_name}
            WHERE {columns[0]}=%s
            """

            try:

                cursor.execute(query, (record_id,))

                con.commit()

                messagebox.showinfo(
                    "Success",
                    "Record Deleted Successfully"
                )

                fetch_data()

                clear_data()

            except Exception as e:

                messagebox.showerror("Error", str(e))

        # =================================================
        # CLEAR FUNCTION
        # =================================================

        def clear_data():

            for column in columns:

                widget = entries[column]

                if isinstance(widget, ttk.Combobox):

                    widget.set("")

                else:

                    widget.delete(0, tk.END)

        # =================================================
        # BUTTON FRAME
        # =================================================

        button_frame = tk.Frame(frame, bg=bg_color)

        button_frame.pack(pady=10)

        tk.Button(
            button_frame,
            text="INSERT",
            width=15,
            bg="#985983",
            fg="white",
            font=("Arial", 11, "bold"),
            command=insert_data
        ).grid(row=0, column=0, padx=10)

        tk.Button(
            button_frame,
            text="UPDATE",
            width=15,
            bg="#3c3442",
            fg="white",
            font=("Arial", 11, "bold"),
            command=update_data
        ).grid(row=0, column=1, padx=10)

        tk.Button(
            button_frame,
            text="DELETE",
            width=15,
            bg="#635b8f",
            fg="white",
            font=("Arial", 11, "bold"),
            command=delete_data
        ).grid(row=0, column=2, padx=10)

        tk.Button(
            button_frame,
            text="CLEAR",
            width=15,
            bg="#28185a",
            fg="white",
            font=("Arial", 11, "bold"),
            command=clear_data
        ).grid(row=0, column=3, padx=10)

    # =====================================================
    # PATIENT TAB
    # =====================================================

    create_crud_tab(
        "Patients",
        "patient_s",
        [
            "patient_id",
            "patient_name",
            "age",
            "gender",
            "phone",
            "address",
            "blood_group",
            "disease",
            "date_registered"
        ],
        "lightblue"
    )

    # =====================================================
    # DOCTOR TAB
    # =====================================================

    create_crud_tab(
        "Doctors",
        "doctors",
        [
            "doctor_id",
            "doctor_name",
            "specialization",
            "phone",
            "email",
            "salary"
        ],
        "lightgreen"
    )

    # =====================================================
    # APPOINTMENT TAB
    # =====================================================

    create_crud_tab(
        "Appointments",
        "appointments",
        [
            "appointment_id",
            "patient_id",
            "doctor_id",
            "appointment_date",
            "appointment_time",
            "status"
        ],
        "lightyellow"
    )

    # =====================================================
    # BILLING TAB
    # =====================================================

    create_crud_tab(
        "Billing",
        "billing",
        [
            "bill_id",
            "patient_id",
            "total_amount",
            "payment_status",
            "bill_date"
        ],
        "lightpink"
    )

    # =====================================================
    # MEDICINE TAB
    # =====================================================

    create_crud_tab(
        "Medicines",
        "medicines",
        [
            "medicine_id",
            "medicine_name",
            "company",
            "price",
            "stock",
            "expiry_date"

        ],
        "lightcyan"
    )

    # =====================================================
    # PRESCRIPTION TAB
    # =====================================================

    create_crud_tab(
        "Prescriptions",
        "prescriptions",
        [
            "prescription_id",
            "patient_id",
            "doctor_id",
            "medicine_id",
            "dosage",
            "prescription_date"
        ],
        "lavender"
    )

    # =====================================================
    # ROOM TAB
    # =====================================================

    create_crud_tab(
        "Rooms",
        "rooms",
        [
            "room_id",
            "room_number",
            "room_type",
            "status"
        ],
        "beige"
    )

    # =====================================================
    # ADMISSION TAB
    # =====================================================

    create_crud_tab(
        "Admissions",
        "admissions",
        [
            "admission_id",
            "patient_id",
            "room_id",
            "admission_date",
            "discharge_date"
        ],
        "mistyrose"
    )

    root.mainloop()

# =========================================================
# LOGIN WINDOW
# =========================================================

login_window = tk.Tk()

login_window.title("Hospital Login")

login_window.geometry("700x500")

# =========================================================
# LOGIN BACKGROUND IMAGE
# =========================================================

bg = Image.open("hospital_login.jpg")

bg = bg.resize((700, 500))

bg_photo = ImageTk.PhotoImage(bg)

bg_label = tk.Label(login_window, image=bg_photo)

bg_label.image = bg_photo

bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# =========================================================
# LOGIN TITLE
# =========================================================

title = tk.Label(
    login_window,
    text="NTHV HOSPITAL LOGIN",
    font=("Arial", 24, "bold"),
    bg="white",
    fg="darkblue"
)

title.pack(pady=30)

# =========================================================
# USERNAME
# =========================================================

tk.Label(
    login_window,
    text="Username",
    font=("Arial", 12, "bold"),
    bg="white"
).pack()

username_entry = tk.Entry(
    login_window,
    width=30,
    font=("Arial", 12)
)

username_entry.pack(pady=10)

# =========================================================
# PASSWORD
# =========================================================

tk.Label(
    login_window,
    text="Password",
    font=("Arial", 12, "bold"),
    bg="white"
).pack()

password_entry = tk.Entry(
    login_window,
    width=30,
    show="*",
    font=("Arial", 12)
)

password_entry.pack(pady=10)

# =========================================================
# LOGIN BUTTON
# =========================================================

login_btn = tk.Button(
    login_window,
    text="LOGIN",
    width=20,
    bg="#170b3d",
    fg="white",
    font=("Arial", 12, "bold"),
    command=login_system
)

login_btn.pack(pady=30)

login_window.mainloop()