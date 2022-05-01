import json
import logging

from flask import Blueprint
from flask_restful import reqparse, Resource, fields, marshal_with, Api

get_resource_fields = {
    'schedule': fields.List,
    'success': fields.Boolean,
}

class VolunteerUnavailability(Resource):
    @marshal_with(get_resource_fields)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument()


volunteer_unavailability_bp = Blueprint('volunteer_unavailability', __name__)
api = Api(volunteer_unavailability_bp)
api.add_resource(VolunteerUnavailability, '/volunteer/unavailability')
