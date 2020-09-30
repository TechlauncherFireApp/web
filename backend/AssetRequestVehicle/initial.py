from flask import Flask
from flask_restful import reqparse, abort, Resource
import re

from includes.main import contains, error_message
from includes.connection_mysqli import get as connection, is_connected, cur_conn_close, conn_close

class Initial(Resource):
    def get(id):
        # Check ID
        if not contains(id): return error_message("0x01")
        id = str(id)

        conn = connection()
        if is_connected(conn):
            cur = conn.cursor(prepared=True)
            try:
                cur.execute("SELECT COUNT(`id`) AS `count` FROM `asset-request_vehicle` WHERE `idRequest`=%s;", [id])
                res = cur.fetchone()
                res = dict(zip(cur.column_names, (res if contains(res) else [])))
                cur_conn_close(cur, conn)
                return (res["count"] > 0)
            # except Exception as e: return str(e)
            except:
                cur_conn_close(cur, conn)
                return error_message("0x02")                    # Fail Message

        conn_close(conn)
        return error_message("0x03")                            # Fail Message