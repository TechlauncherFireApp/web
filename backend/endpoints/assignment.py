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

# Define data input
# {
#   assignment_list : [{
#     asset_id: Integer,
#     asset_name: String,
#     start_time: TimeBlock,
#     end_time: TimeBlock,
#     volunteers: [{
#       volunteer_id: Integer,
#       position_id: Integer,
#       role: String,
#     }]
#   }]
# }

# Validate an asset request input
def input_assignment_req(value, name):
    # Validate that assignment_list contains dictionaries
    value = input_dict(value, name)
    if type(value) is dict:
        # Validate vehicle values
        value = input_key_positive(value, 'asset_id')
        value = input_key_enum(value, 'asset_name', ["Heavy Tanker", "Medium Unit", "Light Unit"])
        value = input_timeblock(value, 'start_time')
        value = input_timeblock(value, 'end_time')
        # Validate the start_time is before the end_time
        if value['start_time'] >= value['end_time']:
            raise ValueError("The start_time '{}' cannot be after the end_time '{}'".format(value['start_time'], value['end_time']))
        # Validate that 'volunteers' is a list of dictionaries
        value = input_list_of(value, 'volunteers', 'dictionary(s)', input_dict, ['in volunteers'])
        # Validate each volunteer
        for num, volunteer in enumerate(value['volunteers']):
            volunteer = input_key_natural(volunteer, 'volunteer_id')
            volunteer = input_key_natural(volunteer, 'position_id')
            volunteer = input_key_enum(volunteer, 'role', ["Crew Member","CrewLeader", "CrewLeader/Driver", "Driver"])
            value['volunteers'][num] = volunteer
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
            asset_id = asset_request["asset_id"]
            asset_type = NameToAsset(asset_request["asset_name"])
            start_time = asset_request["start_time"]
            end_time = asset_request["end_time"]
            asset_request_test = Request(asset_id, asset_type, start_time, end_time)

            assigned_volunteers = []
            volunteers = asset_request["volunteers"]
            # Load the requested volunteers
            for volunteer in volunteers:
                volunteer_id = volunteer["volunteer_id"]
                loaded_volunteer = LoadVolunteer('volunteers',volunteer_id)
                loaded_volunteer.role = volunteer["role"]
                assigned_volunteers.append(loaded_volunteer)

            # Is assignment valid
            success, message = ManualAdditionCheck(asset_request_test, assigned_volunteers)
            return { "success" : success, "errors" : [message] }

        return { "success" : False, "errors" : errors }