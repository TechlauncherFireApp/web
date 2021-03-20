import json
import logging

from flask import Blueprint
from flask_restful import reqparse, Resource, fields, marshal_with, Api
from .utility import *
from domain import session_scope
from repository.volunteer_repository import *

'''
Define Data Input

type DayString = "Monday"|"Tuesday"|"Wednesday"|"Thursday"|"Friday"|"Saturday"|"Sunday"
type DecimalPair = [Decimal, Decimal]

GET
{
    "volunteerID": String
}

PATCH
{
    "volunteerID": String,
    "availability": {
        type DayString : [type DecimalPair]
    }
}

'''


def input_pair_list(pair, key):
    # Validate that the list is of length 2 (pairs)
    pair = type_list_of_length(pair, 2)
    # Validate the pairs of the list
    pair[0] = type_fixed(pair[0], 1)
    pair[1] = type_fixed(pair[1], 1)
    return pair


# Validate an avaiability input
def input_availability(value, name):
    # Validate that availability contains dictionaries
    value = type_dict(value)
    if type(value) is dict:
        for key in value.keys():
            # Validate that the key is correct
            key = type_enum(key, ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
            # Validate that the value is correct
            value = input_key_type(value, key, type_list_of, [input_pair_list, [key]])
    return value


parser = reqparse.RequestParser()
parser.add_argument('volunteerID', action='store', type=str)
parser.add_argument('availability', action='store', type=input_availability)

'''
Define Data Output

type DayString = "Monday"|"Tuesday"|"Wednesday"|"Thursday"|"Friday"|"Saturday"|"Sunday"
type DecimalPair = [Decimal, Decimal]

GET
{
    "availability": {
        type DayString : [type DecimalPair]
    }
}

PATCH
{
    "success" : Boolean
}
'''


def generate_availability_field():
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    output = {}
    for day in days:
        output[day] = fields.List(fields.List(fields.Float()), default=[])
    return output


get_resource_fields = {
    'availability': fields.Nested(generate_availability_field()),
    'success': fields.Boolean,
}

patch_resource_fields = {
    'success': fields.Boolean,
}


# Handle the Recommendation endpoint
class VolunteerAvailability(Resource):

    @marshal_with(get_resource_fields)
    def get(self):
        args = parser.parse_args()
        if args["volunteerID"] is None:
            return {"success": False}

        with session_scope() as session:
            res = get_volunteer(session, args["volunteerID"])
            return {"success": True, "availability": res.availabilities}

    @marshal_with(patch_resource_fields)
    def patch(self):
        args = parser.parse_args()
        if args["volunteerID"] is None or args["availability"] is None:
            return {"success": False}
        try:
            json.dumps(args["availability"])
        except:
            return {"success": False}
        with session_scope() as session:
            set_availabilities(session, args["volunteerID"], args["availability"])
            return {"success": True}


volunteer_availability_bp = Blueprint('volunteer_availability', __name__)
api = Api(volunteer_availability_bp)
api.add_resource(VolunteerAvailability, '/volunteer/availability')
