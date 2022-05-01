import json
import logging

from flask import Blueprint
from flask_restful import reqparse, Resource, fields, marshal_with, Api

unavailable_fields = {

}

class VolunteerUnavailability(Resource):
    @marshal_with(unavailable_fields)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument()


volunteer_unavailability_bp = Blueprint('volunteer_unavailability', __name__)
api = Api(volunteer_unavailability_bp)
api.add_resource(VolunteerUnavailability, '/volunteer/unavailability')
