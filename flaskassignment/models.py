from flaskassignment import db
from flaskassignment import login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_employee(employee_id):
    return Employee.query.get(int(employee_id))


class Employee(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    phone_num = db.Column(db.Integer, unique=True, nullable=False)
    dob = db.Column(db.DateTime, nullable=False)
    address = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, unique=False, default=False)

    def __repr__(self):
        return "Employee {}, {}, {}, {}".format(self.id, self.first_name, self.email, self.is_admin)
