import json

from flask import Blueprint
from flask_restful import reqparse, Resource, fields, marshal_with, Api

from .utility import *
from backend.domain import session_scope
from backend.repository.asset_request_volunteer_repository import *

'''
Define Data Input

GET
{
    "requestID": String
}

POST
{
    "shifts": [{
        "shiftID": String,
        "volunteers": [{
            "ID": String,
            "positionID": Integer,
            "role": [String], [basic | advanced | crewLeader | driver]
        }]
    }]
}

PATCH
{
    "shifts": [{
        "shiftID": String,
        "volunteers": [{
            "ID": String,
            "positionID": Integer,
            "role": [String], [basic | advanced | crewLeader | driver]
        }]
    }]
}

'''


# Validate a volunteer's position and role
def input_volunteer_position(value):
    # Validate that volunteers contains dictionaries
    value = type_dict(value)
    if type(value) is dict:
        # Validate volunteer values
        value = input_key_type(value, 'ID', type_string, [])
        value = input_key_type(value, 'positionID', type_natural, [])
        value = input_key_type(value, 'role', type_list_of,
                               [type_enum, [["basic", "advanced", "crewLeader", "driver"]]])
    return value


# Validate a shift input
def input_shift(value, name):
    # Validate that shifts contains dictionaries
    value = type_dict(value)
    if type(value) is dict:
        # Validate shift values
        value = input_key_type(value, 'shiftID', type_string, [])
        # Validate the list of volunteers
        value = input_key_type(value, 'volunteers', type_list_of, [input_volunteer_position, []])
    return value


parser = reqparse.RequestParser()
# Define search criteria
parser.add_argument('requestID', action='store', type=str)
parser.add_argument('shifts', action='append', type=input_shift)

'''
Define data output

GET
{
    "results" : [{
        "shiftID": String,
        "assetClass": String, [lightUnit | mediumTanker | heavyTanker]
        "startTime": DateTimeString iso8601,
        "endTime": DateTimeString iso8601,
        "volunteers": [{
            "ID": String,
            "positionID": Integer,
            "roles": [String], [basic | advanced | crewLeader | driver]
        }]
    }]
}

POST
{
    "success" : Boolean
}

PATCH
{
    "success" : Boolean
}
'''

shift_volunteers_list_field = {
    "ID": fields.String,
    "positionID": fields.Integer,
    "role": fields.List(fields.String),
    "status": fields.String,
}

shift_list_field = {
    "shiftID": fields.String,
    "assetClass": fields.String,
    "startTime": fields.DateTime(dt_format='iso8601'),
    "endTime": fields.DateTime(dt_format='iso8601'),
    "volunteers": fields.List(fields.Nested(shift_volunteers_list_field)),
}

get_resource_fields = {
    'results': fields.List(fields.Nested(shift_list_field)),
}

post_patch_resource_fields = {
    "success": fields.Boolean
}


# Handle the ShiftRequest endpoint
class ShiftRequest(Resource):
    @marshal_with(get_resource_fields)
    def get(self):
        args = parser.parse_args()
        if args["requestID"] is None:
            return {"results": None}

        return self.get_func(args["requestID"])

    # @marshal_with(get_resource_fields)
    def get_func(self, request_id):
        with session_scope() as session:
            o = []
            rtn = []
            for row in get_shifts_by_request(session, request_id):
                # Access protected _asdict() to return the keyed tuple as a dict to enable flask_restful to marshal
                # it correctly. The alternative method is less tidy.
                rtn.append(row._asdict())

            # TODO: Tech Debt
            #   - Find out what this code is trying to do
            for y in rtn:
                if y["ID"] == None:
                    y["ID"] = "-1"
                n = True
                for i, x in enumerate(o):
                    if x["shiftID"] == y["shiftID"]:
                        o[i]["volunteers"].append(
                            {"ID": y["ID"], "positionID": y["positionID"], "role": json.loads(y["role"]),
                             "status": y["status"]})
                        n = False
                        break
                if n: o.append({"shiftID": y["shiftID"], "assetClass": y["assetClass"], "startTime": y["startTime"],
                                "endTime": y["endTime"], "volunteers": [
                        {"ID": y["ID"], "positionID": y["positionID"], "role": y["role"],
                         "status": y["status"]}]})

                return {"results": o}
        return {"results": None}

    @marshal_with(post_patch_resource_fields)
    def post(self):
        args = parser.parse_args()
        if args["shifts"] is None:
            return {"success": False}

        with session_scope() as session:
            for shift in args["shifts"]:
                for volunteer in shift['volunteers']:
                    add_shift(session, volunteer['ID'], shift['shiftID'], volunteer['positionID'], volunteer['role'])
        return {"success": True}

    @marshal_with(post_patch_resource_fields)
    def patch(self):
        args = parser.parse_args()
        if args["shifts"] is None:
            return {"success": False}

        with session_scope() as session:
            for shift in args["shifts"]:
                for volunteer in shift['volunteers']:
                    update_shift_by_position(session, volunteer['ID'], shift['shiftID'], volunteer['positionID'],
                                             volunteer['role'])
        return {"success": True}


shift_request_bp = Blueprint('shift_request', __name__)
api = Api(shift_request_bp)
api.add_resource(ShiftRequest, '/shift/request')
