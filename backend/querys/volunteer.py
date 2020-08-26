# Mysql
from includes.query_mysql import query_mysql
# Misc
from datetime import *
import re, json
from math import floor

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


# Get all of the volunteers and their info from the database
def volunteer_all():
    # Make query
    query = """
            SELECT
                `id` AS `ID`,`firstName`,`lastName`,`email`,`mobileNo`,`prefHours`,`expYears`,`possibleRoles`,`qualifications`,`availabilities`
            FROM
                `volunteer`;"""
    res = query_mysql(query)

    #TODO handle any error messages

    # Edit retrived data
    for x in res:
        try:
            x["possibleRoles"] = json.loads(x["possibleRoles"])
            x["qualifications"] = json.loads(x["qualifications"])
            x["availabilities"] = availabilitiesToDateTime(json.loads(x["availabilities"]))
        except Exception as e:
            print("Error: {}".format(e))
    return res