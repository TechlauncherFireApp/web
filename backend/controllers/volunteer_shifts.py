from flask import Blueprint
from flask_restful import reqparse, Resource, fields, marshal_with, Api
from domain import session_scope
from repository.asset_request_volunteer_repository import *

'''
Define Data Input
 {
     volunteerID: String
 }

'''

parser = reqparse.RequestParser()
parser.add_argument('volunteerID', action='store', type=str)

'''
Define Data Output

get every: asset-request_volunteer.idVolunteer == volunteerID
need data from four different tables in database
{
    "results" : [{
        "requestTitle":     String      (asset-request.title)
        "vehicleID":        String      (asset-request_vehicle.id)
        "vehicleType":      String      (vehicle.type)
        "vehicleFrom":      DateTimeString iso8601      (asset-request_vehicle.from)
        "vehicleTo":        DateTimeString iso8601      (asset-request_vehicle.to)
        "volunteerRoles":   [String]    (asset-request_volunteer.roles)
        "volunteerStatus":  String      (asset-request_volunteer.status)
    }]
}
'''

result_list_field = {
    'requestTitle': fields.String,
    'vehicleID': fields.String,
    'vehicleType': fields.String,
    'vehicleFrom': fields.DateTime(dt_format='iso8601'),
    'vehicleTo': fields.DateTime(dt_format='iso8601'),
    'volunteerRoles': fields.String,
    'volunteerStatus': fields.String,
}

resource_fields = {
    'results': fields.List(fields.Nested(result_list_field)),
}


# Handle the volunteer/shifts endpoint
class VolunteerShifts(Resource):

    @marshal_with(resource_fields)
    def get(self):
        args = parser.parse_args()
        if args["volunteerID"] is None:
            return {"success": False}

        with session_scope() as session:
            rtn = []
            for row in get_request_by_volunteer(session, args["volunteerID"]):
                # Access protected _asdict() to return the keyed tuple as a dict to enable flask_restful to marshal
                # it correctly. The alternative method is less tidy.
                rtn.append(row._asdict())
            return {"success": True, "results": rtn}


volunteer_shifts_bp = Blueprint('volunteer_shifts', __name__)
api = Api(volunteer_shifts_bp)
api.add_resource(VolunteerShifts, '/volunteer/shifts')
