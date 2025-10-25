# create_tables.py
from database.db_connection import DatabaseConnection

def create_tables():
    db = DatabaseConnection()
    connection = db.connect()
    
    if connection:
        cursor = connection.cursor()
        
        try:
            # Students table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    student_id INT AUTO_INCREMENT PRIMARY KEY,
                    first_name VARCHAR(50) NOT NULL,
                    last_name VARCHAR(50) NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    phone VARCHAR(15),
                    date_of_birth DATE NOT NULL,
                    address TEXT,
                    enrollment_date DATE NOT NULL,
                    major VARCHAR(100),
                    status ENUM('Active', 'Inactive', 'Graduated') DEFAULT 'Active',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Academic records table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS academic_records (
                    record_id INT AUTO_INCREMENT PRIMARY KEY,
                    student_id INT,
                    semester VARCHAR(20) NOT NULL,
                    course_code VARCHAR(20) NOT NULL,
                    course_name VARCHAR(100) NOT NULL,
                    credits INT NOT NULL,
                    grade VARCHAR(2) NOT NULL,
                    gpa DECIMAL(3,2),
                    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
                )
            """)
            
            # Attendance table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS attendance (
                    attendance_id INT AUTO_INCREMENT PRIMARY KEY,
                    student_id INT,
                    date DATE NOT NULL,
                    status ENUM('Present', 'Absent', 'Late') NOT NULL,
                    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
                )
            """)
            
            connection.commit()
            print("✅ Database tables created successfully!")
            
        except Error as e:
            print(f"❌ Error creating tables: {e}")
        finally:
            cursor.close()
            db.disconnect()

if __name__ == "__main__":
    create_tables()