from enum import Enum

class VerifyCode(Enum):
    CODE_CONSISTENCE = 0
    FAIL = 1
    CODE_OVERDUE = 2
    CODE_INCONSISTENCY = 3
