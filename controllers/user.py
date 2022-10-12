from flask import Blueprint
from flask_restful import fields, Resource, marshal_with, Api, reqparse

from domain import session_scope
from repository.user_repository import get_user_by_email, get_volunteer_id_name
from repository.user_role_repository import get_user_roles_by_id

user_info_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'email': fields.String,
    'mobile_number': fields.String,
    'roles': fields.List(fields.String)
}


class GetUserInfoRequest(Resource):
    @marshal_with(user_info_fields)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True)
        args = parser.parse_args()
        with session_scope() as session:
            user = get_user_by_email(session, args['email'])
            user_dict = {
                'id': user.id,
                'name': user.first_name + ' ' + user.last_name,
                'email': user.email,
                'mobile_number': user.mobile_number,
                'roles': get_user_roles_by_id(session, user.id)
            }
            return user_dict


class GetAvailabilitiesRequest(Resource):
    @staticmethod
    def get():
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True)
        args = parser.parse_args()
        with session_scope() as session:
            user = get_user_by_email(session, args['email'])
            return user.availabilities


class GetAllVolunteer(Resource):
    def get(self):
        with session_scope() as session:
            v_dict = get_volunteer_id_name(session)
        return v_dict


user_bp = Blueprint('user', __name__)
api = Api(user_bp, "/user")
api.add_resource(GetUserInfoRequest, "/getUserInfoByEmail")
api.add_resource(GetAvailabilitiesRequest, "/getAvailabilityByEmail")
api.add_resource(GetAllVolunteer, "/getAllVolunteer")
