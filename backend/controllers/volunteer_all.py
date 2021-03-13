from flask import Blueprint
from flask_restful import Resource, fields, marshal_with, Api

'''
No Data Input
--
Define Data Output

{
    "results" : [{
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
    }]
}
'''

volunteer_list_field = {
    'ID': fields.String,
    'firstName': fields.String,
    'lastName': fields.String,
    'email': fields.String,
    'mobileNo': fields.String,
    'prefHours': fields.Integer,
    'expYears': fields.Integer,
    'possibleRoles': fields.List(fields.String),
    'qualifications': fields.List(fields.String),
    'availabilities': fields.List(fields.List(fields.DateTime(dt_format='iso8601')))
}

resource_fields = {
    'results': fields.List(fields.Nested(volunteer_list_field)),
}


# Handle the Recommendation endpoint
class VolunteerAll(Resource):
    @marshal_with(resource_fields)
    def get(self):
        # Get all volunteers from mysql

        # TODO Convert possible positions
        volunteers = volunteer_all(False)

        # Fix possibleRoles values. TODO standardise these
        for volunteer in volunteers:
            for index, role in enumerate(volunteer["possibleRoles"]):
                switcher = {
                    "Basic": "basic",
                    "Advanced": "advanced",
                    "Crew Leader": "crewLeader",
                    "Driver": "driver"
                }
                volunteer["possibleRoles"][index] = switcher[role]

        return {"results": volunteers}


volunteer_all_bp = Blueprint('volunteer_all', __name__)
api = Api(volunteer_all_bp)
api.add_resource(VolunteerAll, '/volunteer/all')