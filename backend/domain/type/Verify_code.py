from enum import Enum

class VerifyCode(Enum):
    CODE_CORRECT = 0
    FAIL = 1
    CODE_OVERDUE = 2
    CODE_INCORRECT = 3
