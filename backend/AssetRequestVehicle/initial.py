from flask import Flask
from flask_restful import reqparse, abort, Resource
import re

from includes.main import contains, error_message
from includes.connection_mysqli import get as connection, is_connected, cur_conn_close

class Initial(Resource):
    def get(id):
        # Check ID
        if not contains(id): return error_message("0x01")
        id = str(id)

        conn = connection()
        if is_connected(conn):
            cur = conn.cursor(prepared=True)
            try:
                q = """
                    SELECT DISTINCT
                        arv.`id`, arv.`idVehicle`, v.`type`, arv.`from` AS `startDateTime`, arv.`to` AS `endDateTime`
                    FROM
                        `asset-request_vehicle` AS arv JOIN `vehicle` AS v ON arv.`idVehicle` = v.`id`
                    WHERE
                        arv.`idRequest`=%s;"""

                cur.execute(re.sub("\s\s+", " ", q), [id])
                res = [dict(zip(cur.column_names, r)) for r in cur.fetchall()]          # Get all the vehicles inside a request
                for x in res:
                    x["startDateTime"] = str(x["startDateTime"])
                    x["endDateTime"] = str(x["endDateTime"])
                return res
            # except Exception as e: return str(e)
            except:
                cur_conn_close(cur, conn)
                return error_message("0x02")                    # Fail Message

        cur_conn_close(cur, conn)
        return error_message("0x03")                            # Fail Message