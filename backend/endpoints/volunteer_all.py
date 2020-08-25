# Flask
from flask import Flask
from flask_restful import reqparse, abort, Resource, fields, marshal_with, inputs


'''
No Data Input
--
Define Data Output

{
    "results" : [{
        “id": String
        "firstName": String
        "lastName": String
        "email": String
        "mobileNo": String
        "prefHours": Integer
        "expYears": Integer
        "possibleRoles": [String]
        "qualifications": [String]
        "availabilities": [[startDateTime, endDateTime]]
    }]
}
'''

volunteer_list_field = {
    'volunteer_id': fields.String,
    'firstName': fields.String,
    'lastName': fields.String,
    'email': fields.String,
    'mobileNo': fields.String,
    'prefHours':fields.Integer,
    'expYears': fields.Integer,
    'possibleRoles': fields.List(fields.String),
    'qualifications': fields.List(fields.String),
    'availabilities': fields.List(fields.List(fields.String))
}

resource_fields = {
    'results': fields.List(fields.Nested(volunteer_list_field)),
}

# Handle the Recommendation endpoint
class VolunteerAll(Resource):
    @marshal_with(resource_fields)
    def get(self):
        #TODO Get all volunteers from mysql

        # Return the results
        output = []
        return {'results': output}
