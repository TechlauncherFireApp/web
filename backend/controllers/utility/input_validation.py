from flask_restful import inputs
from ast import literal_eval # casts a string to a dict
from pytz import UTC

# Function checks if a key exists
def input_key_exists(value, key):
    if key not in value:
        raise ValueError("The parameter '{}' does not exist in the dictionary: {}".format(key, value))

'''
Validates a key within a dictionary (value)
Checks if the key exists
Then validates using a specified type function.
Type function can be from below or a custom one. Must return value.
'''
def input_key_type(value, key, type_validator, extra_args):
    try:
        input_key_exists(value, key)
        value[key] = type_validator(value[key], *extra_args)
        return value
    except Exception as e:
        # raise ValueError("Error validating key '{}':\n{}".format(key)) from e...
        raise ValueError("Error validating key '{}', ({})".format(key, e))

'''
Validates that every entry of a list is of a type
'''
def type_list_of(value, type_validator, extra_args):
    try:
        # value = type_list(value)
        if type(value) is not list:
            raise ValueError("Expected list, you gave us: {}".format(value))
        else:
            #
            for index, item in enumerate(value):
                value[index] = type_validator(item, *extra_args)
        return value
    except Exception as e:
        raise ValueError("Error validating list, ({})".format(e))

'''
Type functions validate whether a value is a type
They cast the value to the type and return
If the cast is unsuccessful, they throw an error
'''
def type_dict(value):
    try:
        if type(value) is not dict:
            value = literal_eval(value)
        return value
    except:
        raise ValueError("Expected a dictionary, you gave us: '{}'.".format(value))

def type_datetime(value):
    return inputs.datetime_from_iso8601(value).replace(tzinfo=UTC)

def type_positive(value):
    return inputs.positive(value)

def type_natural(value):
    return inputs.natural(value)

def type_fixed(value, decimals):
    return round(value, decimals)
    

def type_string(value):
    if type(value) is not str:
        raise ValueError("Expected a string, you gave us: '{}'.".format(value))
    return value

def type_enum(value, enums):
    value = type_string(value)
    valid_enum = False
    for enum in enums:
        if value == enum:
            valid_enum = True
            continue
    if not valid_enum:
        raise ValueError("Expected a string enum of form: {}, You gave us: '{}'.".format(str(enums), value))
    return value

def type_list(value):
    if type(value) is not list:
        raise ValueError("Expected list, you gave us: {}".format(value))
    return value

def type_list_of_length(value, length):
    value = type_list(value)
    if len(value) is not length:
        raise ValueError("Expected a list of length {}, You gave us: '{}'".format(length, value))
    return value
