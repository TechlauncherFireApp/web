# Flask
from flask import Flask
from flask_restful import reqparse, abort, Resource, fields, marshal_with, inputs
# Gurobi
from gurobi.DataGenerator import LoadVolunteer
from gurobi.Scheduler import Schedule
from gurobi.AssetTypes import Request, LightUnit, MediumTanker, HeavyTanker
from gurobi.ManualAdditionCheck import ManualAdditionCheck, NameToAsset
# Helpers
from endpoints.helpers.input_validation import *

'''
Define data input
{
  assignment_list : [{
    shiftID: Integer,
    assetClass: String, [lightUnit | mediumTanker | heavyTanker]
    startTime: DateTimeString,
    endTime: DateTimeString,
    volunteers: [{
      ID: Integer,
      positionID: Integer,
      role: [String],
    }]
  }]
}
'''
# Validate a volunteer's position and role
def input_volunteer_position(value):
    # Validate that volunteers contains dictionaries
    value = type_dict(value)
    if type(value) is dict:
        # Validate volunteer values
        value = input_key_type(value, 'ID', type_string, [])
        value = input_key_type(value, 'positionID', type_natural, [])
        value = input_key_type(value, 'role', type_list_of, ['enum of form [\'basic\', \'advanced\', \'crewLeader\', \'driver\']',
                                            type_enum, [["basic", "advanced", "crewLeader", "driver"]]])
    return value

# Validate an asset request input
def input_assignment_req(value, name):
    # Validate that assignment_list contains dictionaries
    value = type_dict(value)
    if type(value) is dict:
        # Validate vehicle values
        value = input_key_type(value, 'shiftID', type_natural, [])
        value = input_key_type(value, 'assetClass', type_enum, [["heavyTanker", "mediumTanker", "lightUnit"]])
        value = input_key_type(value, 'startTime', type_dateTime, [])
        value = input_key_type(value, 'endTime', type_dateTime, [])
        # Validate the startTime is before the endTime
        if value['startTime'] >= value['endTime']:
            raise ValueError("The start_time '{}' cannot be after the end_time '{}'".format(value['start_time'], value['end_time']))
        # Validate the list of volunteers
        value = input_key_type(value, 'volunteers', type_list_of, ['volunteer(s)',
                                                    input_volunteer_position, []])
    return value


parser = reqparse.RequestParser()
parser.add_argument('assignment_list', action='append', type=input_assignment_req)

# Define data output
resource_fields = {
    'success': fields.Boolean,
    'errors': fields.List(fields.String)
}

# Handle the Recommendation endpoint
class Assignment(Resource):
    def __init__(self, **kwargs):
        # smart_engine is a black box dependency
        self.volunteer_list = kwargs['volunteer_list']

    @marshal_with(resource_fields)
    def post(self):
        errors = []
        args = parser.parse_args()
        # if args["asset_list"] is None:
        #     return
        print(args)

        for asset_request in args["assignment_list"]:
            # Turn the dictionary into a Request object
            shiftID = asset_request["shiftID"]
            assetClass = NameToAsset(asset_request["assetClass"])
            startTime = asset_request["startTime"]
            endTime = asset_request["endTime"]
            asset_request_test = Request(shiftID, assetClass, startTime, endTime)

            assigned_volunteers = []
            volunteers = asset_request["volunteers"]
            # Load the requested volunteers
            for volunteer in volunteers:
                volunteer_id = volunteer["ID"]
                loaded_volunteer = LoadVolunteer('volunteers',volunteer_id)
                loaded_volunteer.role = volunteer["role"]
                assigned_volunteers.append(loaded_volunteer)

            # Is assignment valid
            success, message = ManualAdditionCheck(asset_request_test, assigned_volunteers)
            return { "success" : success, "errors" : [message] }

        return { "success" : False, "errors" : errors }