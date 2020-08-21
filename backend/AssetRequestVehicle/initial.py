from flask import Flask
from flask_restful import reqparse, abort, Resource
import uuid

from includes.main import contains, message_return
from includes.connection_mysqli import get as connection, is_connected, cur_conn_close

class Initial(Resource):
    def get(id):

        # conn = connection()
        # if is_connected(conn):
        #     cur = conn.cursor(prepared=True)
        #     try:
        #         cur.execute("SELET `id`,`idVehicle`,`from`,`to` FROM `asset-request_vehicle` WHERE `idRequest`=%s;", [id])

        return message_return(id)                     # Fail Message