from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource, marshal_with, reqparse, fields

from domain import session_scope
from repository.profile import modify_profile, get_profile
from repository.user_role_repository import get_user_roles_by_id

result_fields = {
    "result": fields.Boolean
}

user_info_fields = {
    'id': fields.Integer,
    'first name': fields.String,
    'last name': fields.String,
    'email': fields.String,
    'mobile_number': fields.String,
    'roles': fields.List(fields.String),
    'gender': fields.String,
    'dietary': fields.String,
    'allergy': fields.String
}

profile = reqparse.RequestParser()
profile.add_argument('id', type=str)
profile.add_argument('phone', type=str)
profile.add_argument('gender', type=str)
profile.add_argument('dietary', type=str)
profile.add_argument('allergy', type=str)

getId = reqparse.RequestParser()
getId.add_argument("id", type=str)


class EditProfile(Resource):
    @marshal_with(result_fields)
    def post(self):
        request.get_json(force=True)
        args = profile.parse_args()
        with session_scope() as session:
            return {'result': modify_profile(session, args['id'], args['phone'], args['gender'], args['dietary'],
                                             args['allergy'])}
            # result = modify_profile(session, args['id'], args['phone'], args['gender'], args['diet'], args['allergy'])
        # return jsonify({"result": result.nameresult})


class getProfile(Resource):
    @marshal_with(user_info_fields)
    def post(self):
        request.get_json(force=True)
        args = getId.parse_args()
        with session_scope() as session:
            user = get_profile(session, args['id'])
            user_dict = {
                'id': user.id,
                'first name': user.first_name,
                'last name': user.last_name,
                'email': user.email,
                'mobile_number': user.mobile_number,
                'roles': get_user_roles_by_id(session, user.id),
                'gender': user.gender,
                'dietary': user.diet,
                'allergy': user.allergy
            }
            return user_dict


profile_bp = Blueprint('profile', __name__)
api = Api(profile_bp)
api.add_resource(EditProfile, '/profile/editProfile')
api.add_resource(getProfile, '/profile/getProfile')
