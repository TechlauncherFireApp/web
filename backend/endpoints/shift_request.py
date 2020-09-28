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
        value = input_key_type(value, 'role', type_list_of, [type_enum, [["basic", "advanced", "crewLeader", "driver"]]])
    return value

# Validate a shift input
def input_shift(value, name):
    # Validate that shifts contains dictionaries
    value = type_dict(value)
    if type(value) is dict:
        # Validate shift values
        value = input_key_type(value, 'shiftID', type_string, [])
        # Validate the list of volunteers
        value = input_key_type(value, 'volunteers', type_list_of, [input_volunteer_position, []])
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
    "role": fields.List(fields.String),
    "status": fields.String,
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
        
        return self.get_func(args["requestID"])
    
    # @marshal_with(get_resource_fields)
    def get_func(self, requestID):
        #TODO Get a shift request from it's requestID

        conn = connection()
        if is_connected(conn):
            cur = conn.cursor(prepared=True)
            try:
                o = []
                q = """
                    SELECT DISTINCT
                        arv.`id` AS `shiftID`, v.`type` AS `assetClass`, arv.`from` AS `startTime`, arv.`to` AS `endTime`,
                        arp.`idVolunteer` AS `ID`, arp.`position` AS `positionID`, arp.`roles` AS `role`, arp.`status` AS `status`
                    FROM
                        `asset-request_volunteer` AS arp
                        INNER JOIN `asset-request_vehicle` AS arv ON arp.`idVehicle` = arv.`id`
                        INNER JOIN `vehicle` AS v ON v.`id` = arv.`idVehicle`
                    WHERE
                        arv.`idRequest` = %s;"""
                cur.execute(re.sub("\s\s+", " ", q), [requestID])
                res = [dict(zip(cur.column_names, r)) for r in cur.fetchall()]      # Get all the vehicles inside a request
                for y in res:

                    # start - untested
                    if y["ID"] == None: y["ID"] = "-1"
                    # end - untested 
                    n = True
                    for i, x in enumerate(o):
                        if x["shiftID"] == y["shiftID"]:
                            o[i]["volunteers"].append({ "ID": y["ID"], "positionID": y["positionID"], "role": json.loads(y["role"]), "status": y["status"] })
                            n = False
                            break
                    if n: o.append({ "shiftID": y["shiftID"], "assetClass": y["assetClass"], "startTime": y["startTime"], "endTime": y["endTime"], "volunteers": [{ "ID": y["ID"], "positionID": y["positionID"], "role": json.loads(y["role"]), "status": y["status"] }] })

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
                if v["ID"] == "-1": v["ID"] = None
                d.append([v["ID"], s["shiftID"], int(v["positionID"]), json.dumps(v["role"])])

        print("data to save:", d)

        conn = connection()
        if is_connected(conn) and contains(d):
            conn.start_transaction()
            cur = conn.cursor(prepared=True)
            try:
                q = ",".join(["(%s,%s,%s,%s)"] * len(d))
                d = np.concatenate(d).tolist()
                cur.execute("INSERT INTO `asset-request_volunteer` (`idVolunteer`,`idVehicle`,`position`,`roles`) VALUES " + q + ";", d)
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
        
        requestID = args["requestID"]
        shifts = args["shifts"]
        cd = self.get_func(requestID)["results"]

        #TODO Update a shift request object in database
        d = []
        if contains(cd) and (type(cd) is list):
            for s in shifts:
                for v in s["volunteers"]:
                    for s2 in cd:
                        for v2 in s2["volunteers"]:
                            if ((s["shiftID"] == s2["shiftID"] and v["positionID"] == v2["positionID"]) and
                                (v["ID"] != v2["ID"] or v["role"] != v2["role"])):
                                if v["ID"] == "-1": v["ID"] = None
                                d.append([v["ID"], json.dumps(v["role"]), s["shiftID"], int(v["positionID"])])
        else:
            return { "success": False }

        # Insert
        conn = connection()
        if contains(d) and is_connected(conn):
            conn.start_transaction()
            cur = conn.cursor(prepared=True)
            try:
                for x in d:
                    cur.execute("UPDATE `asset-request_volunteer` SET `idVolunteer`=%s, `roles`=%s, `status`=DEFAULT WHERE `idVehicle`=%s AND `position`=%s;", x)
                conn.commit()
                cur_conn_close(cur, conn)
                return { "success": True }
            except Exception as e:
                conn.rollback()
                cur_conn_close(cur, conn)
                print (str(e))
                return { "success": False }

# d.append([s["shiftID"], int(v["positionID"]), v["ID"], json.dumps(v["role"])])

# q = ",".join(["(%s,%s,%s,%s)"] * len(d))
# q = re.sub("\s\s+", " ", """
#     INSERT INTO `asset-request_volunteer` (`idVehicle`,`position`,`idVolunteer`,`roles`) VALUES """ + q + """"
#     ON DUPLICATE KEY UPDATE `idVolunteer`=VALUES(`idVolunteer`), `roles`=VALUES(`roles`);
# """)
# d = np.concatenate(d).tolist()
# cur.execute(q, d)