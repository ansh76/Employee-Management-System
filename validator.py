import re

# Regex patterns for input validation
# Note: These are simple validations and can be made more strict if required.
NAME_REGEX = r"^[A-Za-z\s]{3,50}$"
EMAIL_REGEX = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
PHONE_REGEX = r"^\+?\d{10,15}$" # Simple check for 10-15 digits, optionally starting with +
DESIGNATION_REGEX = r"^[A-Za-z\s,-]{3,50}$"

def validate_name(name):
    """Validates employee name."""
    return bool(re.fullmatch(NAME_REGEX, name))

def validate_email(email):
    """Validates email format."""
    return bool(re.fullmatch(EMAIL_REGEX, email))

def validate_phone(phone):
    """Validates phone number format."""
    return bool(re.fullmatch(PHONE_REGEX, phone))

def validate_designation(designation):
    """Validates designation string."""
    return bool(re.fullmatch(DESIGNATION_REGEX, designation))

def validate_salary(salary_str):
    """Validates that the salary is a positive numeric value."""
    try:
        salary = float(salary_str)
        return salary > 0
    except ValueError:
        return False

def validate_employee_id(id_str):
    """Validates that the employee ID is a positive integer."""
    try:
        emp_id = int(id_str)
        return emp_id > 0
    except ValueError:
        return False

# Mapping for user-friendly validation messages
VALIDATION_MAP = {
    'name': "Name must contain 3-50 letters and spaces only.",
    'email': "Invalid email format (e.g., user@domain.com).",
    'phone': "Invalid phone number (10-15 digits, optional '+').",
    'designation': "Designation must contain 3-50 letters, spaces, hyphens, or commas.",
    'salary': "Salary must be a positive number.",
    'id': "ID must be a positive integer."
}

def get_validation_error(field):
    """Returns the user-friendly error message for a failed validation."""
    return VALIDATION_MAP.get(field, "Invalid input format.")
