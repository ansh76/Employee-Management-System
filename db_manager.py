import sqlite3
from sqlite3 import Error

class DatabaseManager:
    """
    Handles all interactions with the SQLite database, including connection, 
    table creation, and parameterized CRUD operations.
    """
    
    def __init__(self, db_file="employee_data.db"):
        self.db_file = db_file
        self.conn = None
        self.cursor = None
        self._connect()
        self._create_table()

    def _connect(self):
        """Creates a database connection to the SQLite database specified by db_file."""
        try:
            self.conn = sqlite3.connect(self.db_file)
            self.cursor = self.conn.cursor()
        except Error as e:
            print(f"Database connection error: {e}")
            self.conn = None
            self.cursor = None

    def _create_table(self):
        """Creates the employees table if it does not exist."""
        if self.conn:
            try:
                self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS employees (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        email TEXT UNIQUE NOT NULL,
                        phone TEXT,
                        designation TEXT,
                        salary REAL NOT NULL
                    );
                """)
                self.conn.commit()
            except Error as e:
                print(f"Error creating table: {e}")

    def close(self):
        """Closes the database connection."""
        if self.conn:
            self.conn.close()

    # --- CRUD Operations ---

    def add_employee(self, name, email, phone, designation, salary):
        """Inserts a new employee record using parameterized query."""
        if not self.conn: return False

        sql = """
            INSERT INTO employees (name, email, phone, designation, salary) 
            VALUES (?, ?, ?, ?, ?)
        """
        try:
            self.cursor.execute(sql, (name, email, phone, designation, salary))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            print("\n[DB Error] Failed to add employee. An employee with this email already exists.")
            return False
        except Error as e:
            print(f"\n[DB Error] Failed to add employee: {e}")
            return False

    def get_all_employees(self):
        """Retrieves all employee records."""
        if not self.conn: return []
        
        sql = "SELECT id, name, email, phone, designation, salary FROM employees ORDER BY id"
        try:
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except Error as e:
            print(f"\n[DB Error] Failed to retrieve employees: {e}")
            return []

    def search_employee(self, search_term):
        """Searches employees by ID (exact match) or Name (partial, case-insensitive match)."""
        if not self.conn: return []

        try:
            # Check if search_term is a numeric ID
            if search_term.isdigit():
                # Search by ID (exact match)
                sql = "SELECT id, name, email, phone, designation, salary FROM employees WHERE id = ?"
                self.cursor.execute(sql, (int(search_term),))
                result = self.cursor.fetchall()
                if result:
                    return result

            # Search by Name (partial, case-insensitive match using LIKE and parameterized query)
            sql = "SELECT id, name, email, phone, designation, salary FROM employees WHERE name LIKE ?"
            self.cursor.execute(sql, (f'%{search_term}%',))
            return self.cursor.fetchall()

        except Error as e:
            print(f"\n[DB Error] Failed to search employee: {e}")
            return []

    def update_employee(self, emp_id, data):
        """Updates employee details (email, phone, designation, salary) for a given ID."""
        if not self.conn: return False

        set_clauses = [f"{key} = ?" for key in data.keys()]
        values = list(data.values())
        values.append(emp_id)
        
        sql = f"UPDATE employees SET {', '.join(set_clauses)} WHERE id = ?"
        
        try:
            self.cursor.execute(sql, values)
            self.conn.commit()
            return self.cursor.rowcount > 0
        except sqlite3.IntegrityError:
            print("\n[DB Error] Failed to update employee. The new email might already be in use.")
            return False
        except Error as e:
            print(f"\n[DB Error] Failed to update employee: {e}")
            return False

    def delete_employee(self, emp_id):
        """Deletes an employee record by ID."""
        if not self.conn: return False

        sql = "DELETE FROM employees WHERE id = ?"
        try:
            self.cursor.execute(sql, (emp_id,))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except Error as e:
            print(f"\n[DB Error] Failed to delete employee: {e}")
            return False

    def get_employee_by_id(self, emp_id):
        """Checks if an employee ID exists and returns the record."""
        if not self.conn: return None
        
        sql = "SELECT id, name, email, phone, designation, salary FROM employees WHERE id = ?"
        try:
            self.cursor.execute(sql, (emp_id,))
            return self.cursor.fetchone()
        except Error as e:
            print(f"\n[DB Error] Failed to retrieve employee by ID: {e}")
            return None
