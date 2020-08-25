# Flask
from flask import Flask
from flask_restful import reqparse, abort, Resource, fields, marshal_with, inputs
import re, json

from includes.main import contains, error_message
from includes.connection_mysqli import get as connection, is_connected, cur_conn_close, conn_close

from datetime import *
from math import floor

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
        "availabilities": [[DateTimeString, DateTimeString]]
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
    'availabilities': fields.List(fields.List(fields.DateTime(dt_format='rfc822')))
}

resource_fields = {
    'results': fields.List(fields.Nested(volunteer_list_field)),
}

# Convert weekday string to representative number
def weekdayStringToInt(weekdayString):
    switcher = {
        'Monday':0,
        'Tuesday':1,
        'Wednesday':2,
        'Thursday':3,
        'Friday':4,
        'Saturday':5,
        'Sunday':6
    }
    return switcher[weekdayString]

# Convert database availabilities to DateTime
def availabilitiesToDateTime(availabilities):
    new_availabilities = []
    now = datetime.now()

    for day in availabilities:
        if len(availabilities[day]) == 0: continue

        # Compare stored day to current day
        weekday = weekdayStringToInt(day)
        days_to_add = weekday - now.weekday()
        if days_to_add < 0:
            days_to_add = 7 + days_to_add
        # Calculate year, month, day
        new_availability_day = now + timedelta(days = days_to_add)

        for availability in availabilities[day]:
            # Calculate hour and minutes
            start_hour = floor(availability[0])
            end_hour = floor(availability[1])
            start_minute = int(60 * (availability[0] - start_hour))
            # hour=24 is invalid
            if end_hour == 24:
                end_hour = 23
                end_minute = 30
            else:
                end_minute = int(60 * (availability[0] - start_hour))
            # Format in DataTime
            start_availability = datetime(new_availability_day.year, new_availability_day.month, new_availability_day.day, start_hour, start_minute, 0)
            end_availability = datetime(new_availability_day.year, new_availability_day.month, new_availability_day.day, end_hour, end_minute, 0)

            # Add availability to output
            new_availability = [start_availability, end_availability]
            new_availabilities.append(new_availability)
    return new_availabilities            





# Handle the Recommendation endpoint
class VolunteerAll(Resource):
    @marshal_with(resource_fields)
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
                        x["availabilities"] = availabilitiesToDateTime(json.loads(x["availabilities"]))
                    except: print("Error")
                cur_conn_close(cur, conn)
                return { "results": res }                                       # Output
            # except Exception as e: return str(e)
            except:
                cur_conn_close(cur, conn)
                return { "results": error_message("0x01") }                     # Fail Message
        
        conn_close(conn)
        return { "results": error_message("0x02") }                             # Fail Message