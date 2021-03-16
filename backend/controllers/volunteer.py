from flask import Blueprint
from flask_restful import reqparse, Resource, fields, marshal_with, Api

from backend.domain import session_scope
from backend.repository.volunteer_repository import *

'''
Define Data Input
 {
     volunterrID: String
 }

'''

parser = reqparse.RequestParser()
parser.add_argument('volunteerID', action='store', type=str)

availability_field = {
    "Monday": fields.List(fields.List(fields.Integer)),
    "Tuesday": fields.List(fields.List(fields.Integer)),
    "Wednesday": fields.List(fields.List(fields.Integer)),
    "Thursday": fields.List(fields.List(fields.Integer)),
    "Friday": fields.List(fields.List(fields.Integer)),
    "Saturday": fields.List(fields.List(fields.Integer)),
    "Sunday": fields.List(fields.List(fields.Integer)),
}

resource_fields = {
    'ID': fields.String,
    'firstName': fields.String,
    'lastName': fields.String,
    'email': fields.String,
    'mobileNo': fields.String,
    'prefHours': fields.Integer,
    'expYears': fields.Integer,
    'possibleRoles': fields.List(fields.String),
    'qualifications': fields.List(fields.String),
    'availabilities': fields.Nested(availability_field)
}


# Handle the Recommendation endpoint
class Volunteer(Resource):

    @marshal_with(resource_fields)
    def get(self):
        args = parser.parse_args()
        if args["volunteerID"] is None:
            return {"success": False}

        with session_scope() as session:
            rtn = []
            for row in list_volunteers(session, args["volunteerID"]):
                # Access protected _asdict() to return the keyed tuple as a dict to enable flask_restful to marshal
                # it correctly. The alternative method is less tidy.
                rtn.append(row._asdict())
            return rtn[0]


volunteer_bp = Blueprint('volunteer', __name__)
api = Api(volunteer_bp)
api.add_resource(Volunteer, '/volunteer')