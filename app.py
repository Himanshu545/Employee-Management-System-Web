from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session
)

import sqlite3
from functools import wraps

from config import Config
from database import create_database
from models import EmployeeModel


app = Flask(__name__)

app.config.from_object(Config)

create_database()


# ===========================================
# Login Required Decorator
# ===========================================

def login_required(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        if "admin" not in session:

            flash("Please login first.", "warning")

            return redirect(url_for("login"))

        return func(*args, **kwargs)

    return wrapper


# ===========================================
# Login
# ===========================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if "admin" in session:

        return redirect(url_for("dashboard"))

    if request.method == "POST":

        username = request.form["username"]

        password = request.form["password"]

        admin = EmployeeModel.admin_login(
            username,
            password
        )

        if admin:

            session["admin"] = username

            flash(
                "Login Successful.",
                "success"
            )

            return redirect(
                url_for("dashboard")
            )

        flash(
            "Invalid Username or Password.",
            "danger"
        )

    return render_template(
        "login.html"
    )


# ===========================================
# Logout
# ===========================================

@app.route("/logout")
def logout():

    session.clear()

    flash(
        "Logged Out Successfully.",
        "success"
    )

    return redirect(
        url_for("login")
    )


# ===========================================
# Dashboard
# ===========================================

@app.route("/")
@login_required
def dashboard():

    total = EmployeeModel.total_employees()

    departments = EmployeeModel.total_departments()

    salary = EmployeeModel.total_salary()

    employees = EmployeeModel.get_recent()

    return render_template(
        "dashboard.html",
        total=total,
        departments=departments,
        salary=salary,
        employees=employees
    )


# ===========================================
# Employees
# ===========================================

@app.route("/employees")
@login_required
def employees():

    employees = EmployeeModel.get_all()

    return render_template(
        "employees.html",
        employees=employees
    )


# ===========================================
# Search Employee
# ===========================================

@app.route("/search")
@login_required
def search_employee():

    keyword = request.args.get(
        "keyword",
        ""
    ).strip()

    if keyword == "":

        return redirect(
            url_for("employees")
        )

    employees = EmployeeModel.search(
        keyword
    )

    return render_template(
        "employees.html",
        employees=employees
    )


# ===========================================
# Add Employee
# ===========================================

@app.route("/add", methods=["GET", "POST"])
@login_required
def add_employee():

    if request.method == "POST":

        data = {

            "name": request.form["name"],

            "age": int(request.form["age"]),

            "gender": request.form["gender"],

            "department": request.form["department"],

            "designation": request.form["designation"],

            "salary": float(request.form["salary"]),

            "phone": request.form["phone"],

            "email": request.form["email"]

        }

        try:

            if EmployeeModel.email_exists(data["email"]):

                flash(
                    "Email already exists.",
                    "danger"
                )

                return redirect(
                    url_for("add_employee")
                )

            EmployeeModel.add_employee(data)

            flash(
                "Employee Added Successfully.",
                "success"
            )

            return redirect(
                url_for("employees")
            )

        except sqlite3.IntegrityError:

            flash(
                "Email already exists.",
                "danger"
            )

        except Exception as e:

            flash(
                str(e),
                "danger"
            )

    return render_template(
        "add_employee.html"
    )


# ===========================================
# Edit Employee
# ===========================================

@app.route("/edit/<int:emp_id>", methods=["GET", "POST"])
@login_required
def edit_employee(emp_id):

    employee = EmployeeModel.get_employee(emp_id)

    if employee is None:

        flash(
            "Employee not found.",
            "danger"
        )

        return redirect(
            url_for("employees")
        )

    if request.method == "POST":

        data = {

            "name": request.form["name"],

            "age": int(request.form["age"]),

            "gender": request.form["gender"],

            "department": request.form["department"],

            "designation": request.form["designation"],

            "salary": float(request.form["salary"]),

            "phone": request.form["phone"],

            "email": request.form["email"]

        }

        EmployeeModel.update_employee(
            emp_id,
            data
        )

        flash(
            "Employee Updated Successfully.",
            "success"
        )

        return redirect(
            url_for("employees")
        )

    return render_template(
        "edit_employee.html",
        employee=employee
    )


# ===========================================
# Delete Employee
# ===========================================

@app.route("/delete/<int:emp_id>")
@login_required
def delete_employee(emp_id):

    EmployeeModel.delete_employee(
        emp_id
    )

    flash(
        "Employee Deleted Successfully.",
        "warning"
    )

    return redirect(
        url_for("employees")
    )


# ==========================================
# Reports
# ==========================================

@app.route("/reports")
def reports():

    total_employees = EmployeeModel.total_employees()

    departments = EmployeeModel.total_departments()

    total_salary = EmployeeModel.total_salary()

    total_payroll = EmployeeModel.payroll_total()

    attendance_count = EmployeeModel.attendance_count()

    payroll_count = EmployeeModel.payroll_records()

    present, absent, late = EmployeeModel.report_summary()

    return render_template(

        "reports.html",

        total_employees=total_employees,

        departments=departments,

        total_salary=total_salary,

        total_payroll=total_payroll,

        attendance_count=attendance_count,

        payroll_count=payroll_count,

        present=present,

        absent=absent,

        late=late

    )


# ==========================================
# Attendance
# ==========================================

@app.route("/attendance", methods=["GET", "POST"])
def attendance():

    if request.method == "POST":

        employee_id = request.form["employee_id"]

        attendance_date = request.form["attendance_date"]

        status = request.form["status"]

        if EmployeeModel.attendance_exists(

            employee_id,

            attendance_date

        ):

            flash(

                "Attendance already marked for this employee.",

                "warning"

            )

            return redirect(

                url_for("attendance")

            )

        EmployeeModel.mark_attendance(

            employee_id,

            attendance_date,

            status

        )

        flash(

            "Attendance Saved Successfully.",

            "success"

        )

        return redirect(

            url_for("attendance")

        )

    employees = EmployeeModel.get_all_employees()

    attendance = EmployeeModel.get_attendance()

    present = EmployeeModel.total_present()

    absent = EmployeeModel.total_absent()

    late = EmployeeModel.total_late()

    return render_template(

        "attendance.html",

        employees=employees,

        attendance=attendance,

        present=present,

        absent=absent,

        late=late

    )
# ==========================================
# Delete Attendance
# ==========================================

@app.route("/delete_attendance/<int:attendance_id>")
def delete_attendance(attendance_id):

    EmployeeModel.delete_attendance(

        attendance_id

    )

    flash(

        "Attendance Deleted Successfully.",

        "warning"

    )

    return redirect(

        url_for("attendance")

    )

# ==========================================
# Payroll
# ==========================================

@app.route("/payroll", methods=["GET", "POST"])
def payroll():

    if request.method == "POST":

        data = {

            "employee_id": int(request.form["employee_id"]),

            "basic_salary": float(request.form["basic_salary"]),

            "bonus": float(request.form["bonus"]),

            "deduction": float(request.form["deduction"]),

            "payroll_date": request.form["payroll_date"]

        }

        EmployeeModel.add_payroll(data)

        flash(

            "Payroll Added Successfully.",

            "success"

        )

        return redirect(

            url_for("payroll")

        )

    employees = EmployeeModel.get_all_employees()

    payroll = EmployeeModel.get_payroll()

    payroll_count = EmployeeModel.payroll_count()

    total_salary = EmployeeModel.total_payroll_amount()

    return render_template(

        "payroll.html",

        employees=employees,

        payroll=payroll,

        payroll_count=payroll_count,

        total_salary=total_salary

    )
# ==========================================
# Delete Payroll
# ==========================================

@app.route("/delete_payroll/<int:payroll_id>")
def delete_payroll(payroll_id):

    EmployeeModel.delete_payroll(payroll_id)

    flash(

        "Payroll Deleted Successfully.",

        "warning"

    )

    return redirect(

        url_for("payroll")

    )
# ===========================================
# Leave Management
# ===========================================

@app.route("/leave", methods=["GET", "POST"])
@login_required
def leave():

    if request.method == "POST":

        employee_id = request.form["employee_id"]

        leave_type = request.form["leave_type"]

        start_date = request.form["start_date"]

        end_date = request.form["end_date"]

        reason = request.form["reason"]

        try:

            EmployeeModel.apply_leave(

                employee_id,

                leave_type,

                start_date,

                end_date,

                reason

            )

            flash(

                "Leave Request Submitted Successfully.",

                "success"

            )

            return redirect(

                url_for("leave")

            )

        except Exception as e:

            flash(

                str(e),

                "danger"

            )

    employees = EmployeeModel.get_all()

    leaves = EmployeeModel.get_leaves()

    pending, approved, rejected = EmployeeModel.leave_summary()

    return render_template(

        "leave.html",

        employees=employees,

        leaves=leaves,

        pending=pending,

        approved=approved,

        rejected=rejected

    )


# ===========================================
# Approve Leave
# ===========================================

@app.route("/approve_leave/<int:leave_id>")
@login_required
def approve_leave(leave_id):

    EmployeeModel.approve_leave(leave_id)

    flash(

        "Leave Approved Successfully.",

        "success"

    )

    return redirect(

        url_for("leave")

    )


# ===========================================
# Reject Leave
# ===========================================

@app.route("/reject_leave/<int:leave_id>")
@login_required
def reject_leave(leave_id):

    EmployeeModel.reject_leave(leave_id)

    flash(

        "Leave Rejected Successfully.",

        "warning"

    )

    return redirect(

        url_for("leave")

    )

# ==========================================
# Settings
# ==========================================

@app.route("/settings", methods=["GET", "POST"])
def settings():

    if request.method == "POST":

        current_password = request.form["current_password"]

        new_password = request.form["new_password"]

        success = EmployeeModel.update_password(

            current_password,

            new_password

        )

        if success:

            flash(

                "Password Updated Successfully.",

                "success"

            )

        else:

            flash(

                "Current Password is Incorrect.",

                "danger"

            )

        return redirect(

            url_for("settings")

        )

    admin = EmployeeModel.get_admin()

    return render_template(

        "settings.html",

        admin=admin

    )


# ===========================================
# Profile
# ===========================================

@app.route("/profile")
@login_required
def profile():

    return render_template(
        "profile.html"
    )


# ===========================================
# Error Pages
# ===========================================

@app.errorhandler(404)
def page_not_found(error):

    return render_template(
        "404.html"
    ), 404


@app.errorhandler(500)
def server_error(error):

    return render_template(
        "500.html"
    ), 500


# ===========================================
# Run Server
# ===========================================

if __name__ == "__main__":

    app.run(
        debug=True
    )