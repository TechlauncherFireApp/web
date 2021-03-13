# Mysql
from includes.query_mysql import query_mysql
# Misc
from datetime import *
from pytz import UTC
import re, json
from math import floor

from includes.main import contains
from includes.connection_mysqli import get as connection, is_connected, cur_conn_close

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
def availabilitiesToDateTime(availabilities, set_offset_aware):
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
        availability_start = now + timedelta(days = days_to_add)

        for availability in availabilities[day]:
            # Calculate hour and minutes
            start_hour = floor(availability[0])
            end_hour = floor(availability[1])
            start_minute = int(60 * (availability[0] - start_hour))
            end_minute =   int(60 * (availability[1] - end_hour))

            # hour=24 is invalid
            if start_hour == 24:
                availability_start = availability_start + timedelta(days = 1)
                start_hour = 0
            if end_hour == 24:
                availability_end = availability_start + timedelta(days = 1)
                end_hour = 0
            else:
                availability_end = availability_start
            
            # Format in DataTime
            start_availability = datetime(availability_start.year, availability_start.month, availability_start.day, start_hour, start_minute, 0)
            end_availability   = datetime(availability_end.year  , availability_end.month  , availability_end.day  , end_hour  , end_minute  , 0)
            
            # Force availability to be offset-aware
            if set_offset_aware:
                start_availability = start_availability.replace(tzinfo=UTC)
                end_availability   = end_availability.replace(tzinfo=UTC)

            # Add availability to output
            new_availability = [start_availability, end_availability]
            new_availabilities.append(new_availability)
    return new_availabilities


# Get all of the volunteers and their info from the database
def volunteer_all(set_offset_aware):
    # Make query
    query = """
            SELECT
                `id` AS `ID`,`firstName`,`lastName`,`email`,`mobileNo`,`prefHours`,`expYears`,`possibleRoles`,`qualifications`,`availabilities`
            FROM
                `volunteer`;"""

    try:
        res = query_mysql(query)
    except Exception as e:
        print(e)
        return []

    # Edit retrived data
    for x in res:
        try:
            x["possibleRoles"] = json.loads(x["possibleRoles"])
            x["qualifications"] = json.loads(x["qualifications"])
            x["availabilities"] = availabilitiesToDateTime(json.loads(x["availabilities"]), set_offset_aware)
        except Exception as e:
            print("Error: {}".format(e))

    return res


# Get all of the volunteers and their info from the database
def volunteer(set_offset_aware, volunteerID):
    # Make query
    conn = connection()
    if is_connected(conn):
        cur = conn.cursor(prepared=True)
        try:
            query = """
                SELECT
                    `firstName`,`lastName`,`email`,`mobileNo`,`prefHours`,`expYears`,`possibleRoles`,`qualifications`,`availabilities`
                FROM
                    `volunteer`
                WHERE
                    `id`=%s;"""
            cur.execute(query, [volunteerID])
            res = cur.fetchone()
            res = dict(zip(cur.column_names, (res if contains(res) else [])))
            cur_conn_close(cur, conn)

            try:
                res["possibleRoles"] = json.loads(res["possibleRoles"])
                res["qualifications"] = json.loads(res["qualifications"])
                res["availabilities"] = availabilitiesToDateTime(json.loads(res["availabilities"]), set_offset_aware)
            except Exception as e:
                print("Error: {}".format(e))

            return res

        except Exception as e:
            cur_conn_close(cur, conn)
            print (str(e))