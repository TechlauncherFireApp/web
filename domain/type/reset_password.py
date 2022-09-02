from enum import Enum

class ResetPassword(Enum):
    SUCCESS = 0
    FAIL = 1
    RECHECK_TWO_INPUTS = 2
    BAD_PASSWORD = 3
