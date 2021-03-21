import json

from flask import Blueprint
from flask_restful import reqparse, Resource, fields, marshal_with, Api

from repository.asset_request_vehicle_repository import insert_vehicle, get_vehicle
from repository.asset_request_volunteer_repository import add_shift, update_shift_by_position, get_shifts_by_request
from .utility import *
from domain import session_scope
from repository.asset_request_volunteer_repository import *

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
        with session_scope() as session:
            rtn = []
            # Get a list of vehicles
            for row in get_shifts_by_request(session, args["requestID"]):
                d = row._asdict()
                volunteers = []
                # For each vehicle, get the volunteers in that vehicle
                for volunteer in get_volunteers(session, d['shiftID']):
                    volunteer_dict = volunteer._asdict()
                    if volunteer_dict['ID'] is None:
                        volunteer_dict['ID'] = '-1'
                    volunteers.append(volunteer_dict)
                d['volunteers'] = volunteers
                rtn.append(d)
        return {"results": rtn}


    @marshal_with(post_patch_resource_fields)
    def post(self):
        args = parser.parse_args()
        if args["shifts"] is None:
            return {"success": False}

        with session_scope() as session:
            for shift in args["shifts"]:
                vehicle_id = get_vehicle(session, shift['shiftID'])

                for volunteer in shift['volunteers']:
                    if volunteer['ID'] == '-1':
                        volunteer['ID'] = None
                    add_shift(session, volunteer['ID'], vehicle_id, volunteer['positionID'], volunteer['role'])
        return {"success": True}

    @marshal_with(post_patch_resource_fields)
    def patch(self):
        args = parser.parse_args()
        if args["shifts"] is None:
            return {"success": False}

        with session_scope() as session:
            for shift in args["shifts"]:
                for volunteer in shift['volunteers']:
                    if volunteer['ID'] == '-1' or volunteer['ID'] == -1:
                        volunteer['ID'] = None
                    update_shift_by_position(session, shift['shiftID'], volunteer['positionID'], volunteer['ID'], volunteer['role'])
        return {"success": True}


shift_request_bp = Blueprint('shift_request', __name__)
api = Api(shift_request_bp)
api.add_resource(ShiftRequest, '/shift/request')
