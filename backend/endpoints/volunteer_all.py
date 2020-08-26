# Flask
from flask import Flask
from flask_restful import reqparse, abort, Resource, fields, marshal_with, inputs
import re, json

from includes.main import contains, error_message
from includes.connection_mysqli import get as connection, is_connected, cur_conn_close, conn_close

'''
No Data Input
--
Define Data Output

{
    "results" : [{
        "id": String
        "firstName": String
        "lastName": String
        "email": String
        "mobileNo": String
        "prefHours": Integer
        "expYears": Integer
        "possibleRoles": [String]
        "qualifications": [String]
        "availabilities": [[startDateTime, endDateTime]]
    }]
}
'''

volunteer_list_field = {
    'volunteer_id': fields.String,
    'firstName': fields.String,
    'lastName': fields.String,
    'email': fields.String,
    'mobileNo': fields.String,
    'prefHours':fields.Integer,
    'expYears': fields.Integer,
    'possibleRoles': fields.List(fields.String),
    'qualifications': fields.List(fields.String),
    'availabilities': fields.List(fields.List(fields.String))
}

resource_fields = {
    'results': fields.List(fields.Nested(volunteer_list_field)),
}

# Handle the Recommendation endpoint
class VolunteerAll(Resource):
    # @marshal_with(resource_fields)
    def get(self):
        #TODO Get all volunteers from mysql

        conn = connection()
        if is_connected(conn):
            cur = conn.cursor()
            try:
                q = """
                    SELECT
                        `id` AS `volunteer_id`,`firstName`,`lastName`,`email`,`mobileNo`,`prefHours`,`expYears`,`possibleRoles`,`qualifications`,`availabilities`
                    FROM
                        `volunteer`;"""

                cur.execute(re.sub("\s\s+", " ", q))
                res = [dict(zip(cur.column_names, r)) for r in cur.fetchall()]          # Get all the vehicles inside a request
                # Edit retrived data
                for x in res:
                    try:
                        x["possibleRoles"] = json.loads(x["possibleRoles"])
                        x["qualifications"] = json.loads(x["qualifications"])
                        x["availabilities"] = json.loads(x["availabilities"])
                    except: res.remove(x)
                cur_conn_close(cur, conn)
                return { "results": res }                                       # Output
            # except Exception as e: return str(e)
            except:
                cur_conn_close(cur, conn)
                return { "results": error_message("0x01") }                     # Fail Message
        
        conn_close(conn)
        return { "results": error_message("0x02") }                             # Fail Message