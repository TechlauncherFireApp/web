from flask import Blueprint
from flask_restful import reqparse, Resource, fields, marshal_with, Api
from ..domain import session_scope
from ..repository.volunteer_repository import get_volunteer, set_preferred_hours

'''
Define Data Input

GET
{
    "volunteerID": String
}

PATCH
{
    "volunteerID": String,
    "prefHours": Integer
}

'''

parser = reqparse.RequestParser()
parser.add_argument('volunteerID', action='store', type=str)
parser.add_argument('prefHours', action='store', type=int)

'''
Define Data Output

GET
{
    "prefHours": Integer
}

PATCH
{
    "success" : Boolean
}
'''

get_resource_fields = {
    'prefHours': fields.Integer,
    'success': fields.Boolean
}

patch_resource_fields = {
    'success': fields.Boolean,
}


# Handle the Recommendation endpoint
class VolunteerPreferredHours(Resource):

    @marshal_with(get_resource_fields)
    def get(self):
        args = parser.parse_args()
        if args["volunteerID"] is None:
            return {"success": False}

        with session_scope() as session:
            res = get_volunteer(session, args['volunteerID'])
            return {"success": True, "prefHours": res.preferred_hours}

    @marshal_with(patch_resource_fields)
    def patch(self):
        args = parser.parse_args()
        if args["volunteerID"] is None or args["prefHours"] is None:
            return {"success": False}

        with session_scope() as session:
            set_preferred_hours(session, args['volunteerID'], args["prefHours"])
            return {"success": True}


volunteer_preferred_hours_bp = Blueprint('volunteer_preferred_hours', __name__)
api = Api(volunteer_preferred_hours_bp)
api.add_resource(VolunteerPreferredHours, '/volunteer/prefhours')
