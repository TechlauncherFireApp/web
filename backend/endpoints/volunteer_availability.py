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
# Validate an avaiability input
def input_availability(value, name):
    # Validate that availabilitys contains dictionaries
    value = type_dict(value)
    if type(value) is dict:
        # 
        for key in value.keys():
            key = type_enum(key, ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"])
        #
        for pair_list in value.values():
            pair_list = type_list(pair_list)
            # 
            for pair in pair_list:
                pair = type_list_of_length(pair, 2)
                pair[0] = type_natural(pair[0])
                pair[1] = type_natural(pair[1])
            
    return value

parser = reqparse.RequestParser()
# Define search criteria
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

        return { "success": False}