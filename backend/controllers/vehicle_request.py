from flask import Blueprint
from flask_restful import reqparse, Resource, fields, marshal_with, Api

from .utility import *
from domain import session_scope
from repository.asset_request_vehicle_repository import *

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
parser.add_argument('requestId', action='store', type=str)
parser.add_argument('startDate', action='store', type=str)
parser.add_argument('endDate', action='store', type=str)
parser.add_argument('assetType', action='store', type=str)

vehicle_list_field = {
    "ID": fields.Integer,
    "Type": fields.String,
    "From_Time": fields.DateTime,
    "To_Time": fields.DateTime
}

resource_fields = {
    "success": fields.Boolean,
    "id": fields.Integer,
    "results": fields.List(fields.Nested(vehicle_list_field))
}

delete_parser = reqparse.RequestParser()
delete_parser.add_argument('requestId', action='store', type=str)
delete_parser.add_argument('vehicleID', action='store', type=str)

# Make a New Request inside the DataBase
class VehicleRequest(Resource):
    @marshal_with(resource_fields)
    def get(self):
        args = parser.parse_args()

        if args["requestId"] is None:
            return {"success": False}

        with session_scope() as session:
            rtn = []
            for row in get_vehicles(session, args["requestId"]):
                rtn.append(row)
            return {"success": (count_vehicles(session, args["requestId"]) > 0), "results": rtn}

    @marshal_with(resource_fields)
    def post(self):
        args = parser.parse_args()
        with session_scope() as session:
            new_id = insert_vehicle(session, args["requestId"], args["assetType"], args["startDate"], args["endDate"])
            return {"success": True, 'id': new_id}

    @marshal_with(resource_fields)
    def delete(self):
        # TODO: Fix this delete controller so it detects args
        args = delete_parser.parse_args()
        with session_scope() as session:
            result = delete_vehicle(session, args["requestId"], args["vehicleID"])
            return {"success": result}


vehicle_request_bp = Blueprint('vehicle_request', __name__)
api = Api(vehicle_request_bp)
api.add_resource(VehicleRequest, '/vehicle/request')
