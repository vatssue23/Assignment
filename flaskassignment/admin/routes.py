from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request
from flaskassignment import bcrypt, db, app
from flaskassignment.admin.forms import AdminLogin, AdminUpdateEmployee, SearchForm
from flask_login import login_user, logout_user, login_required
from flaskassignment.models import Employee
from flaskassignment.employee.forms import RegisterEmployee
from flask_login import current_user
import requests
import jwt


admin = Blueprint("admin", __name__)


@admin.route("/")
def home():
    if current_user.is_authenticated:
        if current_user.is_admin:
            data = Employee.query.all()
            return render_template("admin_home.html", title="HOME", data=data)
        else:
            return redirect(url_for("employee.home"))
    else:
        return redirect(url_for("admin.admin_login"))


@admin.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    form = AdminLogin()
    if form.validate_on_submit():
        admins = Employee.query.filter_by(email=form.email.data).first()
        if admins and bcrypt.check_password_hash(admins.password, form.password.data) and admins.is_admin:
            login_user(admins, remember=form.remember.data)
            flash('User Successfully Logged In !', 'success')
            app.logger.info('%s Logged in Successful', admins.email)
            return redirect(url_for('admin.home'))
        else:
            app.logger.info('%s Logged in Unuccessful', admins.email)
            flash('Login Failed. Either detail is wrong', 'danger')
    return render_template("admin_login.html", title="Admin Login", form=form)


@admin.route('/add_new_employee', methods=['GET', 'POST'])
@login_required
def add_new_employee():
    if current_user.is_admin:
        if current_user.is_authenticated:
            form = RegisterEmployee()
            if form.validate_on_submit():
                hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
                employee = Employee(first_name=form.first_name.data, last_name=form.last_name.data,
                                    email=form.email.data, password=hashed_pass, phone_num=form.phone_num.data,
                                    dob=form.dob.data, address=form.address.data)
                db.session.add(employee)
                db.session.commit()
                app.logger.info('%s employee created Successfully created by Admin %s', employee.email, current_user.email)
                flash('Account Created for {}!'.format(form.first_name.data), 'success')
                return redirect(url_for('admin.home'))
            return render_template("register_new_employee.html",
                                   title="Register New Employee", form=form)
        else:
            return redirect(url_for("main.home"))
    else:
        return redirect(url_for("employee.home"))


@admin.route("/update_employee/<int:employee_id>", methods=['GET', 'POST'])
@login_required
def update_employee(employee_id):
    if current_user.is_admin:
        if current_user.is_authenticated:
            employee = Employee.query.get_or_404(employee_id)
            if not employee.is_admin:
                form = AdminUpdateEmployee()
                if form.validate_on_submit():
                    employee.first_name = form.first_name.data
                    employee.last_name = form.last_name.data
                    employee.dob = form.dob.data
                    employee.address = form.address.data
                    db.session.commit()
                    app.logger.info('%s employee Successfully updated by Admin %s', employee.email, current_user.email)
                    flash('User Successfully Updated!', 'success')
                    return redirect(url_for('admin.home'))
                elif request.method == 'GET':
                    form.first_name.data = employee.first_name
                    form.last_name.data = employee.last_name
                    form.dob.data = employee.dob
                    form.address.data = employee.address
                return render_template("update_employee.html", title="Update Employee", form=form, employee_id=employee_id)
            else:
                return redirect(url_for("admin.home"))
        else:
            return redirect(url_for("main.home"))
    else:
        return redirect(url_for("employee.home"))


@admin.route("/delete_employee/<int:employee_id>", methods=['POST'])
@login_required
def delete_employee(employee_id):
    if current_user.is_admin:
        if current_user.is_authenticated:
            employee = Employee.query.get_or_404(employee_id)
            app.logger.info('%s employee Deleted Successfully by Admin %s', employee.email, current_user.email)
            db.session.delete(employee)
            db.session.commit()
            return redirect(url_for('admin.home'))
        else:
            return redirect(url_for("main.home"))
    else:
        return redirect(url_for("employee.home"))


@admin.route('/logout')
def logout():
    if current_user.is_admin:
        app.logger.info('%s Admin successfully logged out', current_user.email)
        logout_user()
        return redirect(url_for('main.home'))
    else:
        return redirect(url_for("employee.home"))


@admin.route("/search", methods=['GET', 'POST'])
@login_required
def search_employee():
    if current_user.is_admin:
        form = SearchForm()
        if current_user.is_authenticated and current_user.is_admin:
            data = {
                'email': current_user.email,
                'data': form.search_value.data
            }
            employee = {}
            flag = False
            if request.method == 'POST':
                app.logger.info('%s Admin searched with variable %s', current_user.email, form.search_value.data)
                token = {"token": jwt.encode(data, app.config.get('SECRET_KEY')).decode('UTF-8')}
                employee = requests.get("http://127.0.0.1:5000/api/search_result", params=token).json()
                flag = True
            return render_template("search.html", title="Search Employee", form=form, data=employee, flag=flag)
        else:
            return redirect(url_for("admin.home"))
    else:
        return redirect(url_for("employee.home"))
