# Flask
from flask import Flask
from flask_restful import reqparse, abort, Resource, fields, marshal_with, inputs
import re, json

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
class VolunteerPrefhours(Resource):
    @marshal_with(get_resource_fields)
    def get(self):
        args = parser.parse_args()
        if args["volunteerID"] is None:
            return { "success": False }

        # TODO Get the volunteer's prefHours

        return { "success": False, "prefHours": None }

    @marshal_with(patch_resource_fields)
    def patch(self):
        args = parser.parse_args()
        if args["volunteerID"] is None or args["prefHours"] is None:
            return { "success": False }

        # TODO Update the volunteer's prefHours

        return { "success": False }