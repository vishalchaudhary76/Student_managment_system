
import tkinter as tk
from tkinter import ttk, messagebox
from database.db_connection import DatabaseConnection
from models.student import Student
from utils.validators import Validators

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management System - EASYLIST")
        self.root.geometry("1200x700")
        
        self.db = DatabaseConnection()
        self.connection = self.db.connect()
        
        self.setup_ui()
        self.load_students()
    
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Search and Filter Section
        search_frame = ttk.LabelFrame(main_frame, text="Search & Filter", padding="10")
        search_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(search_frame, text="Search:").grid(row=0, column=0, sticky=tk.W)
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30)
        self.search_entry.grid(row=0, column=1, padx=(5, 0))
        self.search_entry.bind('<KeyRelease>', self.search_students)
        
        ttk.Label(search_frame, text="Filter by:").grid(row=0, column=2, padx=(20, 5))
        self.filter_var = tk.StringVar(value="All")
        filter_combo = ttk.Combobox(search_frame, textvariable=self.filter_var, 
                                   values=["All", "Active", "Inactive", "Graduated"],
                                   state="readonly", width=15)
        filter_combo.grid(row=0, column=3, padx=(5, 0))
        filter_combo.bind('<<ComboboxSelected>>', self.filter_students)
        
        # Students Table
        table_frame = ttk.LabelFrame(main_frame, text="Students", padding="10")
        table_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        columns = ('ID', 'First Name', 'Last Name', 'Email', 'Phone', 'Major', 'Status')
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        # Define headings
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        
        self.tree.column('ID', width=50)
        self.tree.column('Email', width=200)
        
        # Scrollbar for table
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Buttons Frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Add Student", command=self.add_student).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Edit Student", command=self.edit_student).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Delete Student", command=self.delete_student).grid(row=0, column=2, padx=5)
        ttk.Button(button_frame, text="View Academic Records", command=self.view_academic_records).grid(row=0, column=3, padx=5)
        ttk.Button(button_frame, text="Generate Reports", command=self.generate_reports).grid(row=0, column=4, padx=5)
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)
    
    def load_students(self, query=None, params=None):
        try:
            cursor = self.connection.cursor(dictionary=True)
            
            if query:
                cursor.execute(query, params)
            else:
                cursor.execute("SELECT * FROM students ORDER BY student_id")
            
            students = cursor.fetchall()
            
            # Clear existing data
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Insert new data
            for student in students:
                self.tree.insert('', tk.END, values=(
                    student['student_id'],
                    student['first_name'],
                    student['last_name'],
                    student['email'],
                    student['phone'],
                    student['major'],
                    student['status']
                ))
            
            cursor.close()
            
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to load students: {str(e)}")
    
    def search_students(self, event=None):
        search_term = self.search_var.get()
        filter_status = self.filter_var.get()
        
        query = """
            SELECT * FROM students 
            WHERE (first_name LIKE %s OR last_name LIKE %s OR email LIKE %s OR major LIKE %s)
        """
        params = [f"%{search_term}%"] * 4
        
        if filter_status != "All":
            query += " AND status = %s"
            params.append(filter_status)
        
        query += " ORDER BY student_id"
        self.load_students(query, params)
    
    def filter_students(self, event=None):
        self.search_students()
    
    def add_student(self):
        # Open student form in add mode
        self.open_student_form()
    
    def edit_student(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a student to edit")
            return
        
        student_id = self.tree.item(selected_item[0])['values'][0]
        self.open_student_form(student_id)
    
    def open_student_form(self, student_id=None):
        # This would open a new window with student form
        # Implementation details for student form window
        pass
    
    def delete_student(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a student to delete")
            return
        
        student_id = self.tree.item(selected_item[0])['values'][0]
        student_name = f"{self.tree.item(selected_item[0])['values'][1]} {self.tree.item(selected_item[0])['values'][2]}"
        
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {student_name}?"):
            try:
                cursor = self.connection.cursor()
                cursor.execute("DELETE FROM students WHERE student_id = %s", (student_id,))
                self.connection.commit()
                cursor.close()
                
                messagebox.showinfo("Success", "Student deleted successfully")
                self.load_students()
                
            except Exception as e:
                messagebox.showerror("Database Error", f"Failed to delete student: {str(e)}")
    
    def view_academic_records(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a student to view records")
            return
        
        student_id = self.tree.item(selected_item[0])['values'][0]
        # Open academic records window for this student
        pass
    
    def generate_reports(self):
        # Open reports generation window
        pass
    
    def __del__(self):
        if hasattr(self, 'db'):
            self.db.disconnect()
