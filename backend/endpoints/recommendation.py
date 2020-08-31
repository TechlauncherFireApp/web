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
    "shiftID": String,
    "assetClass": String, [lightUnit | mediumTanker | heavyTanker]
    "startTime": DateTimeString iso8601,
    "endTime": DateTimeString iso8601
  }]
}
'''

# Validate an asset shift_request input
def input_asset_req(value, name):
    # Validate that request contains dictionaries
    value = type_dict(value)
    if type(value) is dict:
        # Validate vehicle values
        value = input_key_type(value, 'shiftID', type_string, [])
        value = input_key_type(value, 'assetClass', type_enum, [["heavyTanker", "mediumTanker", "lightUnit"]])
        value = input_key_type(value, 'startTime', type_datetime, [])
        value = input_key_type(value, 'endTime', type_datetime, [])
        # Validate the startTime is before the endTime
        if value['startTime'] >= value['endTime']:
            raise ValueError("The startTime '{}' cannot be after the endTime '{}'".format(value['startTime'], value['endTime']))
    return value

parser = reqparse.RequestParser()
parser.add_argument('request', action='append', type=input_asset_req)

'''
Define data output

{
    "results" : [{
        "shiftID": String
        "assetClass": String [lightUnit | mediumTanker | heavyTanker]
        "startTime": DateTimeString iso8601,
        "endTime": DateTimeString iso8601,
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
    'shiftID': fields.String,
    'assetClass': fields.String,
    'startTime': fields.DateTime(dt_format='iso8601', attribute=lambda x: x['timeframe'][0]),
    'endTime': fields.DateTime(dt_format='iso8601',  attribute=lambda x: x['timeframe'][1]),
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

        volunteers = volunteer_all(True)
        for volunteer in volunteers:
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

        if not output == []:
            print("Optimisation Succeeded")
            # print("Optimisation Succeeded:\n{}".format(output))

        return { "results" : output }