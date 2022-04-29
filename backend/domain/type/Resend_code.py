from enum import Enum

class ResendEmail(Enum):
    SUCCESS = 0
    FAIL = 1
    RECHECK_TWO_INPUTS = 2
    BAD_PASSWORD = 3
