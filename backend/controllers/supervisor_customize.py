'''
from flask import Blueprint
from flask_restful import reqparse, Resource, fields, marshal_with, Api

from domain import session_scope
from repository.request_repository import *

parser = reqparse.RequestParser()
parser.add_argument('requestId', action='store', type=int)
parser.add_argument('status', action='store', type=str)

delete_parser = reqparse.RequestParser()
delete_parser.add_argument('requestId', action='store', type=str)

s_request_fields = {
    "id": fields.Integer,
    "title": fields.String,
    "status": fields.String,
    "last_update_time": fields.DateTime
}

get_resource_list = {
    "success": fields.Boolean,
    "results": fields.List(fields.Nested(s_request_fields))
}


class SrExistingRequests(Resource):
    @marshal_with(get_resource_list)
    def get(self):
        with session_scope() as session:
            res = get_existing_requests(session)
            return {"success": True, "Results": res}


supervisor_customize_bp = Blueprint('supervisor_customize', __name__)
api = Api(supervisor_customize_bp, '/supervisor')
api.add_resource(SrExistingRequests, '/requestList')



from flask import Blueprint
from flask_restful import reqparse, Resource, fields, marshal_with, Api

from domain import session_scope
from repository.request_repository import *


Define Data Input

PATCH
{
    "requestId": Int
    "status": String
}

DELETE
{
    "requestId": String
}


parser = reqparse.RequestParser()
parser.add_argument('requestId', action='store', type=int)
parser.add_argument('status', action='store', type=str)

delete_parser = reqparse.RequestParser()
delete_parser.add_argument('requestId', action='store', type=str)




get_resource_obj = {
    "id": fields.String,
    "title": fields.String,
    "status": fields.String
}

get_resource_list = {
    "success": fields.Boolean,
    "results": fields.List(fields.Nested(get_resource_obj))
}


# Handle the Recommendation endpoint
class SrExistingRequests(Resource):
    @marshal_with(get_resource_list)
    def get(self):
        with session_scope() as session:
            res = get_existing_requests(session)
            return {"success": True, "results": res}


supervisor_customize_bp = Blueprint('supervisor_customize', __name__)
api = Api(supervisor_customize_bp)
api.add_resource(SrExistingRequests, '/supervisor')

'''