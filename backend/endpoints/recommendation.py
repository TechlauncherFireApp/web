# Flask
from flask import Flask
from flask_restful import reqparse, abort, Resource, fields, marshal_with, inputs
# Gurobi
import gurobipy as gp
from gurobi.DataGenerator import NumberGenerator, LoadVolunteers, shiftpopulator
from gurobi.Names import firstNames, lastNames
from gurobi.Scheduler import Schedule
from gurobi.AssetTypes import Request, LightUnit, MediumTanker, HeavyTanker
# Helpers
from endpoints.helpers.input_validation import *

# Define data input
# {
#   asset_list : [{
#     asset_id: Integer,
#     asset_name: String,
#     start_time: TimeBlock,
#     end_time: TimeBlock
#   }]
# }

# Validate an asset request input
def input_asset_req(value, name):
    # Validate that asset_list contains dictionaries
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
    return value

parser = reqparse.RequestParser()
parser.add_argument('asset_list', action='append', type=input_asset_req)

# Define data output
TimeBlock = fields.Integer

position_field = {
    'position_id': fields.Integer,
    'role': fields.String, # driver | advanced | basic
    'qualifications': fields.String,
}

volunteer_field = {
    'volunteer_id': fields.Integer,
    'position_id': fields.Integer(attribute='position'),
    'volunteer_name': fields.String,
    'role': fields.String, # driver | advanced | basic
    'qualifications': fields.List(fields.String),
    'contact_info': fields.List(fields.Nested({
        'type': fields.String, # email | phone
        'detail': fields.String, # email_add | phone_no
    }))
}

recommendation_list_field = {
    'asset_id': fields.Integer,
    'asset_class': fields.String, # Enum
    # 'start_time': TimeBlock,
    # 'end_time': TimeBlock,
    'position': fields.List(fields.Nested(position_field)),
    'volunteers': fields.List(fields.Nested(volunteer_field)),
}

def availability_field():
    list_times = shiftpopulator()
    dict_times = {}
    for time in list_times:
        dict_times[time] = fields.Boolean
    return dict_times

volunteer_list_field = {
    'id': fields.Integer,
    'name': fields.String,
    'role': fields.String(attribute='Explvl'),
    # 'prefHours': fields.Integer,
    # 'phonenumber': fields.Integer,
    'qualifications': fields.List(fields.String, attribute='Qualifications'),
    # 'YearsOfExperience': fields.Integer,
    'contact_info': fields.List(fields.Nested({
        'type': fields.String(default='phone'), # email | phone
        'detail': fields.String, # email_add | phone_no
    })),
    # 'Availability': fields.Nested(availability_field()),
}

resource_fields = {
    'recommendation_list': fields.List(fields.Nested(recommendation_list_field)),
    'volunteer_list': fields.List(fields.Nested(volunteer_list_field)),
}


# Format the position data
def formatPosition(position, role, qualifications):
    return {
        'position_id': position,
        'role': role,
        'qualifications': qualifications,
    }


# Handle the Recommendation endpoint
class Recommendation(Resource):
    def __init__(self, **kwargs):
        # smart_engine is a black box dependency
        self.volunteer_list = kwargs['volunteer_list']

    @marshal_with(resource_fields)
    def post(self):
        args = parser.parse_args()
        # if args["asset_list"] is None:
        #     return
        print(args)

        asset_requests = []
        for asset_request in args["asset_list"]:
            asset_id = asset_request["asset_id"]
            asset_name = asset_request["asset_name"]
            start_time = asset_request["start_time"]
            end_time = asset_request["end_time"]
            # Select the asset
            # This could probably be done better
            if asset_name == "Heavy Tanker":
                asset_type = HeavyTanker
            elif asset_name == "Medium Unit":
                asset_type = MediumTanker
            elif asset_name == "Light Unit":
                asset_type = LightUnit
            asset_requests.append(Request(asset_id,asset_type, start_time, end_time))

        try:
            recommendation_list, volunteer_list_out = Schedule(self.volunteer_list, asset_requests)
            print("succeeded to optimise")


            # Fix the contact details output
            for volunteer in volunteer_list_out:
                volunteer.contact_info = {
                    "type":"phone",
                    "detail": volunteer.phonenumber,
                }

            return {
                "recommendation_list" : recommendation_list,
                "volunteer_list" : volunteer_list_out
            }
        except gp.GurobiError as e:
            print('Error code ' + str(e.errno) + ': ' + str(e))
            print("Failed to optimise")