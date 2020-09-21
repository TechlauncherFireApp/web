# Flask
from flask import Flask
from flask_restful import reqparse, abort, Resource, fields, marshal_with, inputs
import re, json
from includes.main import contains
# Mysql
from includes.connection_mysqli import get as connection, is_connected, cur_conn_close

'''
Define Data Input

GET
{
    "volunteerID": String
}

PATCH
{
    "volunteerID": String,
    "prefHours": Integer
}

'''

parser = reqparse.RequestParser()
parser.add_argument('volunteerID', action='store', type=str)
parser.add_argument('prefHours', action='store', type=int)

'''
Define Data Output

GET
{
    "prefHours": Integer
}

PATCH
{
    "success" : Boolean
}
'''

get_resource_fields = {
    'prefHours': fields.Integer,
    'success': fields.Boolean
}

patch_resource_fields = {
    'success': fields.Boolean,
}


# Handle the Recommendation endpoint
class VolunteerPrefhours(Resource):
    @marshal_with(get_resource_fields)
    def get(self):
        args = parser.parse_args()
        if args["volunteerID"] is None:
            return { "success": False }
        id = args["volunteerID"]
        # TODO Get the volunteer's prefHours

        conn = connection()
        if is_connected(conn):
            cur = conn.cursor(prepared=True)
            try:
                cur.execute("SELECT `prefHours` FROM `volunteer` WHERE `id`=%s;", [id])
                res = cur.fetchone()
                res = dict(zip(cur.column_names, (res if contains(res) else [])))
                if contains(res):
                    cur_conn_close(cur, conn)
                    return { "success": True, "prefHours": int(res["prefHours"]) }
                cur_conn_close(cur, conn)
            except Exception as e:
                cur_conn_close(cur, conn)
                print (str(e))

        return { "success": False, "prefHours": None }

    @marshal_with(patch_resource_fields)
    def patch(self):
        args = parser.parse_args()
        if args["volunteerID"] is None or args["prefHours"] is None:
            return { "success": False }
        id = args["volunteerID"]
        prefHours = int(args["prefHours"])
        # TODO Update the volunteer's prefHours

        print ("\n" + str(prefHours) + "\n")

        conn = connection()
        if is_connected(conn):
            conn.start_transaction()                # Transaction type
            cur = conn.cursor(prepared=True)
            try:
                cur.execute("UPDATE `volunteer` SET `prefHours`=%s WHERE `id`=%s;", [prefHours, id])
                conn.commit()                       # Commit
                cur_conn_close(cur, conn)
                return { "success": True }
            except Exception as e:
                conn.rollback()                     # RollBack
                cur_conn_close(cur, conn)
                print (str(e))

        return { "success": False }