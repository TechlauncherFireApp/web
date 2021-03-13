from flask import Blueprint
from flask_restful import reqparse, Resource, fields, marshal_with, Api
import datetime, numpy as np


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

        try:
            datetime.datetime.strptime(value["startDateTime"], "%Y-%m-%d %H:%M:%S.%f").date()
        except:
            raise ValueError("startDateTime not in correct format")
        try:
            datetime.datetime.strptime(value["endDateTime"], "%Y-%m-%d %H:%M:%S.%f").date()
        except:
            raise ValueError("endDateTime not in correct format")

        # Validate the startTime is before the endTime
        # if value['startDateTime'] >= value['endDateTime']:
        #     raise ValueError("The startDateTime '{}' cannot be after the endDateTime '{}'".format(value['startDateTime'], value['endDateTime']))
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

        requestID = args["requestID"]

        conn = connection()
        if is_connected(conn):
            cur = conn.cursor(prepared=True)
            try:
                cur.execute(
                    "SELECT COUNT(`idRequest`) AS `count` FROM `asset-request_vehicle` AS arv WHERE arv.`idRequest`=%s;",
                    [requestID])
                res = cur.fetchone()
                res = dict(zip(cur.column_names, (res if contains(res) else [])))
                cur_conn_close(cur, conn)
                return {"success": (res["count"] > 0)}
            except Exception as e:
                cur_conn_close(cur, conn)
                print(str(e))
                return {"success": False}

        conn_close(conn)
        return {"success": False}

    @marshal_with(resource_fields)
    def post(self):
        args = parser.parse_args()
        if args["requestID"] is None or args["vehicles"] is None: return {"success": False}

        requestID = args["requestID"]
        vehicles = args["vehicles"]

        # Query Parameter's Data
        d = []
        for v in vehicles:
            d.append([v["vehicleID"], requestID, v["assetClass"], v["startDateTime"], v["endDateTime"]])

        conn = connection()
        if contains(d) and is_connected(conn):
            conn.start_transaction()
            cur = conn.cursor(prepared=True)
            try:
                # Insert Vehicle of the Request
                q = ",".join(["(%s,%s,%s,%s,%s)"] * len(d))
                d = np.concatenate(d).tolist()
                cur.execute(
                    "INSERT INTO `asset-request_vehicle` (`id`,`idRequest`,`type`,`from`,`to`) VALUES " + q + ";", d)
                conn.commit()
                cur_conn_close(cur, conn)
                return {"success": True}
            except Exception as e:
                conn.rollback()
                cur_close(cur)
                print(str(e))

        conn_close(conn)
        return {"success": False}


vehicle_request_bp = Blueprint('vehicle_request', __name__)
api = Api(vehicle_request_bp)
api.add_resource(VehicleRequest, '/vehicle/request')
