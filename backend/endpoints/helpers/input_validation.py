from flask_restful import inputs
from ast import literal_eval # casts a string to a dict
from pytz import UTC

def input_key_exists(value, key):
    if key not in value:
        raise ValueError("The parameter '{}' does not exist in the dictionary: {}".format(key, value))

def input_key_type(value, key, type_validator):
    input_key_exists(value, key)
    value[key] = type_validator(value[key])
    return value

def input_dict(value, key):
    input_key_exists(value, key)
    value[key] = type_dict(value[key])
    return value

def type_dict(value):
    try:
        if type(value) is not dict:
            value = literal_eval(value)
        return value
    except:
        raise ValueError("'{}' is not a dictionary.".format(value))

def input_datetime(value, key):
    input_key_exists(value, key)
    value[key] = type_datetime(value[key])
    return value

def type_datetime(value):
    return inputs.datetime_from_rfc822(value).replace(tzinfo=UTC)

def input_key_positive(value, key):
    input_key_exists(value, key)
    value[key] = type_positive(value[key])
    return value

def type_positive(value):
    return inputs.positive(value)

def input_key_natural(value, key):
    input_key_exists(value, key)
    value[key] = type_natural(value[key])
    return value

def type_natural(value):
    return inputs.natural(value)
    
def input_key_string(value, key):
    input_key_exists(value, key)
    value[key] = type_string(value[key])
    return value

def type_string(value):
    if type(value) is not str:
        raise ValueError("'{}' is not a string.".format(value))
    return value

def input_key_enum(value, key, enums):
    input_key_exists(value, key)
    value[key] = type_enum(value[key], enums)
    return value

def type_enum(value, enums):
    value = type_string(value)
    valid_enum = False
    for enum in enums:
        if value == enum:
            valid_enum = True
            continue
        
    if not valid_enum:
        raise ValueError("The parameter '{}' is not a valid asset like {}. You gave us: {}".format(key, str(enums), value[key]))
    return value
    
def input_list_of(value, key, of, validator_func, extra_args):
    input_key_exists(value, key)
    try:
        if type(value[key]) is not list:
            # value = literal_eval(value)
            raise ValueError("The parameter '{}' is not a list. You gave us: {}".format(key, value[key]))
        else:
            #
            for num, item in enumerate(value[key]):
                value[key][num] = validator_func(item, *extra_args)
        return value
    except:
        raise ValueError("The parameter '{}' is not a list of '{}'. You gave us: {}".format(key, of, value[key]))