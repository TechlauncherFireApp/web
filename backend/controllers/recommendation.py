from flask import Blueprint
from flask_restful import reqparse, Resource, fields, marshal_with, Api
from .utility import *
from services.optimiser import schedule
from repository.volunteer_repository import *
from domain import session_scope

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
def input_asset_req(value):
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
            raise ValueError(
                "The startTime '{}' cannot be after the endTime '{}'".format(value['startTime'], value['endTime']))
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
    'endTime': fields.DateTime(dt_format='iso8601', attribute=lambda x: x['timeframe'][1]),
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

        # Compile an asset request type for the scheduler
        asset_requests = []
        for shift_request in args["request"]:
            asset_request = {
                "shiftID": shift_request["shiftID"],
                "assetClass": shift_request["assetClass"],
                "timeframe": (shift_request["startTime"], shift_request["endTime"])
            }
            asset_requests.append(asset_request)

        # Get all volunteers
        with session_scope() as session:
            volunteers = list_volunteers(session)

            # Shouldn't have to have this switcher
            # for volunteer in volunteers:
            #     # Fix possibleRoles values.
            #     roles = []
            #     for role in volunteer["possibleRoles"]:
            #         switcher = {
            #             "Basic": "basic",
            #             "Advanced": "advanced",
            #             "Crew Leader": "crewLeader",
            #             "Driver": "driver"
            #         }
            #         roles.append(switcher[role])
            #     volunteer["possibleRoles"] = roles

            # Get the generated recommendation
            output = schedule(volunteers, asset_requests)

            if not output == []:
                print("Optimisation Succeeded")
                # print("Optimisation Succeeded:\n{}".format(output))

            return {"results": output}


recommendation_bp = Blueprint('recommendation', __name__)
api = Api(recommendation_bp)
api.add_resource(Recommendation, '/recommendation')
