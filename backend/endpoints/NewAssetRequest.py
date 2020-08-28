from flask import Flask
from flask_restful import reqparse, abort, Resource
import uuid

from includes.main import contains, error_message
from includes.connection_mysqli import get as connection, is_connected, cur_conn_close

# Make a New Request inside the DataBase
class NewAssetRequest(Resource):
    def get(title):
        idAdmin = "jkEM0NW1QsTOqhH"                 # Using a single default admin (Brigade Captain)
        
        conn = connection()
        if is_connected(conn):
            id = uuid.uuid4().hex[0:15]             # Make New Request ID
            conn.start_transaction()                # Transaction type
            cur = conn.cursor(prepared=True)
            try:
                cur.execute("INSERT INTO `asset-request`(`id`,`idAdmin`,`title`) VALUES (%s,%s,%s);", [id, idAdmin, title])
                conn.commit()                       # Commit
                cur_conn_close(cur, conn)
                return { "id": id }                 # Success Message
            # except Exception as e: return str(e)
            except:
                conn.rollback()                     # RollBack
                cur_conn_close(cur, conn)
        return error_message("0x01")                # Fail Message