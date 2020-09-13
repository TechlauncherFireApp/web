# Flask
from flask import Flask
from flask_restful import reqparse, abort, Resource, fields, marshal_with, inputs
import re, json
# Mysql
from querys.volunteer import volunteer
from includes.main import contains
from includes.connection_mysqli import get as connection, is_connected, cur_conn_close


'''
Define Data Input
 {
     volunterrID: String
 }

'''

parser = reqparse.RequestParser()
parser.add_argument('volunteerID', action='store', type=str)


'''
Define Data Output

{
    "id": String
    "firstName": String
    "lastName": String
    "email": String
    "mobileNo": String
    "prefHours": Integer
    "expYears": Integer
    "possibleRoles": [String]
    "qualifications": [String]
    "availabilities": [[DateTimeString iso8601, DateTimeString iso8601]]
}
'''

resource_fields = {
    'ID': fields.String,
    'firstName': fields.String,
    'lastName': fields.String,
    'email': fields.String,
    'mobileNo': fields.String,
    'prefHours':fields.Integer,
    'expYears': fields.Integer,
    'possibleRoles': fields.List(fields.String),
    'qualifications': fields.List(fields.String),
    'availabilities': fields.List(fields.List(fields.DateTime(dt_format='iso8601')))
}


# Handle the Recommendation endpoint
class Volunteer(Resource):

    @marshal_with(resource_fields)
    def get(self):
        args = parser.parse_args()
        if args["volunteerID"] is None:
            return { "success": False }

        # Get a spepcific volunteer from mysql

        # TODO Convert possible positions
        volunteerID = args["volunteerID"]
        
        volunteer_obj = volunteer(False, volunteerID)
        volunteer_obj["ID"] = volunteerID
        volunteer_obj["success"] = True
        print(volunteer_obj)

        return volunteer_obj