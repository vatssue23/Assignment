from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request
from flaskassignment import bcrypt, db, app
from flaskassignment.models import Employee
from flaskassignment.employee.forms import RegisterEmployee, Login, UpdateEmployee
from flask_login import login_user, logout_user, current_user, login_required


employee = Blueprint('employee', __name__)


@employee.route("/")
def home():
    return redirect(url_for("employee.employee_details"))


@employee.route("/register_employee", methods=['GET', 'POST'])
def register_employee():
    if current_user.is_authenticated:
        return redirect(url_for('employee.employee_details'))
    form = RegisterEmployee()
    if form.validate_on_submit():
        hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        employe = Employee(first_name=form.first_name.data, last_name=form.last_name.data,
                                email=form.email.data, password=hashed_pass, phone_num=form.phone_num.data,
                                dob=form.dob.data, address=form.address.data)
        db.session.add(employe)
        db.session.commit()
        app.logger.info('%s Successfully Registered', employe.email)
        flash('Account Created for {}!'.format(form.first_name.data), 'success')
        return redirect(url_for('employee.login'))
    return render_template("register_employee.html",
                               title="Register Employee", form=form)


@employee.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = Login()
    if form.validate_on_submit():
        employe = Employee.query.filter_by(email=form.email.data).first()
        if employe and bcrypt.check_password_hash(employe.password, form.password.data) and not employe.is_admin:
            login_user(employe, remember=form.remember.data)
            app.logger.info('%s Logged in Successfully', employe.email)
            flash('User Successfully Logged In !', 'success')
            return redirect(url_for('employee.employee_details'))
        else:
            app.logger.info('%s Logged in Unsuccessful', employe.email)
            flash('Login Failed. Either detail is wrong', 'danger')

    return render_template("login.html",
                               title="Login Employee", form=form)


@employee.route('/logout')
def logout():
    if not current_user.is_admin:
        app.logger.info('%s Successfully Logged Out', current_user.email)
        logout_user()
        return redirect(url_for('main.home'))
    else:
        return redirect(url_for("admin.home"))


@employee.route('/employee_details', methods=['GET', 'POST'])
@login_required
def employee_details():
    if not current_user.is_admin:
        form = UpdateEmployee()
        if form.validate_on_submit():
            current_user.first_name = form.first_name.data
            current_user.last_name = form.last_name.data
            current_user.phone_num = form.phone_num.data
            current_user.dob = form.dob.data
            current_user.address = form.address.data
            db.session.commit()
            app.logger.info('%s Updated its own details', current_user.email)
            flash('User Successfully Updated!', 'success')
            return redirect(url_for('employee.employee_details'))
        elif request.method == 'GET':
            form.first_name.data = current_user.first_name
            form.last_name.data = current_user.last_name
            form.phone_num.data = current_user.phone_num
            form.dob.data = current_user.dob
            form.address.data = current_user.address
        return render_template("employee_details.html", title="Employee Details", form=form)
    else:
        return redirect(url_for("admin.home"))
