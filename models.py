import sqlite3
from config import Config


class EmployeeModel:

    # ==========================
    # Database Connection
    # ==========================

    @staticmethod
    def get_connection():

        conn = sqlite3.connect(Config.DATABASE)

        conn.row_factory = sqlite3.Row

        return conn


    # ==========================
    # Admin Login
    # ==========================

    @staticmethod
    def admin_login(username, password):

        conn = EmployeeModel.get_connection()

        cursor = conn.cursor()

        cursor.execute("""

        SELECT *

        FROM admin

        WHERE username=?

        AND password=?

        """,

        (

            username,

            password

        ))

        admin = cursor.fetchone()

        conn.close()

        return admin


    # ==========================
    # Dashboard Statistics
    # ==========================

    @staticmethod
    def total_employees():

        conn = EmployeeModel.get_connection()

        cursor = conn.cursor()

        cursor.execute(

            "SELECT COUNT(*) FROM employees"

        )

        total = cursor.fetchone()[0]

        conn.close()

        return total


    @staticmethod
    def total_departments():

        conn = EmployeeModel.get_connection()

        cursor = conn.cursor()

        cursor.execute("""

        SELECT COUNT(DISTINCT department)

        FROM employees

        """)

        total = cursor.fetchone()[0]

        conn.close()

        return total


    @staticmethod
    def total_salary():

        conn = EmployeeModel.get_connection()

        cursor = conn.cursor()

        cursor.execute("""

        SELECT IFNULL(SUM(salary),0)

        FROM employees

        """)

        salary = cursor.fetchone()[0]

        conn.close()

        return salary


    # ==========================
    # Employee CRUD
    # ==========================

    @staticmethod
    def get_all():

        conn = EmployeeModel.get_connection()

        cursor = conn.cursor()

        cursor.execute("""

        SELECT *

        FROM employees

        ORDER BY id DESC

        """)

        employees = cursor.fetchall()

        conn.close()

        return employees


    @staticmethod
    def get_recent(limit=5):

        conn = EmployeeModel.get_connection()

        cursor = conn.cursor()

        cursor.execute("""

        SELECT *

        FROM employees

        ORDER BY id DESC

        LIMIT ?

        """,

        (limit,))

        employees = cursor.fetchall()

        conn.close()

        return employees


    @staticmethod
    def get_employee(emp_id):

        conn = EmployeeModel.get_connection()

        cursor = conn.cursor()

        cursor.execute("""

        SELECT *

        FROM employees

        WHERE id=?

        """,

        (emp_id,))

        employee = cursor.fetchone()

        conn.close()

        return employee


    @staticmethod
    def add_employee(data):

        conn = EmployeeModel.get_connection()

        cursor = conn.cursor()

        cursor.execute("""

        INSERT INTO employees

        (

        name,

        age,

        gender,

        department,

        designation,

        salary,

        phone,

        email

        )

        VALUES

        (?,?,?,?,?,?,?,?)

        """,

        (

            data["name"],

            data["age"],

            data["gender"],

            data["department"],

            data["designation"],

            data["salary"],

            data["phone"],

            data["email"]

        ))

        conn.commit()

        conn.close()


    @staticmethod
    def update_employee(emp_id, data):

        conn = EmployeeModel.get_connection()

        cursor = conn.cursor()

        cursor.execute("""

        UPDATE employees

        SET

        name=?,

        age=?,

        gender=?,

        department=?,

        designation=?,

        salary=?,

        phone=?,

        email=?

        WHERE id=?

        """,

        (

            data["name"],

            data["age"],

            data["gender"],

            data["department"],

            data["designation"],

            data["salary"],

            data["phone"],

            data["email"],

            emp_id

        ))

        conn.commit()

        conn.close()


    @staticmethod
    def delete_employee(emp_id):

        conn = EmployeeModel.get_connection()

        cursor = conn.cursor()

        cursor.execute(

            "DELETE FROM employees WHERE id=?",

            (emp_id,)

        )

        conn.commit()

        conn.close()


    @staticmethod
    def search(keyword):

        conn = EmployeeModel.get_connection()

        cursor = conn.cursor()

        cursor.execute("""

        SELECT *

        FROM employees

        WHERE

        name LIKE ?

        OR department LIKE ?

        OR designation LIKE ?

        OR email LIKE ?

        ORDER BY id DESC

        """,

        (

            "%" + keyword + "%",

            "%" + keyword + "%",

            "%" + keyword + "%",

            "%" + keyword + "%"

        ))

        employees = cursor.fetchall()

        conn.close()

        return employees


    @staticmethod
    def email_exists(email):

        conn = EmployeeModel.get_connection()

        cursor = conn.cursor()

        cursor.execute(

            "SELECT id FROM employees WHERE email=?",

            (email,)

        )

        employee = cursor.fetchone()

        conn.close()

        return employee is not None


    # ============================================
