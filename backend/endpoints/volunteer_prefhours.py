# Flask
from flask import Flask
from flask_restful import reqparse, abort, Resource, fields, marshal_with, inputs
import re, json

'''
Define Data Input

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

{
    "success" : Boolean
}
'''

resource_fields = {
    'success': fields.Boolean,
}


# Handle the Recommendation endpoint
class VolunteerPrefhours(Resource):
    @marshal_with(resource_fields)
    def patch(self):
        args = parser.parse_args()
        if args["volunteerID"] is None or args["prefHours"] is None:
            return { "success": None }

        # TODO Update the volunteer's prefHours

        return { "success": False }