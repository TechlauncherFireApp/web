from flask import Blueprint
from flask_restful import fields, Resource, marshal_with, Api, reqparse

from domain import session_scope
from repository.asset_type_role_repository import get_seats, delete_seat, add_seat

get_fields = {
    'assetTypeRoleId': fields.Integer,
    'seatNumber': fields.Integer,
    'roleId': fields.Integer,
    'roleName': fields.String,
}

post_fields = {
    'userRoleId': fields.Integer
}

patch_fields = {
    'success': fields.Boolean
}

parser = reqparse.RequestParser()
parser.add_argument('assetTypeId', action='store', type=str)
parser.add_argument('assetTypeRoleId', action='store', type=str)
parser.add_argument('roleId', action='store', type=str)


class AssetTypeRole(Resource):
    @marshal_with(get_fields)
    def get(self):
        args = parser.parse_args()
        if args['assetTypeId'] is None:
            return
        with session_scope() as session:
            return get_seats(session, args['assetTypeId'])

    def delete(self):
        args = parser.parse_args()
        if args['assetTypeRoleId'] is None:
            return
        with session_scope() as session:
            return delete_seat(session, args['assetTypeRoleId'])

    def post(self):
        args = parser.parse_args()
        if args['assetTypeId'] is None or args['roleId'] is None:
            return
        with session_scope() as session:
            return add_seat(session, args['assetTypeId'], args['roleId'])


asset_type_role_bp = Blueprint('asset-type-role', __name__)
api = Api(asset_type_role_bp)
api.add_resource(AssetTypeRole, '/asset-type-role')
