from flask import Blueprint
from flask_restful import fields, Resource, marshal_with, Api, reqparse

from domain import session_scope
from repository.tenancy_config_repository import *


parser = reqparse.RequestParser()
parser.add_argument('getAll', action='store', type=bool)
parser.add_argument('name', action='store', type=str)
parser.add_argument('title', action='store', type=str)
parser.add_argument('font', action='store', type=str)
parser.add_argument('navColour', action='store', type=str)
parser.add_argument('backColour', action='store', type=str)

config_list_field = {
    'id': fields.String,
    'name': fields.String,
    'font': fields.String,
    'nav_colour': fields.String,
    'back_colour': fields.String,
    'deleted': fields.String(attribute='deleted')
}

get_config_fields = {
    'success': fields.Boolean,
    'results': fields.List(fields.Nested(config_list_field))
}


class TenancyConfig(Resource):
    # TODO Create Tenancy Configuration API
    @marshal_with(get_config_fields)
    def get(self):
        args = parser.parse_args()


tenancy_config_bp = Blueprint('tenancy_config', __name__)
api = Api(tenancy_config_bp)
api.add_resource(TenancyConfig, '/tenancy_config')
