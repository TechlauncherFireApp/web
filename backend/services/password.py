import bcrypt


class PasswordService:
    """
    Manages password hashing & comparison in a cryptographically secure method.
    """
    _MIN_LENGTH = 10
    _ALLOWED_CHARACTERS = set(c for c in '0123456789acbcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYz!@#$%^&*()_+')

    @staticmethod
    def hash(plaintext: str) -> bytes:
        """
        Hash a plaintext password, returning a bytes-like object of the password, hashed.
        :param plaintext: The password to hash.
        :return: The password, hashed as bytes.
        """
        return bcrypt.hashpw(bytes(plaintext), bcrypt.gensalt())

    @staticmethod
    def compare(plaintext: str, hashed: bytes) -> bool:
        """
        Compare a plaintext password and a corresponding hashed password, returning true when the two strings are equal.
        :param plaintext: The plaintext password input
        :param hashed: A hashed function to compare to.
        :return: True when they are equal, otherwise false.
        """
        return bcrypt.checkpw(bytes(plaintext), hashed)

    def validate(self, plaintext: str) -> bool:
        """
        Check that a plaintext password meets our minimum password requirements.
        :param plaintext: The password to check the validity of.
        :return: True if the password is valid.
        """
        if len(plaintext) < self._MIN_LENGTH:
            return False
        if any(passChar not in self._ALLOWED_CHARACTERS for passChar in plaintext):
            return False
        return True
