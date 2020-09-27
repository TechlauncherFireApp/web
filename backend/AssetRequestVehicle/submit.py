from flask import Flask
from flask_restful import reqparse, abort, Resource
import datetime, numpy as np

from AssetRequestVehicle.initial import Initial as AssetRequestVehicle_initial
from includes.main import contains, error_message
from includes.connection_mysqli import get as connection, is_connected, cur_conn_close


'''
Define Input

{
    "id": String
    "vehicles": [{
        "id": String
        "idVehicle": String 
        "type": String 
        "startDateTime": DateTimeString
        "endDateTime": DateTimeString
    }]
}
'''

class Submit(Resource):
    def get(idRequest, vehicles):
        
        # Check and Validate Data
        if type(vehicles) is not list: return error_message("0x01")
        if not contains(vehicles): return error_message("empty")
        for i in vehicles:
            if not contains(i["type"], i["startDateTime"], i["endDateTime"]): return error_message("0x03")
            i["type"] = str(i["type"])
            try: datetime.datetime.strptime(i["startDateTime"], "%Y-%m-%d %H:%M:%S.%f").date()
            except: return error_message("startDateTime")
            i["startDateTime"] = str(i["startDateTime"])
            try: datetime.datetime.strptime(i["endDateTime"], "%Y-%m-%d %H:%M:%S.%f").date()
            except: return error_message("endDateTime")
            i["endDateTime"] = str(i["endDateTime"])

        # Query Parameter's Data
        d = { "vehicle": [], "ARvehicle": [] }
        for v in vehicles:
            d["vehicle"].append([v["idVehicle"], v["type"]])
            d["ARvehicle"].append([v["id"], v["idVehicle"], idRequest, v["startDateTime"], v["endDateTime"]])

        conn = connection()

        if contains(d["vehicle"]) and is_connected(conn):
            conn.start_transaction()
            cur = conn.cursor(prepared=True)
            try:
                # Make New Vehicle
                q = ",".join(["(%s,%s)"] * len(d["vehicle"]))
                d["vehicle"] = np.concatenate(d["vehicle"]).tolist()
                cur.execute("INSERT INTO `vehicle` (`id`,`type`) VALUES " + q + ";", d["vehicle"])
                # Insert Vehicle of the Request
                q = ",".join(["(%s,%s,%s,%s,%s)"] * len(d["ARvehicle"]))
                d["ARvehicle"] = np.concatenate(d["ARvehicle"]).tolist()
                cur.execute("INSERT INTO `asset-request_vehicle` (`id`,`idVehicle`,`idRequest`,`from`,`to`) VALUES " + q + ";", d["ARvehicle"])
                conn.commit()
                cur_conn_close(cur, conn)
                return "1"
            except Exception as e:
                conn.rollback()
                print (str(e))

        cur_conn_close(cur, conn)
        return error_message("0x07")                    # Success Message