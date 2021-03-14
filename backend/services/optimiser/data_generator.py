import random
import json
import datetime


# returns a list populated with the the hours in a week to be scheduled
def shift_populator():
    results = []
    # week number can be added if need be by adding an extra forloop and the code could be very similar to the hours
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    blocks = range(48)
    for i in days:
        for j in blocks:
            # concatenating the day string with the hour to generate the label for an hour that is to be scheduled
            results.append(i + str(j))
    return results


# turns shift strings into time blocks
def day_hour_to_number_converter(day_hour):
    # total_blocks of time per day
    total_blocks = 48
    # Starts from monday
    Timeblock = 0
    if day_hour[0:3] == "Tue":
        Timeblock += 1 * total_blocks
    if day_hour[0:3] == "Wed":
        Timeblock += 2 * total_blocks
    if day_hour[0:3] == "Thu":
        Timeblock += 3 * total_blocks
    if day_hour[0:3] == "Fri":
        Timeblock += 4 * total_blocks
    if day_hour[0:3] == "Sat":
        Timeblock += 5 * total_blocks
    if day_hour[0:3] == "Sun":
        Timeblock += 6 * total_blocks
    Timeblock += int(day_hour[3:5])
    return Timeblock


def number_to_day_hour_converter(number):
    # total_blocks of time per day
    total_blocks = 48
    DayHour = ""
    # Starts from monday
    if number < total_blocks * 1:
        DayHour += "Mon"
    elif number < total_blocks * 2:
        DayHour += "Tue"
    elif number < total_blocks * 3:
        DayHour += "Wed"
    elif number < total_blocks * 4:
        DayHour += "Thu"
    elif number < total_blocks * 5:
        DayHour += "Fri"
    elif number < total_blocks * 6:
        DayHour += "Sat"
    else:
        DayHour += "Sun"
    DayHour += str(number % total_blocks)

    return DayHour


# returns true Percent% of the time
def boolean_generator(percent):
    if percent >= random.randint(1, 100):
        return True
    else:
        return False


def availability_generator():
    availability_dict = {}
    # arbitrary false declaration so the value assigned in the loop stays on
    generated_boolean = False
    for j in shift_populator():
        # i is time block
        i = day_hour_to_number_converter(j)
        # 240 corresponds to 12am on a saturday so i<240 represents weekdays
        if i < 240:
            if i % 48 == 0:
                # at 12 am to 9am on weekdays generates a true 10% of the time for the set of volunteers generated
                generated_boolean = boolean_generator(10)
            if i % 48 == 18:
                # at 9am to 5pm on weekdays generates a true 20% of the time for the set of volunteers
                generated_boolean = boolean_generator(20)
            if i % 48 == 34:
                #  5pm onwards on weekdays generates a true 80% of the time for the set of volunteers
                generated_boolean = boolean_generator(80)
        # weekdays
        else:
            # weekends
            if i % 48 == 0:
                # at 12 am to 9am on weekends generates a true 10% of the time for the set of volunteers generated
                generated_boolean = boolean_generator(10)
            if i % 48 == 18:
                # at 9am onwards on weekends generates a true 80% of the time for the set of volunteers
                generated_boolean = boolean_generator(80)

        # assigns the generated boolean
        # converts to the string format for now
        availability_dict[j] = generated_boolean

    return availability_converter(availability_dict)


def next_monday():
    i = 0
    while (datetime.datetime.today() + datetime.timedelta(days=i)).weekday() != 0:
        i += 1
    return (datetime.datetime.today() + datetime.timedelta(days=i)).replace(hour=0, minute=0, second=0, microsecond=0)


def availability_converter(availability_dict):
    """Takes availabilities in boolean and timeblock representation and changes it to a list of days and starttimes"""

    Days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    # the
    monday_time = next_monday()
    # this is a boolean that tracks the start of a shift in order to convert into a set of tuples
    # with a start and end
    new_shift_check = False
    time_pairs = []
    # this will hold the time pairs
    time_pair_list = list()

    for shift in shift_populator():
        time_block_number = day_hour_to_number_converter(shift)
        # This represents the start of a time pair the case that a person has started being available
        if availability_dict[shift] and not new_shift_check:
            new_shift_check = True
            time_pairs.append(monday_time + datetime.timedelta(hours=(time_block_number % 48) / 2))

        # This represents the end of a time pair
        if not availability_dict[shift] and new_shift_check:
            new_shift_check = False
            time_pairs.append(monday_time + datetime.timedelta(hours=(time_block_number % 48) / 2))
            time_pair_list.append(time_pairs)
            time_pairs = []
    return time_pair_list


def delete_contents(path):
    import os, shutil
    folder = path
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


# generates number volunteers in the volunteers folder
def volunteer_json(volunteers, folder_path):
    # Converting the enums into strings for JSon
    for i in volunteers:
        i.experience_level = i.experience_level.value
    j = 0
    # this is to ensure that the volunteers from previous runs of the file are being deleted
    delete_contents(folder_path)

    for i in volunteers:
        with open(folder_path + '/volunteer' + str(j) + '.json', 'w') as fp:
            json.dump(i.__dict__, fp)
        j += 1
