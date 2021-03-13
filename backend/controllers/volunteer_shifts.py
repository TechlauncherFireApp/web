import json
import re

from flask import Blueprint
from flask_restful import reqparse, Resource, fields, marshal_with, Api

'''
Define Data Input
 {
     volunteerID: String
 }

'''

parser = reqparse.RequestParser()
parser.add_argument('volunteerID', action='store', type=str)

'''
Define Data Output

get every: asset-request_volunteer.idVolunteer == volunteerID
need data from four different tables in database
{
    "results" : [{
        "requestTitle":     String      (asset-request.title)
        "vehicleID":        String      (asset-request_vehicle.id)
        "vehicleType":      String      (vehicle.type)
        "vehicleFrom":      DateTimeString iso8601      (asset-request_vehicle.from)
        "vehicleTo":        DateTimeString iso8601      (asset-request_vehicle.to)
        "volunteerRoles":   [String]    (asset-request_volunteer.roles)
        "volunteerStatus":  String      (asset-request_volunteer.status)
    }]
}
'''

result_list_field = {
    'requestTitle': fields.String,
    'vehicleID': fields.String,
    'vehicleType': fields.String,
    'vehicleFrom': fields.DateTime(dt_format='iso8601'),
    'vehicleTo': fields.DateTime(dt_format='iso8601'),
    'volunteerRoles': fields.List(fields.String),
    'volunteerStatus': fields.String,
}

resource_fields = {
    'results': fields.List(fields.Nested(result_list_field)),
}


# Handle the volunteer/shifts endpoint
class VolunteerShifts(Resource):

    @marshal_with(resource_fields)
    def get(self):
        args = parser.parse_args()
        if args["volunteerID"] is None:
            return {"success": False}
        volunteerID = args["volunteerID"]

        conn = connection()
        if is_connected(conn):
            cur = conn.cursor(prepared=True)
            try:
                q = re.sub("\s\s+", " ", """
                    SELECT DISTINCT
                        ar.`title` AS `requestTitle`,
                        arv.`id` AS `vehicleID`, arv.`type` AS `vehicleType`,
                        arv.`from` AS `vehicleFrom`, arv.`to` AS `vehicleTo`,
                        arp.`roles` AS `volunteerRoles`, arp.`status` AS `volunteerStatus`
                    FROM
                        `asset-request_volunteer` AS arp
                        INNER JOIN `asset-request_vehicle` AS arv ON arp.`idVehicle` = arv.`id`
                        INNER JOIN `asset-request` AS ar ON arv.`idRequest` = ar.`id`
                    WHERE
                        `idVolunteer` = %s;
                """)

                cur.execute(q, [volunteerID])
                res = [dict(zip(cur.column_names, r)) for r in cur.fetchall()]
                o = []
                for r in res:
                    r["volunteerRoles"] = json.loads(r["volunteerRoles"])
                    o.append(r)
                print(o)
                if contains(o):
                    cur_conn_close(cur, conn)
                    return {"success": True, "results": o}
                cur_conn_close(cur, conn)
            except Exception as e:
                cur_conn_close(cur, conn)
                print(str(e))

        return {"success": False}


volunteer_shifts_bp = Blueprint('volunteer_shifts', __name__)
api = Api(volunteer_shifts_bp)
api.add_resource(VolunteerShifts, '/volunteer/shifts')
