from flask import Blueprint
from flask_restful import reqparse, Resource, fields, marshal_with, Api
from .utility import *

'''
Define Data Input

GET
{
    idVolunteer: String
    idVehicle: String
}

PATCH
{
    idVolunteer: String
    idVehicle: String
    Status: String 
}

'''

parser = reqparse.RequestParser()
parser.add_argument('idVolunteer', action='store', type=str)  # unsure about this line
parser.add_argument('idVehicle', action='store', type=str)
parser.add_argument('status', action='store', type=str)

'''
Define Data Output

GET
{
    status: String
}

PATCH
{
    success: boolean
}

'''

get_resource_fields = {
    'status': fields.String,
    'success': fields.Boolean
}

patch_resource_fields = {
    'success': fields.Boolean
}


class VolunteerStatus(Resource):

    @marshal_with(get_resource_fields)
    def get(self):
        args = parser.parse_args()
        if (args["idVolunteer"] is None or args["idVehicle"] is None):
            return {"status": None, "success": False}
        idVolunteer = args['idVolunteer']
        idVehicle = args['idVehicle']
        conn = connection()
        if is_connected(conn):
            cur = conn.cursor(prepared=True)
            try:
                cur.execute("SELECT `status` FROM `asset-request_volunteer` WHERE `idVolunteer`=%s AND `idVehicle`=%s;",
                            [idVolunteer, idVehicle])
                res = cur.fetchone()
                res = dict(zip(cur.column_names, (res if contains(res) else [])))
                if contains(res):
                    cur_conn_close(cur, conn)
                    return {"success": True, "status": (res["status"])}
                cur_conn_close(cur, conn)
            except Exception as e:
                cur_conn_close(cur, conn)
                print(str(e))
        return {"success": False, "status": None}

    @marshal_with(patch_resource_fields)
    def patch(self):

        args = parser.parse_args()
        if (args["idVolunteer"] is None or args["idVehicle"] is None or args["status"] is None):
            return {"success": False}

        idVolunteer = args['idVolunteer']
        idVehicle = args['idVehicle']
        status = args['status']

        if status not in ["confirmed", "rejected"]: return {"success": False}

        conn = connection()
        if is_connected(conn):
            conn.start_transaction()  # Transaction type
            cur = conn.cursor(prepared=True)
            try:
                cur.execute(
                    "UPDATE `asset-request_volunteer` SET `status`=%s WHERE `idVolunteer`=%s AND `idVehicle`=%s;",
                    [status, idVolunteer, idVehicle])
                conn.commit()  # Commit
                cur_conn_close(cur, conn)
                return {"success": True}
            except Exception as e:
                conn.rollback()  # RollBack
                cur_conn_close(cur, conn)
                print(str(e))

        return {"success": False}


volunteer_status_bp = Blueprint('volunteer_status', __name__)
api = Api(volunteer_status_bp)
api.add_resource(VolunteerStatus, '/volunteer/status')
