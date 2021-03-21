from enum import Enum


class RegisterResult(Enum):
    SUCCESS = -1
    USERNAME_ALREADY_REGISTERED = 0
    BAD_USERNAME = 1
    BAD_PASSWORD = 2
    BAD_ROLE = 3
