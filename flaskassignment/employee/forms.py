from flask_wtf import FlaskForm
from flask_login import current_user
from flaskassignment.models import Employee
from wtforms import StringField, SubmitField, DateField, BooleanField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Email, Length, ValidationError
from datetime import date


min_age = 18


class RegisterEmployee(FlaskForm):
    first_name = StringField('First Name*', validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last Name', validators=[Length(min=0, max=20)])
    email = StringField('Email*', validators=[DataRequired(), Email()])
    password = PasswordField('Password*', validators=[DataRequired(), Length(min=6, max=20)])
    confirm_password = PasswordField('Confirm Password*', validators=[DataRequired(), EqualTo('password')])
    phone_num = StringField('Phone Number*', validators=[DataRequired(), Length(min=10, max=10)])
    dob = DateField('Date of Birth (YYYY-MM-DD)*', validators=[DataRequired()], format='%Y-%m-%d')
    address = StringField('Address*', validators=[DataRequired()])
    submit = SubmitField('Register Employee')

    def validate_dob(form, field):
        global min_age
        today = date.today()
        age = today.year - field.data.year - ((today.month, today.day) < (field.data.month, field.data.day))
        if age < min_age:
            raise ValidationError('AGE SHOULD BE ABOVE 18')

    def validate_email(form, field):
        employee = Employee.query.filter_by(email=field.data).first()
        if employee:
            raise ValidationError('User Already exists with this email')

    def validate_phone_num(form, field):
        employee = Employee.query.filter_by(phone_num=field.data).first()
        if employee:
            raise ValidationError('User Already exists with this Phone Number')


class Login(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')


class UpdateEmployee(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last Name', validators=[Length(min=0, max=20)])
    phone_num = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=10)])
    dob = DateField('Date of Birth (YYYY-MM-DD)', validators=[DataRequired()], format='%Y-%m-%d')
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Update Employee')

    def validate_dob(form, field):
        global min_age
        today = date.today()
        age = today.year - field.data.year - ((today.month, today.day) < (field.data.month, field.data.day))
        if age < min_age:
            raise ValidationError('AGE SHOULD BE ABOVE 18')

    def validate_phone_num(form, field):
        if int(form.phone_num.data) != current_user.phone_num:
            employee = Employee.query.filter_by(phone_num=field.data).first()
            if employee:
                raise ValidationError('User Already exists with this Phone Number')
