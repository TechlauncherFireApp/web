from flask import Flask
from flask_restful import reqparse, abort, Resource, fields, marshal_with
import uuid

from includes.main import contains, error_message
from includes.connection_mysqli import get as connection, is_connected, cur_conn_close

'''
Define Data Input

{
    "title": String
}
'''

parser = reqparse.RequestParser()
parser.add_argument('title', action='store', type=str)

'''
Define Data Output

{
    "id": String
}
'''

resource_fields = {
    "id": fields.String
}

# Make a New Request inside the DataBase
class NewAssetRequest(Resource):
    @marshal_with(resource_fields)
    def post(self):
        args = parser.parse_args()
        if args["title"] is None:
            return
        
        title = args["title"]
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
            except Exception as e:
                conn.rollback()                     # RollBack
                cur_conn_close(cur, conn)
                raise Exception(e)
        raise Exception("0x01")                     # Fail Message