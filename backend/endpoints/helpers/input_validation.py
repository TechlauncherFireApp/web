from flask_restful import inputs
from ast import literal_eval # casts a string to a dict

def input_dict(value, name):
    try:
        if type(value) is not dict:
            value = literal_eval(value)
        return value
    except:
        raise ValueError("The parameter '{}' is not a dictionary. You gave us: {}".format(name, value))

def input_key_exists(value, key):
    if key not in value:
        raise ValueError("The parameter '{}' does not exist in the dictionary: {}".format(key, value))

# Validate a timeblock input
def input_timeblock(value, key):
    input_key_exists(value, key)
    value[key] = inputs.natural(value[key])
    max_timeblock = 335
    if value[key] > max_timeblock:
        raise ValueError("The parameter '{}' is too large. Max is {}. You gave us: {}".format(key, max_timeblock, value[key]))
    return value

def input_key_positive(value, key):
    input_key_exists(value, key)
    value[key] = inputs.positive(value[key])
    return value

def input_key_natural(value, key):
    input_key_exists(value, key)
    value[key] = inputs.natural(value[key])
    return value
    
def input_key_string(value, key):
    input_key_exists(value, key)
    if type(value[key]) is not str:
        raise ValueError("The parameter '{}' is not a string. You gave us: {}".format(key, value[key]))
    return value

def input_key_enum(value, key, enums):
    input_key_exists(value, key)
    value = input_key_string(value, key)

    valid_enum = False
    for enum in enums:
        if value[key] == enum:
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