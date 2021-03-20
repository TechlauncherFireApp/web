import datetime
import numpy as np

from flask import Blueprint
from flask_restful import reqparse, Resource, fields, marshal_with, Api

from .utility import *
from domain import session_scope
from repository.asset_request_vehicle_repository import *

'''
Define Data Input

GET
{
  "requestID": String
}

POST
{
  "requestID": String,
  "vehicles" : [{
    "vehicleID": String,
    "assetClass": String, [lightUnit | mediumTanker | heavyTanker]
    "startDateTime": DateTimeString iso8601,
    "endDateTime": DateTimeString iso8601
  }]
}

'''


# Validate a shift input
def input_vehicles(value, name):
    # Validate that it is a dictionary
    value = type_dict(value)
    if type(value) is dict:
        # Validate shift values
        value = input_key_type(value, 'vehicleID', type_string, [])
        value = input_key_type(value, 'assetClass', type_enum, [["heavyTanker", "mediumTanker", "lightUnit"]])
        value = input_key_type(value, 'startDateTime', type_string, [])
        value = input_key_type(value, 'endDateTime', type_string, [])
    return value


parser = reqparse.RequestParser()
parser.add_argument('requestID', action='store', type=str)
parser.add_argument('vehicles', action='append', type=input_vehicles)

'''
Define Data Output

GET
{
  "success": Boolean
}

POST
{
  "success": Boolean
}

'''

resource_fields = {
    "success": fields.Boolean
}


# Make a New Request inside the DataBase
class VehicleRequest(Resource):
    @marshal_with(resource_fields)
    def get(self):
        args = parser.parse_args()

        if args["requestID"] is None: return {"success": False}

        with session_scope() as session:
            return {"success": (count_vehicles(session, args["requestID"]) > 0)}

    @marshal_with(resource_fields)
    def post(self):
        args = parser.parse_args()
        if args["requestID"] is None or args["vehicles"] is None: return {"success": False}

        with session_scope() as session:
            for v in args["vehicles"]:
                new_id = insert_vehicle(session, args["requestID"], v["assetClass"], v["startDateTime"], v["endDateTime"])
                return {"success": True, 'id': new_id}


vehicle_request_bp = Blueprint('vehicle_request', __name__)
api = Api(vehicle_request_bp)
api.add_resource(VehicleRequest, '/vehicle/request')
