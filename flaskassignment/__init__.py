from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = '58f6ca56fb543a94821432e3964b4481'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'employee.login'
login_manager.login_message = 'info'


from flaskassignment.employee.routes import employee
from flaskassignment.admin.routes import admin
from flaskassignment.main.routes import main
from flaskassignment.api import api

app.register_blueprint(employee, url_prefix="/employee")
app.register_blueprint(admin, url_prefix="/admin")
app.register_blueprint(main)
app.register_blueprint(api, url_prefix="/api")


from logging.config import dictConfig

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})


