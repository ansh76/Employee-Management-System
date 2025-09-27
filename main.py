import sys
from db_manager import DatabaseManager
from validator import (
    validate_name, validate_email, validate_phone, 
    validate_designation, validate_salary, validate_employee_id, 
    get_validation_error
)
from tabulate import tabulate

# Global database manager instance
db = DatabaseManager()
HEADERS = ["ID", "Name", "Email", "Phone", "Designation", "Salary"]

def get_valid_input(prompt, validator_func, field_name):
    """
    Utility function to repeatedly prompt the user until valid input is provided.
    """
    while True:
        try:
            user_input = input(f"Enter {prompt}: ").strip()
            if validator_func(user_input):
                # Special handling for salary to convert to float
                if field_name == 'salary':
                    return float(user_input)
                # Special handling for ID to convert to int
                if field_name == 'id':
                    return int(user_input)
                return user_input
            else:
                print(f"[Validation Error] {get_validation_error(field_name)}")
        except EOFError:
            print("\nInput interrupted. Returning to main menu.")
            return None
        except Exception as e:
            # Catches unexpected type errors during conversion/validation
            print(f"[Internal Error] An unexpected error occurred: {e}")
            return None

def display_menu():
    """Displays the main CLI menu options."""
    print("\n" + "="*50)
    print("      EMPLOYEE MANAGEMENT SYSTEM (SQLite)       ")
    print("="*50)
    print("1. Add New Employee")
    print("2. View All Employees")
    print("3. Search Employee (by ID or Name)")
    print("4. Update Employee Details")
    print("5. Delete Employee Record")
    print("6. Exit")
    print("="*50)

def display_records(records):
    """Displays employee records in a clean tabular format."""
    if not records:
        print("\n[INFO] No records found.")
        return

    # Format salary column for better readability
    formatted_records = []
    for record in records:
        # Convert salary (index 5) to a formatted string
        record_list = list(record)
        record_list[5] = f"${record_list[5]:,.2f}"
        formatted_records.append(record_list)

    print("\n--- Employee Records ---")
    print(tabulate(formatted_records, headers=HEADERS, tablefmt="fancy_grid"))

def handle_add_employee():
    """Handles the process of creating a new employee record."""
    print("\n--- ADD NEW EMPLOYEE ---")
    
    # Collect and validate all required inputs
    name = get_valid_input("Employee Name", validate_name, 'name')
    if name is None: return

    email = get_valid_input("Email Address", validate_email, 'email')
    if email is None: return

    phone = get_valid_input("Phone Number", validate_phone, 'phone')
    if phone is None: return

    designation = get_valid_input("Designation", validate_designation, 'designation')
    if designation is None: return

    salary = get_valid_input("Salary", validate_salary, 'salary') # Returns float
    if salary is None: return

    # Attempt to add to database
    if db.add_employee(name, email, phone, designation, salary):
        print(f"\n[SUCCESS] Employee '{name}' added successfully.")

def handle_view_all_employees():
    """Handles viewing all employee records."""
    records = db.get_all_employees()
    display_records(records)

def handle_search_employee():
    """Handles searching for employee records by ID or Name."""
    search_term = input("\nEnter Employee ID or Name to search: ").strip()
    
    if not search_term:
        print("[WARNING] Search term cannot be empty.")
        return

    records = db.search_employee(search_term)
    display_records(records)

def handle_update_employee():
    """Handles updating details for an existing employee."""
    print("\n--- UPDATE EMPLOYEE DETAILS ---")
    
    # 1. Get and validate ID
    while True:
        emp_id_str = input("Enter Employee ID to update: ").strip()
        if not validate_employee_id(emp_id_str):
            print(f"[Validation Error] {get_validation_error('id')}")
            continue

        emp_id = int(emp_id_str)
        if not db.get_employee_by_id(emp_id):
            print(f"[ERROR] Employee with ID {emp_id} not found.")
            return

        break

    # 2. Get and validate fields to update
    update_data = {}
    
    # New Email
    new_email = input("Enter NEW Email (or leave blank to keep current): ").strip()
    if new_email:
        if validate_email(new_email):
            update_data['email'] = new_email
        else:
            print(f"[Validation Error] New email: {get_validation_error('email')}")
            return
            
    # New Phone
    new_phone = input("Enter NEW Phone Number (or leave blank to keep current): ").strip()
    if new_phone:
        if validate_phone(new_phone):
            update_data['phone'] = new_phone
        else:
            print(f"[Validation Error] New phone: {get_validation_error('phone')}")
            return

    # New Designation
    new_designation = input("Enter NEW Designation (or leave blank to keep current): ").strip()
    if new_designation:
        if validate_designation(new_designation):
            update_data['designation'] = new_designation
        else:
            print(f"[Validation Error] New designation: {get_validation_error('designation')}")
            return

    # New Salary
    new_salary_str = input("Enter NEW Salary (or leave blank to keep current): ").strip()
    if new_salary_str:
        if validate_salary(new_salary_str):
            update_data['salary'] = float(new_salary_str)
        else:
            print(f"[Validation Error] New salary: {get_validation_error('salary')}")
            return

    if not update_data:
        print("[INFO] No fields were entered for update. Operation cancelled.")
        return

    # 3. Perform update
    if db.update_employee(emp_id, update_data):
        print(f"\n[SUCCESS] Employee ID {emp_id} updated successfully.")
    else:
        print(f"\n[ERROR] Failed to update employee ID {emp_id}.")

def handle_delete_employee():
    """Handles deleting an employee record by ID."""
    print("\n--- DELETE EMPLOYEE RECORD ---")
    
    # 1. Get and validate ID
    while True:
        emp_id_str = input("Enter Employee ID to DELETE: ").strip()
        if not validate_employee_id(emp_id_str):
            print(f"[Validation Error] {get_validation_error('id')}")
            continue

        emp_id = int(emp_id_str)
        
        # Check if ID exists
        employee = db.get_employee_by_id(emp_id)
        if not employee:
            print(f"[ERROR] Employee with ID {emp_id} not found.")
            return

        # Confirmation prompt
        print(f"\n[WARNING] You are about to delete record for: {employee[1]} (ID: {employee[0]})")
        confirm = input("Are you sure you want to proceed? (yes/no): ").strip().lower()

        if confirm == 'yes':
            # 2. Perform deletion
            if db.delete_employee(emp_id):
                print(f"\n[SUCCESS] Employee ID {emp_id} deleted successfully.")
            else:
                print(f"\n[ERROR] Failed to delete employee ID {emp_id}.")
            return
        elif confirm == 'no':
            print("\n[INFO] Deletion cancelled.")
            return
        else:
            print("[WARNING] Invalid confirmation. Please enter 'yes' or 'no'.")
            continue


def main():
    """Main function to run the CLI application."""
    if not db.conn:
        print("[CRITICAL ERROR] Application failed to connect to the database. Exiting.")
        sys.exit(1)

    while True:
        display_menu()
        
        try:
            choice = input("Enter your choice (1-6): ").strip()
        except EOFError:
            print("\nInput interrupted. Exiting program.")
            break
        
        if choice == '1':
            handle_add_employee()
        elif choice == '2':
            handle_view_all_employees()
        elif choice == '3':
            handle_search_employee()
        elif choice == '4':
            handle_update_employee()
        elif choice == '5':
            handle_delete_employee()
        elif choice == '6':
            print("\nThank you for using the Employee Management System. Goodbye!")
            break
        else:
            print("\n[WARNING] Invalid choice. Please enter a number between 1 and 6.")
        
    db.close()

if __name__ == "__main__":
    main()
