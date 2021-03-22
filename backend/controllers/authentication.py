from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource, marshal_with, reqparse

from domain import session_scope
from services.authentication import AuthenticationService

registration_parser = reqparse.RequestParser()
registration_parser.add_argument('email', type=str)
registration_parser.add_argument('password', type=str)
registration_parser.add_argument('given_name', type=str)
registration_parser.add_argument('last_name', type=str)
registration_parser.add_argument('phone', type=str)

login_parser = reqparse.RequestParser()
login_parser.add_argument('email', type=str)
login_parser.add_argument('password', type=str)


class Register(Resource):

    def post(self):
        request.get_json(force=True)
        args = registration_parser.parse_args()
        auth = AuthenticationService()
        with session_scope() as session:
            result = auth.register(session, args['email'], args['password'], args['given_name'z], args['last_name'],
                                   args['phone'])
        return jsonify({"result": result.name})


class Login(Resource):
    def post(self):
        request.get_json(force=True)
        args = login_parser.parse_args()
        auth = AuthenticationService()
        with session_scope() as session:
            result, token, user = auth.login(session, args['email'], args['password'])
            if token is None:
                return jsonify({"result": result.name})
            return jsonify({"result": result.name, "access_token": token, "role": user.role.name, 'id': user.id})


authentication_bp = Blueprint('authentication', __name__)
api = Api(authentication_bp)
api.add_resource(Register, '/authentication/register')
api.add_resource(Login, '/authentication/login')
