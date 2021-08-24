from flask import Blueprint
from flask_restful import fields, Resource, marshal_with, Api, reqparse

from domain import session_scope
from repository.reference_repository import get_roles, get_qualifications, add_qualification, add_role, \
    toggle_qualification, toggle_role, get_asset_type, add_asset_type, toggle_asset_type

get_role_fields = {
    'id': fields.Integer,
    'code': fields.String,
    'name': fields.String,
    'created': fields.DateTime(attribute='insert_date_time', dt_format='iso8601'),
    'updated': fields.DateTime(attribute='update_date_time', dt_format='rfc822'),
    'deleted': fields.String(attribute='deleted'),
}

post_role_fields = {
    'id': fields.String,
}

role_parser = reqparse.RequestParser()
role_parser.add_argument('id', action='store', type=str)
role_parser.add_argument('name', action='store', type=str)
role_parser.add_argument('code', action='store', type=str)


class RoleRequest(Resource):
    @marshal_with(get_role_fields)
    def get(self):
        with session_scope() as session:
            return get_roles(session)

    @marshal_with(post_role_fields)
    def post(self):
        args = role_parser.parse_args()
        if args['name'] is None or args['name'] == '' or args['code'] is None or args['code'] == '':
            return
        with session_scope() as session:
            role_id = add_role(session, args['name'], args['code'])
            return {'id': role_id}

    def patch(self):
        args = role_parser.parse_args()
        if args['id'] is None or args['id'] == '':
            return
        with session_scope() as session:
            toggle_role(session, args['id'])
        return


get_qualifications_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'created': fields.DateTime(attribute='insert_date_time', dt_format='iso8601'),
    'updated': fields.DateTime(attribute='update_date_time', dt_format='iso8601'),
    'deleted': fields.String(attribute='deleted'),
}

post_qualification_fields = {
    'id': fields.String,
}

qualification_parser = reqparse.RequestParser()
qualification_parser.add_argument('name', action='store', type=str)


class QualificationsRequest(Resource):
    @marshal_with(get_qualifications_fields)
    def get(self):
        with session_scope() as session:
            return get_qualifications(session)

    @marshal_with(post_qualification_fields)
    def post(self):
        args = qualification_parser.parse_args()
        if args['name'] is None or args['name'] == '':
            return
        with session_scope() as session:
            role_id = add_qualification(session, args['name'])
            return {'id': role_id}

    def patch(self):
        args = qualification_parser.parse_args()
        if args['name'] is None or args['name'] == '':
            return
        with session_scope() as session:
            toggle_qualification(session, args['name'])
        return
    
    
get_asset_type_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'code': fields.String,
    'created': fields.DateTime(attribute='insert_date_time', dt_format='iso8601'),
    'updated': fields.DateTime(attribute='update_date_time', dt_format='iso8601'),
    'deleted': fields.String(attribute='deleted'),
}

post_asset_type_fields = {
    'id': fields.String,
}

asset_type_parser = reqparse.RequestParser()
asset_type_parser.add_argument('name', action='store', type=str)
asset_type_parser.add_argument('code', action='store', type=str)


class AssetTypeRequest(Resource):
    @marshal_with(get_asset_type_fields)
    def get(self):
        with session_scope() as session:
            return get_asset_type(session)

    @marshal_with(post_asset_type_fields)
    def post(self):
        args = asset_type_parser.parse_args()
        if args['name'] is None or args['name'] == '':
            return
        if args['code'] is None or args['code'] == '':
            return
        with session_scope() as session:
            asset_type_id = add_asset_type(session, args['code'], args['name'])
            return {'id': asset_type_id}

    def patch(self):
        args = asset_type_parser.parse_args()
        if args['code'] is None or args['code'] == '':
            return
        with session_scope() as session:
            toggle_asset_type(session, args['code'])
        return


reference_bp = Blueprint('reference', __name__)
api = Api(reference_bp)
api.add_resource(RoleRequest, '/reference/roles')
api.add_resource(AssetTypeRequest, '/reference/asset_types')
api.add_resource(QualificationsRequest, '/reference/qualifications')
