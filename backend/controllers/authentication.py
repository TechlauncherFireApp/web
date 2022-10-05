from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource, reqparse

from domain import session_scope
from services.authentication import AuthenticationService

registration_parser = reqparse.RequestParser()
registration_parser.add_argument('email', type=str)
registration_parser.add_argument('password', type=str)
registration_parser.add_argument('given_name', type=str)
registration_parser.add_argument('last_name', type=str)
registration_parser.add_argument('phone', type=str)
registration_parser.add_argument('gender', type=str)
registration_parser.add_argument('diet', type=str)
registration_parser.add_argument('allergy', type=str)

login_parser = reqparse.RequestParser()
login_parser.add_argument('email', type=str)
login_parser.add_argument('password', type=str)

password_parser = reqparse.RequestParser()
password_parser.add_argument('email', type=str)

verify_password_parser = reqparse.RequestParser()
verify_password_parser.add_argument('email', type=str)
verify_password_parser.add_argument('code', type=str)

reset_password_parser = reqparse.RequestParser()
reset_password_parser.add_argument('email', type=str)
reset_password_parser.add_argument('new_password', type=str)
reset_password_parser.add_argument('repeat_password', type=str)


class Register(Resource):

    def post(self):
        request.get_json(force=True)
        args = registration_parser.parse_args()
        auth = AuthenticationService()
        with session_scope() as session:
            result = auth.register(session, args['email'], args['password'], args['given_name'], args['last_name'],
                                   args['phone'], args['gender'], args['diet'], args['allergy'])
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


class send_code(Resource):
    def post(self):
        request.get_json(force=True)
        args = password_parser.parse_args()
        auth = AuthenticationService()
        with session_scope() as session:
            result = auth.send_code(session, args['email'])
        return jsonify({"result": result.name})


class verify_code(Resource):
    def post(self):
        request.get_json(force=True)
        args = verify_password_parser.parse_args()
        auth = AuthenticationService()
        with session_scope() as session:
            result = auth.verify_code(session, args['email'], args['code'])
        return jsonify({"result": result.name})


class reset_password(Resource):
    def post(self):
        request.get_json(force=True)
        args = reset_password_parser.parse_args()
        auth = AuthenticationService()
        with session_scope() as session:
            result = auth.reset_password(session, args['email'], args['new_password'], args['repeat_password'])
        return jsonify({"result": result.name})





authentication_bp = Blueprint('authentication', __name__)
api = Api(authentication_bp)
api.add_resource(Register, '/authentication/register')
api.add_resource(Login, '/authentication/login')
api.add_resource(send_code, '/authentication/send_code')
api.add_resource(verify_code, '/authentication/verify')
api.add_resource(reset_password, '/authentication/reset')
