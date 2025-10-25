
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from database.db_connection import DatabaseConnection
from utils.validators import Validators

class StudentForm:
    def __init__(self, parent, student_id=None):
        self.parent = parent
        self.student_id = student_id
        self.db = DatabaseConnection()
        self.connection = self.db.connect()
        
        self.setup_form()
        if student_id:
            self.load_student_data()
    
    def setup_form(self):
        self.form_window = tk.Toplevel(self.parent)
        self.form_window.title("Add Student" if not self.student_id else "Edit Student")
        self.form_window.geometry("500x400")
        self.form_window.resizable(False, False)
        
        # Form fields
        main_frame = ttk.Frame(self.form_window, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # First Name
        ttk.Label(main_frame, text="First Name *:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.first_name = ttk.Entry(main_frame, width=30)
        self.first_name.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        # Last Name
        ttk.Label(main_frame, text="Last Name *:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.last_name = ttk.Entry(main_frame, width=30)
        self.last_name.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        # Email
        ttk.Label(main_frame, text="Email *:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.email = ttk.Entry(main_frame, width=30)
        self.email.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        # Phone
        ttk.Label(main_frame, text="Phone:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.phone = ttk.Entry(main_frame, width=30)
        self.phone.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        # Date of Birth
        ttk.Label(main_frame, text="Date of Birth *:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.dob = ttk.Entry(main_frame, width=30)
        self.dob.grid(row=4, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        ttk.Label(main_frame, text="(YYYY-MM-DD)").grid(row=4, column=2, sticky=tk.W, pady=5, padx=(5, 0))
        
        # Address
        ttk.Label(main_frame, text="Address:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.address = tk.Text(main_frame, width=30, height=4)
        self.address.grid(row=5, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        # Major
        ttk.Label(main_frame, text="Major:").grid(row=6, column=0, sticky=tk.W, pady=5)
        self.major = ttk.Entry(main_frame, width=30)
        self.major.grid(row=6, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        # Status
        ttk.Label(main_frame, text="Status:").grid(row=7, column=0, sticky=tk.W, pady=5)
        self.status = ttk.Combobox(main_frame, values=["Active", "Inactive", "Graduated"], state="readonly")
        self.status.set("Active")
        self.status.grid(row=7, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=8, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Save", command=self.save_student).grid(row=0, column=0, padx=10)
        ttk.Button(button_frame, text="Cancel", command=self.form_window.destroy).grid(row=0, column=1, padx=10)
        
        # Configure grid weights
        main_frame.columnconfigure(1, weight=1)
        self.form_window.columnconfigure(0, weight=1)
        self.form_window.rowconfigure(0, weight=1)
    
    def load_student_data(self):
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM students WHERE student_id = %s", (self.student_id,))
            student = cursor.fetchone()
            cursor.close()
            
            if student:
                self.first_name.insert(0, student['first_name'])
                self.last_name.insert(0, student['last_name'])
                self.email.insert(0, student['email'])
                if student['phone']:
                    self.phone.insert(0, student['phone'])
                self.dob.insert(0, str(student['date_of_birth']))
                if student['address']:
                    self.address.insert('1.0', student['address'])
                if student['major']:
                    self.major.insert(0, student['major'])
                self.status.set(student['status'])
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load student data: {str(e)}")
    
    def save_student(self):
        # Collect data from form
        student_data = {
            'first_name': self.first_name.get().strip(),
            'last_name': self.last_name.get().strip(),
            'email': self.email.get().strip(),
            'phone': self.phone.get().strip(),
            'date_of_birth': self.dob.get().strip(),
            'address': self.address.get('1.0', tk.END).strip(),
            'major': self.major.get().strip(),
            'status': self.status.get()
        }
        
        # Validate data
        errors = Validators.validate_student_data(student_data)
        if errors:
            messagebox.showerror("Validation Error", "\n".join(errors))
            return
        
        try:
            cursor = self.connection.cursor()
            
            if self.student_id:
                # Update existing student
                query = """
                    UPDATE students SET first_name=%s, last_name=%s, email=%s, phone=%s, 
                    date_of_birth=%s, address=%s, major=%s, status=%s 
                    WHERE student_id=%s
                """
                params = (
                    student_data['first_name'], student_data['last_name'], student_data['email'],
                    student_data['phone'] or None, student_data['date_of_birth'],
                    student_data['address'] or None, student_data['major'] or None,
                    student_data['status'], self.student_id
                )
            else:
                # Insert new student
                query = """
                    INSERT INTO students (first_name, last_name, email, phone, date_of_birth, 
                    address, major, status, enrollment_date) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                params = (
                    student_data['first_name'], student_data['last_name'], student_data['email'],
                    student_data['phone'] or None, student_data['date_of_birth'],
                    student_data['address'] or None, student_data['major'] or None,
                    student_data['status'], datetime.now().date()
                )
            
            cursor.execute(query, params)
            self.connection.commit()
            cursor.close()
            
            messagebox.showinfo("Success", "Student saved successfully")
            self.form_window.destroy()
            
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to save student: {str(e)}")
    
    def __del__(self):
        if hasattr(self, 'db'):
            self.db.disconnect()
