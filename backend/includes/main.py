import math, numbers

error_message = "error"

def message_return(m=None):
    return (m if contains(m) else error_message)

def check_Request(r):
    return (r.is_ajax() and (r.method in ["GET","POST"]))

def contains(*l):
    for i in l:
        if (
            (i is None) or
            ((type(i) is list) and (len(i) <= 0)) or
            ((type(i) is dict) and (not bool(i))) or
            ((type(i) is str) and (i == "")) or
            (isinstance(i, numbers.Number) and math.isnan(i))
        ): return False
    return True