# Attendance Methods
# ============================================

    @staticmethod
    def get_all_employees():

        conn = EmployeeModel.get_connection()

        cursor = conn.cursor()

        cursor.execute("""

            SELECT id, name

            FROM employees

            ORDER BY name

        """)

        employees = cursor.fetchall()

        conn.close()

        return employees


    @staticmethod
    def mark_attendance(employee_id, attendance_date, status):

        conn = EmployeeModel.get_connection()

        cursor = conn.cursor()

        cursor.execute("""

            INSERT INTO attendance

            (employee_id, attendance_date, status)

            VALUES (?, ?, ?)

        """, (

            employee_id,

            attendance_date,

            status

        ))

        conn.commit()

        conn.close()


    @staticmethod
    def attendance_exists(employee_id, attendance_date):

        conn = EmployeeModel.get_connection()

        cursor = conn.cursor()

        cursor.execute("""

            SELECT attendance_id

            FROM attendance

            WHERE employee_id = ?

            AND attendance_date = ?

        """, (

            employee_id,

            attendance_date

        ))

        result = cursor.fetchone()

        conn.close()

        return result is not None


    @staticmethod
    def get_attendance():

        conn = EmployeeModel.get_connection()

        cursor = conn.cursor()

        cursor.execute("""

            SELECT

                attendance.attendance_id,

                attendance.employee_id,

                employees.name,

                attendance.attendance_date,

                attendance.status

            FROM attendance

            JOIN employees

            ON attendance.employee_id = employees.id

            ORDER BY attendance.attendance_date DESC

        """)

        records = cursor.fetchall()

        conn.close()

        return records


    @staticmethod
    def delete_attendance(attendance_id):

        conn = EmployeeModel.get_connection()

        cursor = conn.cursor()

        cursor.execute("""

            DELETE FROM attendance

            WHERE attendance_id = ?

        """, (

            attendance_id,

        ))

        conn.commit()

        conn.close()


    @staticmethod
    def total_present():

        conn = EmployeeModel.get_connection()

        cursor = conn.cursor()

        cursor.execute("""

            SELECT COUNT(*)

            FROM attendance

            WHERE status='Present'

        """)

        count = cursor.fetchone()[0]

        conn.close()

        return count


    @staticmethod
    def total_absent():

        conn = EmployeeModel.get_connection()

        cursor = conn.cursor()

        cursor.execute("""

            SELECT COUNT(*)

            FROM attendance

            WHERE status='Absent'

        """)

        count = cursor.fetchone()[0]

        conn.close()

        return count


    @staticmethod
    def total_late():

        conn = EmployeeModel.get_connection()

        cursor = conn.cursor()

        cursor.execute("""

            SELECT COUNT(*)

            FROM attendance

            WHERE status='Late'

        """)

        count = cursor.fetchone()[0]

        conn.close()

        return count
        # ==========================
    # ============================================
