import os
from io import BytesIO

import werkzeug.utils
import werkzeug.datastructures
from flask import Blueprint, request, Response
from flask_restful import fields, Resource, marshal_with, Api, reqparse

from domain import session_scope
from repository.tenancy_config_repository import *


parser = reqparse.RequestParser()
parser.add_argument('id', action='store', type=str)
parser.add_argument('getAll', action='store', type=str)
parser.add_argument('name', action='store', type=str)
parser.add_argument('title', action='store', type=str)
parser.add_argument('font', action='store', type=str)
parser.add_argument('navColour', action='store', type=str)
parser.add_argument('backColour', action='store', type=str)

config_list_field = {
    'id': fields.String,
    'name': fields.String,
    'title': fields.String,
    'font': fields.String,
    'nav_colour': fields.String(attribute='navbar_colour'),
    'back_colour': fields.String(attribute='background_colour'),
    'deleted': fields.String(attribute='deleted')
}

get_config_fields = {
    'success': fields.Boolean,
    'results': fields.List(fields.Nested(config_list_field)),
}

config_fields = {
    'success': fields.Boolean,
    'id': fields.Integer
}


ALLOWED_EXTENSIONS = ["PNG", "JPG", "JPEG"]


def allowed_image(filename):
    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in ALLOWED_EXTENSIONS:
        return True
    else:
        return False


class TenancyConfig(Resource):
    @marshal_with(get_config_fields)
    def get(self):
        args = parser.parse_args()
        with session_scope() as session:
            if args['getAll'] == 'true':
                res = get_all_configs(session)
                return {'success': True, 'results': res}
            res = get_active_config(session)
            return {'success': True, 'results': res}

    @marshal_with(config_fields)
    def post(self):
        args = parser.parse_args()
        if args['name'] is None or args['name'] == '' or args['title'] is None \
                or args['title'] == '':
            return {'success': False}

        if request.files:
            pic = request.files['logo']
            blob = pic.read()
            pic.seek(0)
            filename = werkzeug.utils.secure_filename(pic.filename)
            if not allowed_image(filename) or len(blob) > 64000:
                return {'success': False}
            mimetype = pic.mimetype
            with session_scope() as session:
                config_id = insert_config(session, args['name'], args['title'], args['font'], pic.read(), filename,
                                          mimetype, args['navColour'], args['backColour'])
                return {'success': True, 'id': config_id}

        with session_scope() as session:
            config_id = insert_config(session, args['name'], args['title'], args['font'], '', '',
                                      '', args['navColour'], args['backColour'])
            return {'success': True, 'id': config_id}

    @marshal_with(config_fields)
    def patch(self):
        args = parser.parse_args()
        if args['id'] is None or args['id'] == '':
            return {'success': False}
        with session_scope() as session:
            toggle_config(session, args['id'])
        return {'success': True}

    @marshal_with(config_fields)
    def delete(self):
        args = parser.parse_args()
        if args['id'] is None or args['id'] == '':
            return {'success': False}
        with session_scope() as session:
            delete_config(session, args['id'])
        return {'success': True}


class ImageRequest(Resource):
    def get(self):
        with session_scope() as session:
            img = get_img(session)
            return Response(BytesIO(img.logo), mimetype=img.logo_mimetype)


tenancy_config_bp = Blueprint('tenancy_config', __name__)
api = Api(tenancy_config_bp)
api.add_resource(TenancyConfig, '/tenancy_config')
api.add_resource(ImageRequest, '/tenancy_img')
