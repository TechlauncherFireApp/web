# Flask
from flask import Flask
from flask_restful import reqparse, abort, Resource, fields, marshal_with, inputs
import re, json
# Helpers
from endpoints.helpers.input_validation import *
# Mysql
from querys.volunteer import volunteer_all

'''
Define Data Input

GET
{
    "requestID": String
}

POST
{
    "requestID": String,
    "shifts": [{
        "shiftID": Integer,
        "assetClass": String,
        "startTime": DateTimeString,
        "endTime": DateTimeString,
        "volunteers": [{
            "ID": String,
            "positionID": Integer,
            "role": [String]
        }]
    }]
}


PATCH
{
    "requestID": String,
    "shifts": [{
        "shiftID": Integer,
        "assetClass": String,
        "startTime": DateTimeString,
        "endTime": DateTimeString,
        "volunteers": [{
            "ID": String,
            "positionID": Integer,
            "role": [String]
        }]
    }]
}

'''
# Validate a volunteer's position and role
def input_volunteer_position(value, name):
    # Validate that volunteers contains dictionaries
    value = type_dict(value, name)
    if type(value) is dict:
        # Validate volunteer values
        value = input_key_string(value, 'ID')
        value = input_key_natural(value, 'positionID')
        value = input_key_enum(value, 'role', ["basic", "advanced", "crewLeader", "driver"])
    return value

# Validate a shift input
def input_shift(value, name):
    # Validate that shifts contains dictionaries
    if type(value) is dict:
        # Validate shift values
        value = input_key_positive(value, 'shiftID')
        value = input_key_enum(value, 'assetClass', ["heavyTanker", "mediumTanker", "lightUnit"])
        value = input_datetime(value, 'startTime')
        value = input_datetime(value, 'endTime')
        # TODO - further validation on DateTime values
        # Validate the startTime is before the endTime

        # if value['startTime'] >= value['endTime']:
        #     raise ValueError("The startTime '{}' cannot be after the endTime '{}'".format(value['startTime'], value['endTime']))
        # value = input_volunteer_position(value, 'volunteers')
        # Validate each volunteer
        print(0)
        value = input_list_of(value, 'volunteers', 'dictionary(s)', type_dict, [])
        print(0)
        for num, volunteer in enumerate(value['volunteers']):
            volunteer = input_key_string(volunteer, 'ID')
            volunteer = input_key_natural(volunteer, 'positionID')
            volunteer = input_list_of(volunteer, 'role', 'enum of form [\'basic\', \'advanced\', \'crewLeader\', \'driver\']', type_enum, [["basic", "advanced", "crewLeader", "driver"]])
            # volunteer = input_key_enum(volunteer, 'role', ["basic", "advanced", "crewLeader", "driver"])
            value['volunteers'][num] = volunteer
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
        "shiftID": Integer,
        "assetClass": String, [lightUnit | mediumTanker | heavyTanker]
        "startTime": DateTimeString,
        "endTime": DateTimeString,
        "volunteers": [{
            "ID": String,
            "positionID": Integer,
            "role": [String]
        }]
    }]
}

POST
{
    "success" : Boolen
}

PATCH
{
    "success" : Boolen
}
'''

shift_volunteers_list_field = {
    "ID": fields.String,
    "positionID": fields.Integer,
    "role": fields.List(fields.String)
}

shift_list_field = {
    "shiftID": fields.Integer,
    "assetClass": fields.String,
    "startTime": fields.DateTime(dt_format='rfc822'),
    "endTime": fields.DateTime(dt_format='rfc822'),
    "volunteers": fields.List(fields.Nested(shift_volunteers_list_field)),
}

get_resource_fields = {
    'results': fields.List(fields.Nested(shift_list_field)),
}

post_patch_resource_fields = {
    "success" : fields.Boolean
}

# Handle the ShiftRequest endpoint
class ShiftRequest(Resource):
    @marshal_with(get_resource_fields)
    def get(self):
        args = parser.parse_args()
        if args["requestID"] is None:
            return
        
        requestID = args["requestID"]
        #TODO Get a shift request from it's requestID


        return { "results": None }
    
    @marshal_with(post_patch_resource_fields)
    def post(self):
        args = parser.parse_args()
        if args["requestID"] is None or args["shifts"] is None:
            return { "success": False }
        
        requestID = args["requestID"]
        shifts = args["shifts"]
        #TODO Create a new shift request object in database


        return { "success": False }

    @marshal_with(post_patch_resource_fields)
    def patch(self):
        args = parser.parse_args()
        if args["requestID"] is None or args["shifts"] is None:
            return { "success": False }
        
        requestID = args["requestID"]
        shifts = args["shifts"]
        #TODO Update a shift request object in database


        return { "success": False }