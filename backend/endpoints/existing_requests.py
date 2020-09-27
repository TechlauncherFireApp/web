# Flask
from flask import Flask
from flask_restful import reqparse, abort, Resource, fields, marshal_with, inputs
import re, json
from includes.main import contains
# Mysql
from includes.connection_mysqli import get as connection, is_connected, cur_conn_close

'''
Define Data Input

None

'''

parser = reqparse.RequestParser()

'''
Define Data Output

GET
{
    "id": String,
    "title": String
}

'''

get_resource_obj = {
    "id": fields.String,
    "title": fields.String
}

get_resource_list = {
    "success": fields.Boolean,
    "results": fields.List(fields.Nested(get_resource_obj))
}


# Handle the Recommendation endpoint
class ExistingRequests(Resource):
    @marshal_with(get_resource_list)
    def get(self):
        idAdmin = "jkEM0NW1QsTOqhH"                 # Using a single default admin (Brigade Captain)
        # TODO Get the volunteer's prefHours

        conn = connection()
        if is_connected(conn):
            cur = conn.cursor()
            try:
                cur.execute("SELECT `id`,`title` FROM `asset-request` WHERE `idAdmin`=%s;", [idAdmin])
                res = [dict(zip(cur.column_names, r)) for r in cur.fetchall()]
                if contains(res):
                    cur_conn_close(cur, conn)
                    return { "success": True, "results": res }
                cur_conn_close(cur, conn)
            except Exception as e:
                cur_conn_close(cur, conn)
                print (str(e))

        return { "success": False, "results": None }