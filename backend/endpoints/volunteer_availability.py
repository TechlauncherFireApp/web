# Flask
from flask import Flask
from flask_restful import reqparse, abort, Resource, fields, marshal_with, inputs
import re, json
# Helpers
from endpoints.helpers.input_validation import *
# Mysql

'''
Define Data Input

type DayString = "Monday"|"Tuesday"|"Wednesday"|"Thursday"|"Friday"|"Saturday"|"Sunday"
type IntegerPair = [Integer, Integer]
{
    "volunteerID": String,
    "availability": {
        type DayString : [type IntegerPair]
    }
}

'''
def input_pair_list(pair, key):
    # Validate that the list is of length 2 (pairs)
    pair = type_list_of_length(pair, 2)
    # Validate the pairs of the list
    pair[0] = type_natural(pair[0])
    pair[1] = type_natural(pair[1])
    return pair

# Validate an avaiability input
def input_availability(value, name):
    # Validate that availability contains dictionaries
    value = type_dict(value)
    if type(value) is dict:
        for key in value.keys():
            # Validate that the key is correct
            key = type_enum(key, ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"])
            # Validate that the value is correct
            value = input_key_type(value, key, type_list_of, [input_pair_list, [key]])
    return value

parser = reqparse.RequestParser()
parser.add_argument('volunteerID', action='store', type=str)
parser.add_argument('availability', action='append', type=input_availability)

'''
Define Data Output

{
    "success" : Boolean
}
'''

resource_fields = {
    'success': fields.Boolean,
}


# Handle the Recommendation endpoint
class VolunteerAvailability(Resource):
    @marshal_with(resource_fields)
    def patch(self):
        args = parser.parse_args()
        if args["volunteerID"] is None or args["availability"] is None:
            return { "results": None }

        # TODO Update the volunteers availability
        # Tom - I imagine this being like, remove the old availability and push the new availability

        return { "success": False}