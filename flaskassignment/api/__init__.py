from flask import Blueprint

api = Blueprint("api", __name__)

from flask_restful import Resource, Api, reqparse
from flaskassignment.models import Employee
from flask import jsonify
import jwt
from flaskassignment import app

apis = Api(api)


parser = reqparse.RequestParser()
parser.add_argument('token', help='This field cannot be blank', required=True)


class Searcher(Resource):
    def get(self):
        dat = parser.parse_args()
        data = jwt.decode(dat['token'], app.config.get('SECRET_KEY'))
        person = Employee.query.filter_by(email=data['email']).first()
        if person.is_admin:
            ei = []
            ei.append(Employee.query.filter_by(first_name=data['data']).all())
            ei.append(Employee.query.filter_by(last_name=data['data']).all())
            ei.append(Employee.query.filter_by(address=data['data']).all())
            final_person = {}
            i = 1
            for list_in in ei:
                for dat in list_in:
                    if not dat.is_admin:
                        temp = {
                            "id": dat.id,
                            "first_name": dat.first_name,
                            "last_name": dat.last_name,
                            "email": dat.email
                        }
                        final_person[i] = temp
                        i = i + 1
            return jsonify(final_person)


apis.add_resource(Searcher, "/search_result")

