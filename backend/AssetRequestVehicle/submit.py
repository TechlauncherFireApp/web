from flask import Flask
from flask_restful import reqparse, abort, Resource
import datetime, numpy as np

from AssetRequestVehicle.initial import Initial as AssetRequestVehicle_initial
from includes.main import contains, error_message
from includes.connection_mysqli import get as connection, is_connected, cur_conn_close

# except Exception as e: return error_message(str(e))

class Submit(Resource):
    def get(idRequest, vehicles):
        
        # Check and Validate Data
        if type(vehicles) is not list: return error_message("0x01")
        if not contains(vehicles): return error_message("empty")
        for i in vehicles:
            if not contains(i["type"], i["startDateTime"], i["endDateTime"]): return error_message("0x02")
            i["type"] = str(i["type"])
            try: datetime.datetime.strptime(i["startDateTime"], "%Y-%m-%d %H:%M:%S.%f").date()
            except: return error_message("startDateTime")
            i["startDateTime"] = str(i["startDateTime"])
            try: datetime.datetime.strptime(i["endDateTime"], "%Y-%m-%d %H:%M:%S.%f").date()
            except: return error_message("endDateTime")
            i["endDateTime"] = str(i["endDateTime"])

        # Get Current Data from DataBase
        current = AssetRequestVehicle_initial.get(idRequest)

        d = { "insert": { "vehicle": [], "ARvehicle": [] }, "delete": [] }
        if contains(current) and (type(current) is dict):
            for c in current:
                for v in vehicles:
                    # Insert
                    if c["id"] != v["id"]:
                        d["insert"]["vehicle"].append([v["idVehicle"], v["type"]])
                        d["insert"]["ARvehicle"].append([v["id"], v["idVehicle"], idRequest, v["startDateTime"], v["endDateTime"]])
        else:
            # Insert    
            for v in vehicles:
                d["insert"]["vehicle"].append([v["idVehicle"], v["type"]])
                d["insert"]["ARvehicle"].append([v["id"], v["idVehicle"], idRequest, v["startDateTime"], v["endDateTime"]])

        # Insert
        conn = connection()
        if contains(d["insert"]["vehicle"]) and is_connected(conn):
            conn.start_transaction()
            cur = conn.cursor(prepared=True)
            try:
                q = ",".join(["(%s,%s)"] * len(d["insert"]["vehicle"]))
                d["insert"]["vehicle"] = np.concatenate(d["insert"]["vehicle"]).tolist()
                cur.execute("INSERT INTO `vehicle` (`id`,`type`) VALUES " + q + ";", d["insert"]["vehicle"])
                q = ",".join(["(%s,%s,%s,%s,%s)"] * len(d["insert"]["ARvehicle"]))
                d["insert"]["ARvehicle"] = np.concatenate(d["insert"]["ARvehicle"]).tolist()
                cur.execute("INSERT INTO `asset-request_vehicle` (`id`,`idVehicle`,`idRequest`,`from`,`to`) VALUES " + q + ";", d["insert"]["ARvehicle"])
                conn.commit()
                cur.close()
            except:
                conn.rollback()
                cur_conn_close(cur, conn)
                return error_message("0x03")

        conn.close()
        return "1"                                      # Fail Message