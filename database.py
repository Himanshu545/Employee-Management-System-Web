import sqlite3


def create_database():

    conn = sqlite3.connect("database/employee.db")

    cursor = conn.cursor()

    # ================= Employees =================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS employees(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        name TEXT NOT NULL,

        age INTEGER NOT NULL,

        gender TEXT NOT NULL,

        department TEXT NOT NULL,

        designation TEXT NOT NULL,

        salary REAL NOT NULL,

        phone TEXT NOT NULL,

        email TEXT UNIQUE NOT NULL

    )
    """)

    # ================= Admin =================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS admin(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        username TEXT UNIQUE NOT NULL,

        password TEXT NOT NULL

    )
    """)

    cursor.execute("""
    INSERT OR IGNORE INTO admin(username, password)

    VALUES('admin', 'admin123')
    """)

    # ================= Attendance =================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance(

        attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,

        employee_id INTEGER NOT NULL,

        attendance_date TEXT NOT NULL,

        status TEXT NOT NULL,

        FOREIGN KEY(employee_id) REFERENCES employees(id)

    )
    """)

    # ================= Payroll =================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS payroll(

        payroll_id INTEGER PRIMARY KEY AUTOINCREMENT,

        employee_id INTEGER NOT NULL,

        basic_salary REAL NOT NULL,

        bonus REAL DEFAULT 0,

        deduction REAL DEFAULT 0,

        net_salary REAL NOT NULL,

        payroll_date TEXT NOT NULL,

        FOREIGN KEY(employee_id) REFERENCES employees(id)

    )
    """)
    # ================= Leave =================

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS leaves(

        leave_id INTEGER PRIMARY KEY AUTOINCREMENT,

        employee_id INTEGER NOT NULL,

        leave_type TEXT NOT NULL,

        start_date TEXT NOT NULL,

        end_date TEXT NOT NULL,

        reason TEXT NOT NULL,

        status TEXT DEFAULT 'Pending',

        FOREIGN KEY(employee_id)

        REFERENCES employees(id)

    )

    """)
    
    conn.commit()

    conn.close()