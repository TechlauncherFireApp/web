from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource, marshal_with, reqparse, fields

from domain import session_scope
from repository.profile import modify_profile
result_fields = {
    "result": fields.Boolean
}

profile = reqparse.RequestParser()
profile.add_argument('id', type=str)
profile.add_argument('phone', type=str)
profile.add_argument('gender', type=str)
profile.add_argument('dietary', type=str)
profile.add_argument('allergy', type=str)


class EditProfile(Resource):
    @marshal_with(result_fields)
    def post(self):
        request.get_json(force=True)
        args = profile.parse_args()
        with session_scope() as session:
            return {'result': modify_profile(session, args['id'], args['phone'], args['gender'], args['dietary'], args['allergy'])}
            # result = modify_profile(session, args['id'], args['phone'], args['gender'], args['diet'], args['allergy'])
        # return jsonify({"result": result.nameresult})


profile_bp = Blueprint('profile', __name__)
api = Api(profile_bp)
api.add_resource(EditProfile, '/profile/editProfile')
