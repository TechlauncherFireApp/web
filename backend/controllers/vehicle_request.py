from flask import Blueprint
from flask_restful import reqparse, Resource, fields, marshal_with, Api

from .utility import *
from domain import session_scope
from repository.asset_request_vehicle_repository import *

from services.optimiser.input_processing import *


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
delete_parser.add_argument('vehicleId', action='store', type=str)


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
        args = delete_parser.parse_args()
        with session_scope() as session:
            result = delete_vehicle(session, args["requestId"], args["vehicleId"])
            return {"success": result}


vehicle_request_bp = Blueprint('vehicle_request', __name__)
api = Api(vehicle_request_bp)
api.add_resource(VehicleRequest, '/vehicle/request')

a_fields = {
    "number": fields.Integer
}


class GetInputA(Resource):
    @marshal_with(a_fields)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('requestID', type=int, required=True)
        request_id = parser.parse_args()["requestID"]
        with session_scope() as session:
            result_A = get_input_A(session, request_id)
            return {"number": result_A}


r_fields = {"number": fields.Integer}


class GetInputR(Resource):
    @marshal_with(r_fields)
    def get(self):
        with session_scope() as session:
            result_R = get_input_R(session)
            return {"number": result_R}


p_fields = {"number": fields.Integer}


class GetInputP(Resource):
    @marshal_with(p_fields)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('requestID', type=int, required=True)
        request_id = parser.parse_args()["requestID"]

        with session_scope() as session:
            result_P = get_input_P(session, request_id)
            return {"number": result_P}


v_fields = {"number": fields.Integer}


class GetInputV(Resource):
    @marshal_with(v_fields)
    def get(self):
        with session_scope() as session:
            result_V = get_input_V(session)
            return {"number": result_V}


q_fields = {"number": fields.Integer}


class GetInputQ(Resource):
    @marshal_with(q_fields)
    def get(self):
        with session_scope() as session:
            result_Q = get_input_Q(session)
            return {"number": result_Q}


vehicle_fields = {
    "number": fields.Integer
}


class GetVehicleRequest(Resource):
    @marshal_with(vehicle_fields)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('requestID', type=int, required=True)
        request_id = parser.parse_args()["requestID"]
        with session_scope() as session:
            result_vehicle = test_vehicle_list(session, request_id)
            return {"number": result_vehicle}


processing_api = Api(vehicle_request_bp, '/processing')
processing_api.add_resource(GetInputA, '/getInputA')
processing_api.add_resource(GetInputR, '/getInputR')
processing_api.add_resource(GetInputP, '/getInputP')
processing_api.add_resource(GetInputV, '/getInputV')
processing_api.add_resource(GetInputQ, '/getInputQ')
processing_api.add_resource(GetVehicleRequest, '/getVehicleRequest')
