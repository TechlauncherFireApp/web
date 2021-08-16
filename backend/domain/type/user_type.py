from enum import Enum


class UserType(Enum):
    VOLUNTEER = 0
    ADMIN = 1
    # promotion 0 -> 1 -> 2
    # demotion 1 -> 0
    ROOT_ADMIN = 2
