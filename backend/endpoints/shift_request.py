# Flask
from flask import Flask
from flask_restful import reqparse, abort, Resource, fields, marshal_with, inputs
import re, json, numpy as np
# Helpers
from includes.main import contains
from endpoints.helpers.input_validation import *
# Mysql
from includes.connection_mysqli import get as connection, is_connected, cur_conn_close
from querys.volunteer import volunteer_all

'''
Define Data Input

GET
{
    "requestID": String
}

POST
{
    "shifts": [{
        "shiftID": String,
        "volunteers": [{
            "ID": String,
            "positionID": Integer,
            "roles": [String], [basic | advanced | crewLeader | driver]
        }]
    }]
}

PATCH
{
    "shifts": [{
        "shiftID": String,
        "volunteers": [{
            "ID": String,
            "positionID": Integer,
            "roles": [String], [basic | advanced | crewLeader | driver]
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

# Validate a shift input
def input_shift(value, name):
    # Validate that shifts contains dictionaries
    value = type_dict(value)
    if type(value) is dict:
        # Validate shift values
        value = input_key_type(value, 'shiftID', type_string, [])
        # Validate the list of volunteers
        value = input_key_type(value, 'volunteers', type_list_of, ['volunteer(s)',
                                                    input_volunteer_position, []])
    return value

parser = reqparse.RequestParser()
# Define search criteria
parser.add_argument('requestID', action='store', type=str)
parser.add_argument('shifts', action='append', type=input_shift)

'''
Define data output

GET
{
    "results" : [{
        "shiftID": String,
        "assetClass": String, [lightUnit | mediumTanker | heavyTanker]
        "startTime": DateTimeString iso8601,
        "endTime": DateTimeString iso8601,
        "volunteers": [{
            "ID": String,
            "positionID": Integer,
            "roles": [String], [basic | advanced | crewLeader | driver]
        }]
    }]
}

POST
{
    "success" : Boolean
}

PATCH
{
    "success" : Boolean
}
'''

shift_volunteers_list_field = {
    "ID": fields.String,
    "positionID": fields.Integer,
    "roles": fields.List(fields.String)
}

shift_list_field = {
    "shiftID": fields.String,
    "assetClass": fields.String,
    "startTime": fields.DateTime(dt_format='iso8601'),
    "endTime": fields.DateTime(dt_format='iso8601'),
    "volunteers": fields.List(fields.Nested(shift_volunteers_list_field)),
}

get_resource_fields = {
    'results': fields.List(fields.Nested(shift_list_field)),
}

post_patch_resource_fields = {
    "success" : fields.Boolean
}

# Handle the ShiftRequest endpoint
class ShiftRequest(Resource):
    @marshal_with(get_resource_fields)
    def get(self):
        args = parser.parse_args()
        if args["requestID"] is None:
            return { "results": None }
        
        requestID = args["requestID"]
        #TODO Get a shift request from it's requestID

        conn = connection()
        if is_connected(conn):
            cur = conn.cursor(prepared=True)
            try:
                o = []
                q = """
                    SELECT DISTINCT
                        arv.`id` AS `shiftID`, v.`type` AS `assetClass`, arv.`from` AS `startTime`, arv.`to` AS `endTime`,
                        arp.`idVolunteer` AS `ID`, arp.`position` AS `positionID`, arp.`roles` AS `roles`
                    FROM
                        `asset-request_volunteer` AS arp
                        INNER JOIN `asset-request_vehicle` AS arv ON arp.`idVehicle` = arv.`id`
                        INNER JOIN `vehicle` AS v ON v.`id` = arv.`idVehicle`
                    WHERE
                        arv.`idRequest` = %s;"""
                cur.execute(re.sub("\s\s+", " ", q), [requestID])
                res = [dict(zip(cur.column_names, r)) for r in cur.fetchall()]      # Get all the vehicles inside a request
                for y in res:
                    n = True
                    for i, x in o:
                        if x["shiftID"] == y["shiftID"]:
                            o[i]["volunteers"].append({ "ID": y["ID"], "positionID": y["positionID"], "roles": json.loads(y["roles"]) })
                            n = False
                            break
                    if n: o.append({ "shiftID": y["shiftID"], "assetClass": y["assetClass"], "startTime": y["startTime"], "endTime": y["endTime"], "volunteers": [{ "ID": y["ID"], "positionID": y["positionID"], "roles": json.loads(y["roles"]) }] })

                cur_conn_close(cur, conn)
                return { "results": o }
            except Exception as e:
                cur_conn_close(cur, conn)
                print("Error: {}".format(e))

        return { "results": None }
    
    @marshal_with(post_patch_resource_fields)
    def post(self):
        args = parser.parse_args()
        if args["shifts"] is None:
            return { "success": False }
        
        shifts = args["shifts"]
        #TODO Create a new shift request object in database
        d = []
        for s in shifts:
            for v in s["volunteers"]:
                d.append([v["ID"], s["shiftID"], int(v["positionID"]), json.dumps(v["role"])])

        conn = connection()
        if is_connected(conn) and contains(d):
            conn.start_transaction()
            cur = conn.cursor(prepared=True)
            try:
                q = ",".join(["(%s,%s,%s,%s)"] * len(d))
                d = np.concatenate(d).tolist()
                cur.execute("INSERt INTO `asset-request_volunteer` (`idVolunteer`,`idVehicle`,`position`,`roles`) VALUES " + q + ";", d)
                conn.commit()
                cur_conn_close(cur, conn)
                return { "success": True }
            except Exception as e:
                conn.rollback()
                cur_conn_close(cur, conn)
                print("Error: {}".format(e))

        return { "success": False }

    @marshal_with(post_patch_resource_fields)
    def patch(self):
        args = parser.parse_args()
        if args["requestID"] is None or args["shifts"] is None:
            return { "success": False }
        
        shifts = args["shifts"]
        #TODO Update a shift request object in database


        return { "success": False }