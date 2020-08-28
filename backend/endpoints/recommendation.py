# Flask
from flask import Flask
from flask_restful import reqparse, abort, Resource, fields, marshal_with, inputs
# Gurobi
from gurobi.Scheduler import Schedule
# Helpers
from endpoints.helpers.input_validation import *
# Misc
from datetime import *
from pytz import UTC
# Mysql
from querys.volunteer import volunteer_all

'''
Define data input

{
  "request" : [{
    "shiftID": Integer,
    "assetClass": String, [lightUnit | mediumTanker | heavyTanker]
    "startTime": DateTimeString,
    "endTime": DateTimeString
  }]
}
'''

# Validate an asset shift_request input
def input_asset_req(value, name):
    # Validate that request contains dictionaries
    value = input_dict(value, name)
    if type(value) is dict:
        # Validate vehicle values
        value = input_key_positive(value, 'shiftID')
        value = input_key_enum(value, 'assetClass', ["heavyTanker", "mediumTanker", "lightUnit"])
        value = input_datetime(value, 'startTime')
        value = input_datetime(value, 'endTime')
        # TODO - further validation on DateTime values
        # Validate the start_time is before the end_time

        # if value['startTime'] >= value['endTime']:
        #     raise ValueError("The startTime '{}' cannot be after the endTime '{}'".format(value['startTime'], value['endTime']))
    return value

parser = reqparse.RequestParser()
parser.add_argument('request', action='append', type=input_asset_req)

'''
Define data output

{
    "results" : [{
        "shiftID": Integer
        "assetClass": String [lightUnit | mediumTanker | heavyTanker]
        "startTime": DateTimeString,
        "endTime": DateTimeString,
        "volunteers": {
            "ID": String,
            "positionID": Integer,
            "role": [String]
        }
    }]
}
'''

volunteer_field = {
    'ID': fields.String,
    'positionID': fields.Integer,
    'role': fields.List(fields.String)
}

recommendation_list_field = {
    'shiftID': fields.Integer,
    'assetClass': fields.String,
    'startTime': fields.DateTime(dt_format='rfc822', attribute=lambda x: x['timeframe'][0]),
    'endTime': fields.DateTime(dt_format='rfc822',  attribute=lambda x: x['timeframe'][1]),
    'volunteers': fields.List(fields.Nested(volunteer_field))
}

resource_fields = {
    'results': fields.List(fields.Nested(recommendation_list_field))
}

# Handle the Recommendation endpoint
class Recommendation(Resource):

    @marshal_with(resource_fields)
    def post(self):
        args = parser.parse_args()
        if args["request"] is None:
            return

        asset_requests = []
        for shift_request in args["request"]:
            asset_request = {
                "shiftID":shift_request["shiftID"],
                "assetClass":shift_request["assetClass"],
                "timeframe":(shift_request["startTime"], shift_request["endTime"])
            }
            asset_requests.append(asset_request)

        # TODO - remove once fixed below
        # volunteers = []
        # for i in range(12):
        #     volunteer = {}
        #     volunteer["ID"] = i
        #     volunteer["prefHours"] = 69945585 + 1
        #     volunteer["possibleRoles"] = ["basic", "advanced", "crewLeader", "driver"]
        #     start = datetime.min.replace(tzinfo=UTC)
        #     end = datetime.max.replace(tzinfo=UTC)
        #     volunteer["availabilities"] = [(start,end)]
        #     volunteers.append(volunteer)

        volunteers = volunteer_all()
        for volunteer in volunteers:
            # Fix datetime variables
            for availability in volunteer["availabilities"]:
                availability[0] = availability[0].replace(tzinfo=UTC)
                availability[1] = availability[1].replace(tzinfo=UTC)
            
            # Fix possibleRoles values. TODO standardise these
            for role in volunteer["possibleRoles"]:
                switcher = {
                    "Basic":"basic",
                    "Advanced":"advanced",
                    "Crew Leader":"crewLeader",
                    "Driver":"driver"
                }
                # TODO fix whatever is going on here
                # Desired Code doesn't work:
                # volunteer["possibleRoles"] = switcher[role]
                # This works:
                volunteer["possibleRoles"] = ["basic", "advanced", "crewLeader", "driver"]

        output = Schedule(volunteers, asset_requests)
        # TODO - Scheduler overrides each volunteer's ID string. Who's been assigned?

        if not output == []:
            # print("succeeded to optimise")
            print("succeeded to optimise, output:\n{}".format(output))

        return { "results" : output }