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

'''
Define data input

# TODO
# Cannot represent timeframe as 'timeframe = (startTime, endTime)'
# Discuss to use either
# timeframe = [startTime, endTime]
# or separate startTime, endTime keys
#

{
  "request" : [{
    "shiftID": Integer,
    "assetClass": String, [lightUnit | mediumTanker | heavyTanker]
    "startTime": DateTime,
    "endTime": DateTime
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
        "volunteers": {
            "ID": Integer,
            "positionID": Integer,
            "role": String
        }
    }]
}
'''

volunteer_field = {
    'ID': fields.Integer,
    'positionID': fields.Integer,
    'role': fields.List(fields.String)
}

recommendation_list_field = {
    'shiftID': fields.Integer,
    'assetClass': fields.String,
    'volunteers': fields.List(fields.Nested(volunteer_field))
}

resource_fields = {
    'results': fields.List(fields.Nested(recommendation_list_field))
}

# Handle the Recommendation endpoint
class Recommendation(Resource):
    # def __init__(self, **kwargs):
    #     pass

    @marshal_with(resource_fields)
    def post(self):
        args = parser.parse_args()
        # if args["request"] is None:
        #     return
        print(args)

        asset_requests = []
        for shift_request in args["request"]:
            asset_request = {
                "shiftID":shift_request["shiftID"],
                "assetClass":shift_request["assetClass"],
                "timeframe":(shift_request["startTime"], shift_request["endTime"])
            }
            asset_requests.append(asset_request)

        '''
        Temporary test block code.
        Replace with database volunteers.
        '''
        Volunteers = []
        for i in range(12):
            volunteer = {}
            volunteer["ID"] = i
            volunteer["prefHours"] = 69945585 + 1
            volunteer["possibleRoles"] = ["basic", "advanced", "crewLeader", "driver"]
            start = datetime.min.replace(tzinfo=UTC)
            end = datetime.max.replace(tzinfo=UTC)
            volunteer["availabilities"] = [(start,end)]
            Volunteers.append(volunteer)

        # try:
        output = Schedule(Volunteers, asset_requests)
        print("succeeded to optimise")
        # print("succeeded to optimise, output:\n{}".format(output))

        return {
            "results" : output
        }