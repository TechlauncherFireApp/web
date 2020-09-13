# Flask
from flask import Flask
from flask_restful import reqparse, abort, Resource, fields, marshal_with, inputs
import re, json
# Helpers
from endpoints.helpers.input_validation import *
from includes.main import contains
# Mysql
from includes.connection_mysqli import get as connection, is_connected, cur_conn_close

'''
Define Data Input

type DayString = "Monday"|"Tuesday"|"Wednesday"|"Thursday"|"Friday"|"Saturday"|"Sunday"
type DecimalPair = [Decimal, Decimal]

GET
{
    "volunteerID": String
}

PATCH
{
    "volunteerID": String,
    "availability": {
        type DayString : [type DecimalPair]
    }
}

'''
def input_pair_list(pair, key):
    # Validate that the list is of length 2 (pairs)
    pair = type_list_of_length(pair, 2)
    # Validate the pairs of the list
    pair[0] = type_fixed(pair[0], 1)
    pair[1] = type_fixed(pair[1], 1)
    return pair

# Validate an avaiability input
def input_availability(value, name):
    # Validate that availability contains dictionaries
    value = type_dict(value)
    if type(value) is dict:
        for key in value.keys():
            # Validate that the key is correct
            key = type_enum(key, ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"])
            # Validate that the value is correct
            value = input_key_type(value, key, type_list_of, [input_pair_list, [key]])
    return value

parser = reqparse.RequestParser()
parser.add_argument('volunteerID', action='store', type=str)
parser.add_argument('availability', action='store', type=input_availability)

'''
Define Data Output

type DayString = "Monday"|"Tuesday"|"Wednesday"|"Thursday"|"Friday"|"Saturday"|"Sunday"
type DecimalPair = [Decimal, Decimal]

GET
{
    "availability": {
        type DayString : [type DecimalPair]
    }
}

PATCH
{
    "success" : Boolean
}
'''

def generate_availability_field():
    days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    output = {}
    for day in days:
        output[day] = fields.List(fields.List(fields.Float()))
    return output

get_resource_fields = {
    'availability': fields.Nested(generate_availability_field()),
    'success': fields.Boolean,
}

patch_resource_fields = {
    'success': fields.Boolean,
}


# Handle the Recommendation endpoint
class VolunteerAvailability(Resource):
    @marshal_with(get_resource_fields)
    def get(self):
        args = parser.parse_args()
        if args["volunteerID"] is None:
            return { "success": False }
        id = args["volunteerID"]
        # TODO get the volunteers availability

        conn = connection()
        if is_connected(conn):
            cur = conn.cursor(prepared=True)
            try:
                cur.execute("SELECT `availabilities` FROM `volunteer` WHERE `id`=%s;", [id])
                res = cur.fetchone()
                res = dict(zip(cur.column_names, (res if contains(res) else [])))
                if contains(res):
                    cur_conn_close(cur, conn)
                    return { "success": True, "availability": json.loads(res["availabilities"]) }
                cur_conn_close(cur, conn)
            except Exception as e:
                cur_conn_close(cur, conn)
                print (str(e))

        return { "success": False, "availability": None }

    @marshal_with(patch_resource_fields)
    def patch(self):
        args = parser.parse_args()
        if args["volunteerID"] is None or args["availability"] is None:
            return { "success": False }

        av = None
        try: av = json.dumps(args["availability"])
        except: return { "success": False }
        id = args["volunteerID"]

        # TODO Update the volunteers availability
        # Tom - I imagine this being like, remove the old availability and push the new availability

        conn = connection()
        if is_connected(conn):
            conn.start_transaction()                # Transaction type
            cur = conn.cursor(prepared=True)
            try:
                cur.execute("UPDATE `volunteer` SET `availabilities`=%s WHERE `id`=%s;", [av, id])
                # print("\n\n")
                # print(args)
                # print("\n\n")
                conn.commit()                       # Commit
                cur_conn_close(cur, conn)
                return { "success": True }
            except Exception as e:
                conn.rollback()                     # RollBack
                cur_conn_close(cur, conn)
                print (str(e))

        return { "success": False }