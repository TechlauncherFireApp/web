from jwcrypto import jwt
from jwcrypto import jwk


class JWKService:
    __secret__ = jwk.JWK.generate(kty='oct', size=256)
    __issuer__ = "FIREAPP2.0"

    def generate(self, subject: int, name: str) -> str:
        """
        Generate a JWT token for communication between client and application server.
        :param subject: The subject (ID) of the client for the token.
        :param name: The name of the client for the token.
        :return: The token as a string.
        """
        # TODO: Authentication
        #   - Add token expiry & refreshing, low priority in MVP
        token = jwt.JWT(header={"alg": "HS256"}, claims={"sub": subject, "name": name, "iss": self.__issuer__})
        token.make_signed_token(self.__secret__)
        token = token.serialize()
        return token
