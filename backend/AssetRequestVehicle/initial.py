from flask import Flask
from flask_restful import reqparse, abort, Resource
import re

from includes.main import contains, error_message
from includes.connection_mysqli import get as connection, is_connected, cur_conn_close

class Initial(Resource):
    def get(id):
        if not contains(id): return error_message()
        id = str(id)

        conn = connection()
        if is_connected(conn):
            cur = conn.cursor(prepared=True)

            try:
                q = """
                    SELECT
                        arv.`id`, arv.`idVehicle`, v.`type`, arv.`from` AS `startDateTime`, arv.`to` AS `endDateTime`
                    FROM
                        `asset-request_vehicle` AS arv JOIN `vehicle` AS v ON arv.`idVehicle` = v.`id`
                    WHERE
                        `idRequest`=%s;"""

                cur.execute(re.sub("\s\s+", " ", q), [id])
                res = [dict(zip(cur.column_names, r)) for r in cur.fetchall()]
                for x in res:
                    x["startDateTime"] = str(x["startDateTime"])
                    x["endDateTime"] = str(x["endDateTime"])
                
                return res

            except: None
        cur_conn_close(cur, conn)

        return error_message("end")                     # Fail Message