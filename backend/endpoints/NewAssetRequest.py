from flask import Flask
from flask_restful import reqparse, abort, Resource
import uuid

from includes.main import contains, message_return
from includes.connection_mysqli import get as connection, is_connected, cur_conn_close

class NewAssetRequest(Resource):
    def get(self):
        idAdmin = "jkEM0NW1QsTOqhH"
        
        conn = connection()
        if is_connected(conn):
            id = uuid.uuid4().hex[0:15]             # Make New Request ID
            conn.start_transaction()                # Transaction type
            cur = conn.cursor()
            try:
                cur.execute("INSERT INTO `asset-request`(`id`,`idAdmin`) VALUES (%s,%s);", [id, idAdmin])
                conn.commit()                       # Commit
                cur_conn_close(cur, conn)
                return { "status": 1, "id": id }    # Success Message
            except:
                conn.rollback()                     # RollBack
                cur_conn_close(cur, conn)
        return message_return()                     # Fail Message