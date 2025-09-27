# 📁 Employee Management System (CLI)

## 🌟 Project Overview
This is a robust **Command-Line Interface (CLI)** application developed in **Python** to efficiently manage employee records for an organization.  
The system supports full **CRUD (Create, Read, Update, Delete)** operations, ensuring reliable and secure data handling through a relational database.

The focus is on:
- **Data Integrity** → Ensured using Regular Expressions for validation.  
- **Security** → Uses parameterized SQL queries to prevent SQL Injection.  
- **Usability** → User-friendly CLI menus with tabular output.  

---

## ✨ Key Features
- **CRUD Operations** → Add, View, Search, Update, and Delete employee records.  
- **Persistent Storage** → Employee data is stored in SQLite and remains intact between sessions.  
- **Input Validation** → Email, phone, salary, etc., validated using Python’s `re` library.  
- **Security** → Uses parameterized queries for all DB operations.  
- **Tabular Output** → Uses the `tabulate` library for clean table display.  
- **Error Handling** → Handles invalid inputs and runtime errors gracefully.  

---

## 🛠️ Tech Stack

| Category         | Technology          | Purpose                                          |
|------------------|--------------------|--------------------------------------------------|
| Language         | Python (3.x)       | Core application logic                           |
| Database         | SQLite3            | Persistent, file-based relational data storage   |
| Validation       | re (Regex)         | Pattern matching for email, phone, etc.          |
| Output Formatting| tabulate           | Displaying records in clean table format         |
| DB Connector     | sqlite3 (Built-in) | Managing DB connections and SQL execution        |

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.x installed on your system.

### 1. Clone the Repository
```bash
git clone https://github.com/ansh76/Employee-Management-System.git
cd Employee-Management-System
