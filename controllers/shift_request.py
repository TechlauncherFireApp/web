from flask import Blueprint
from flask_restful import reqparse, Resource, fields, marshal_with, Api

from .utility import *
from domain import session_scope
from repository.asset_request_volunteer_repository import *


# Validate a volunteer's position and role
def input_volunteer_position(value):
    # Validate that volunteers contains dictionaries
    value = type_dict(value)
    if type(value) is dict:
        # Validate volunteer values
        value = input_key_type(value, 'ID', type_string, [])
        value = input_key_type(value, 'role', type_string, [])
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
parser.add_argument('requestID', action='store', type=str)
parser.add_argument('shifts', action='append', type=input_shift)

shift_volunteers_list_field = {
    "volunteerId": fields.Integer,
    "volunteerGivenName": fields.String,
    "volunteerSurname": fields.String,
    "mobile_number": fields.String,
    "positionId": fields.Integer,
    "role": fields.String,
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

modify_parser = reqparse.RequestParser()
modify_parser.add_argument('shift_id', action='store', type=int)
modify_parser.add_argument('position_id', action='store', type=int)
modify_parser.add_argument('volunteer_id', action='store', type=int)


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
                    if volunteer_dict['volunteerId'] is None:
                        volunteer_dict['volunteerId'] = -1
                    volunteers.append(volunteer_dict)
                d['volunteers'] = volunteers
                rtn.append(d)
        return {"results": rtn}

    @marshal_with(post_patch_resource_fields)
    def delete(self):
        args = modify_parser.parse_args()
        with session_scope() as session:
            remove_assignment(session, args['shift_id'], args['position_id'])
        return {"success": True}

    @marshal_with(post_patch_resource_fields)
    def patch(self):
        args = modify_parser.parse_args()
        print(args)
        with session_scope() as session:
            update_shift_by_position(session, args['shift_id'], args['position_id'], args['volunteer_id'])
        return {"success": True}


shift_request_bp = Blueprint('shift_request', __name__)
api = Api(shift_request_bp)
api.add_resource(ShiftRequest, '/shift/request')
