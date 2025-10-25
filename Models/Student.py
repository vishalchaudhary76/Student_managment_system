class Student:
    def __init__(self, student_id=None, first_name="", last_name="", email="", 
                 phone="", date_of_birth=None, address="", enrollment_date=None, 
                 major="", status="Active"):
        self.student_id = student_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.date_of_birth = date_of_birth
        self.address = address
        self.enrollment_date = enrollment_date
        self.major = major
        self.status = status
    
    def to_dict(self):
        return {
            'student_id': self.student_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone': self.phone,
            'date_of_birth': self.date_of_birth,
            'address': self.address,
            'enrollment_date': self.enrollment_date,
            'major': self.major,
            'status': self.status
        }
