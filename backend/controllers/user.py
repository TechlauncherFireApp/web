from flask import Blueprint
from flask_restful import fields, Resource, marshal_with, Api, reqparse

from domain import session_scope
from repository.user_repository import get_user_by_id
from repository.user_role_repository import get_user_roles_by_id, get_user_roles


user_fields = {
    'name': fields.String,
    'email': fields.String,
    'mobile_number': fields.String,
    'roles': fields.List(fields.String)
}


class GetUserRequest(Resource):
    @marshal_with(user_fields)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, required=True)
        args = parser.parse_args()
        with session_scope() as session:
            user = get_user_by_id(session, args['id'])
            user_dict = {
                'name': user.first_name + ' ' + user.last_name,
                'email': user.email,
                'mobile_number': user.mobile_number,
                'roles': get_user_roles_by_id(session, args['id'])
            }
            return user_dict


user_bp = Blueprint('user', __name__)
api = Api(user_bp, "/user")
api.add_resource(GetUserRequest, "/getUserById")
