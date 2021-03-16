from flask import Blueprint
from flask_restful import reqparse, Resource, fields, marshal_with, Api
from backend.domain import session_scope
from backend.repository.asset_request_volunteer_repository import *

'''
Define Data Input

GET
{
    idVolunteer: String
    idVehicle: String
}

PATCH
{
    idVolunteer: String
    idVehicle: String
    Status: String 
}

'''

parser = reqparse.RequestParser()
parser.add_argument('idVolunteer', action='store', type=str)  # unsure about this line
parser.add_argument('idVehicle', action='store', type=str)
parser.add_argument('status', action='store', type=str)

'''
Define Data Output

GET
{
    status: String
}

PATCH
{
    success: boolean
}

'''

get_resource_fields = {
    'status': fields.String,
    'success': fields.Boolean
}

patch_resource_fields = {
    'success': fields.Boolean
}


class VolunteerStatus(Resource):

    @marshal_with(get_resource_fields)
    def get(self):
        args = parser.parse_args()
        if args["idVolunteer"] is None or args["idVehicle"] is None:
            return {"status": None, "success": False}

        with session_scope() as session:
            res = get_asset_request_volunteer(session, args["idVolunteer"], args["idVehicle"])
            return {"success": True, "status": res.status}

    @marshal_with(patch_resource_fields)
    def patch(self):

        args = parser.parse_args()
        if args["idVolunteer"] is None or args["idVehicle"] is None or args["status"] is None:
            return {"success": False}
        if args['status'] not in ["confirmed", "rejected"]: return {"success": False}

        with session_scope() as session:
            set_asset_request_volunteer_status(session, args['status'], args["idVolunteer"], args["idVehicle"])
            return {"success": True}


volunteer_status_bp = Blueprint('volunteer_status', __name__)
api = Api(volunteer_status_bp)
api.add_resource(VolunteerStatus, '/volunteer/status')
