import re
from datetime import datetime, date

class Validators:
    @staticmethod
    def validate_email(email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_phone(phone):
        pattern = r'^\+?1?\d{9,15}$'
        return re.match(pattern, phone) is not None
    
    @staticmethod
    def validate_name(name):
        return len(name) >= 2 and name.replace(' ', '').isalpha()
    
    @staticmethod
    def validate_date(date_str):
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return True
        except ValueError:
            return False
    
    @staticmethod
    def calculate_age(birth_date):
        today = date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        return age
    
    @staticmethod
    def validate_student_data(student_data):
        errors = []
        
        if not Validators.validate_name(student_data['first_name']):
            errors.append("First name must be at least 2 characters and contain only letters")
        
        if not Validators.validate_name(student_data['last_name']):
            errors.append("Last name must be at least 2 characters and contain only letters")
        
        if not Validators.validate_email(student_data['email']):
            errors.append("Invalid email format")
        
        if student_data['phone'] and not Validators.validate_phone(student_data['phone']):
            errors.append("Invalid phone number format")
        
        if not Validators.validate_date(str(student_data['date_of_birth'])):
            errors.append("Invalid date format (YYYY-MM-DD)")
        else:
            age = Validators.calculate_age(student_data['date_of_birth'])
            if age < 15 or age > 80:
                errors.append("Student age must be between 15 and 80 years")
        
        return errors
