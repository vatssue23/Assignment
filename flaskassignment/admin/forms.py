from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, BooleanField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Email, Length, ValidationError
from datetime import date

min_age = 18


class AdminLogin(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')


class AdminUpdateEmployee(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last Name', validators=[Length(min=0, max=20)])
    dob = DateField('Date of Birth (YYYY-MM-DD)', validators=[DataRequired()], format='%Y-%m-%d')
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Update Employee')

    def validate_dob(form, field):
        global min_age
        today = date.today()
        age = today.year - field.data.year - ((today.month, today.day) < (field.data.month, field.data.day))
        if age < min_age:
            raise ValidationError('AGE SHOULD BE ABOVE 18')


class SearchForm(FlaskForm):
    search_value = StringField('Search Value', validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField('Search Employee')