# Payroll Methods
# ============================================

    @staticmethod
    def add_payroll(data):

        net_salary = (
            data["basic_salary"]
            + data["bonus"]
            - data["deduction"]
        )

        conn = EmployeeModel.get_connection()

        cursor = conn.cursor()

        cursor.execute("""

            INSERT INTO payroll(

                employee_id,

                basic_salary,

                bonus,

                deduction,

                net_salary,

                payroll_date

            )

            VALUES(?,?,?,?,?,?)

        """, (

            data["employee_id"],

            data["basic_salary"],

            data["bonus"],

            data["deduction"],

            net_salary,

            data["payroll_date"]

        ))

        conn.commit()

        conn.close()


    @staticmethod
    def get_payroll():

        conn = EmployeeModel.get_connection()

        cursor = conn.cursor()

        cursor.execute("""

            SELECT

                payroll.payroll_id,

                payroll.employee_id,

                employees.name,

                payroll.basic_salary,

                payroll.bonus,

                payroll.deduction,

                payroll.net_salary,

                payroll.payroll_date

            FROM payroll

            JOIN employees

            ON payroll.employee_id = employees.id

            ORDER BY payroll.payroll_id DESC

        """)

        rows = cursor.fetchall()

        conn.close()

        return rows


    @staticmethod
    def delete_payroll(payroll_id):

        conn = EmployeeModel.get_connection()

        cursor = conn.cursor()

        cursor.execute("""

            DELETE FROM payroll

            WHERE payroll_id = ?

        """, (

            payroll_id,

        ))

        conn.commit()

        conn.close()


    @staticmethod
    def payroll_count():

        conn = EmployeeModel.get_connection()

        cursor = conn.cursor()

        cursor.execute("""

            SELECT COUNT(*)

            FROM payroll

        """)

        count = cursor.fetchone()[0]

        conn.close()

        return count


    @staticmethod
    def total_payroll_amount():

        conn = EmployeeModel.get_connection()

        cursor = conn.cursor()

        cursor.execute("""

            SELECT IFNULL(

                SUM(net_salary),

                0

            )

            FROM payroll

        """)

        total = cursor.fetchone()[0]

        conn.close()

        return total
        # ==========================
    # Leave Management
    # ==========================

    @staticmethod
    def apply_leave(employee_id,
                    leave_type,
                    start_date,
                    end_date,
                    reason):

        conn = EmployeeModel.get_connection()

        cursor = conn.cursor()

        cursor.execute("""

        INSERT INTO leaves(

            employee_id,

            leave_type,

            start_date,

            end_date,

            reason

        )

        VALUES(?,?,?,?,?)

        """,

        (

            employee_id,

            leave_type,

            start_date,

            end_date,

            reason

        ))

        conn.commit()

        conn.close()


    @staticmethod
    def get_leaves():

        conn = EmployeeModel.get_connection()

        cursor = conn.cursor()

        cursor.execute("""

        SELECT

            leaves.leave_id,

            employees.name,

            employees.department,

            leaves.leave_type,

            leaves.start_date,

            leaves.end_date,

            leaves.reason,

            leaves.status

        FROM leaves

        INNER JOIN employees

        ON leaves.employee_id = employees.id

        ORDER BY leaves.leave_id DESC

        """)

        data = cursor.fetchall()

        conn.close()

        return data


    @staticmethod
    def approve_leave(leave_id):

        conn = EmployeeModel.get_connection()

        cursor = conn.cursor()

        cursor.execute("""

        UPDATE leaves

        SET status='Approved'

        WHERE leave_id=?

        """,

        (leave_id,))

        conn.commit()

        conn.close()


    @staticmethod
    def reject_leave(leave_id):

        conn = EmployeeModel.get_connection()

        cursor = conn.cursor()

        cursor.execute("""

        UPDATE leaves

        SET status='Rejected'

        WHERE leave_id=?

        """,

        (leave_id,))

        conn.commit()

        conn.close()


    @staticmethod
    def leave_summary():

        conn = EmployeeModel.get_connection()

        cursor = conn.cursor()

        cursor.execute("""

        SELECT COUNT(*)

        FROM leaves

        WHERE status='Pending'

        """)

        pending = cursor.fetchone()[0]

        cursor.execute("""

        SELECT COUNT(*)

        FROM leaves

        WHERE status='Approved'

        """)

        approved = cursor.fetchone()[0]

        cursor.execute("""

        SELECT COUNT(*)

        FROM leaves

        WHERE status='Rejected'

        """)

        rejected = cursor.fetchone()[0]

        conn.close()

        return pending, approved, rejected
# ============================================
# Reports
# ============================================

    @staticmethod
    def attendance_count():

        conn = EmployeeModel.get_connection()

        cursor = conn.cursor()

        cursor.execute("""

            SELECT COUNT(*)

            FROM attendance

        """)

        total = cursor.fetchone()[0]

        conn.close()

        return total


    @staticmethod
    def payroll_total():

        conn = EmployeeModel.get_connection()

        cursor = conn.cursor()

        cursor.execute("""

            SELECT IFNULL(

                SUM(net_salary),

                0

            )

            FROM payroll

        """)

        total = cursor.fetchone()[0]

        conn.close()

        return total


    @staticmethod
    def payroll_records():

        conn = EmployeeModel.get_connection()

        cursor = conn.cursor()

        cursor.execute("""

            SELECT COUNT(*)

            FROM payroll

        """)

        total = cursor.fetchone()[0]

        conn.close()

        return total


    @staticmethod
    def report_summary():

        conn = EmployeeModel.get_connection()

        cursor = conn.cursor()

        cursor.execute("""

            SELECT COUNT(*)

            FROM attendance

            WHERE status='Present'

        """)

        present = cursor.fetchone()[0]


        cursor.execute("""

            SELECT COUNT(*)

            FROM attendance

            WHERE status='Absent'

        """)

        absent = cursor.fetchone()[0]


        cursor.execute("""

            SELECT COUNT(*)

            FROM attendance

            WHERE status='Late'

        """)

        late = cursor.fetchone()[0]

        conn.close()

        return present, absent, late
# ============================================
# Settings
# ============================================

    @staticmethod
    def get_admin():

        conn = EmployeeModel.get_connection()

        cursor = conn.cursor()

        cursor.execute("""

            SELECT *

            FROM admin

            LIMIT 1

        """)

        admin = cursor.fetchone()

        conn.close()

        return admin


    @staticmethod
    def update_password(current_password, new_password):

        conn = EmployeeModel.get_connection()

        cursor = conn.cursor()

        cursor.execute("""

            SELECT *

            FROM admin

            WHERE password = ?

        """, (

            current_password,

        ))

        admin = cursor.fetchone()

        if admin:

            cursor.execute("""

                UPDATE admin

                SET password = ?

                WHERE id = ?

            """, (

                new_password,

                admin["id"]

            ))

            conn.commit()

            conn.close()

            return True

        conn.close()

        return False