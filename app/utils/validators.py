import re

def is_valid_email(email):
    """Check if email format is valid using Regex."""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def validate_student_data(data, is_update=False):
    """
    Validate student data against business rules.
    Returns: (bool, str) -> (is_valid, error_message)
    """
    # 1. Validate required fields (only if it is a new creation)
    required_fields = ['first_name', 'last_name', 'email', 'major', 'enrollment_date']
    if not is_update:
        for field in required_fields:
            if field not in data:
                return False, f"Missing required field: {field}"

    # 2. Validate Email
    if 'email' in data:
        if not is_valid_email(data['email']):
            return False, "Invalid email format"

    # 3. Validate GPA (0.0 - 4.0)
    if 'gpa' in data and data['gpa'] is not None:
        try:
            gpa = float(data['gpa'])
            if not (0.0 <= gpa <= 4.0):
                return False, "GPA must be between 0.0 and 4.0"
        except ValueError:
            return False, "GPA must be a number"

    # 4. Validate Semester (1 - 12)
    if 'semester' in data and data['semester'] is not None:
        try:
            semester = int(data['semester'])
            if not (1 <= semester <= 12):
                return False, "Semester must be between 1 and 12"
        except ValueError:
            return False, "Semester must be an integer"

    return True, None