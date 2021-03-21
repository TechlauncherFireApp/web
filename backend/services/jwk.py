import flask_restful
from flask import request
from jwcrypto import jwt
from jwcrypto import jwk

__secret__ = jwk.JWK.generate(kty='oct', size=256)
__issuer__ = "FIREAPP2.0"


class JWKService:

    @staticmethod
    def generate(subject: int, name: str) -> str:
        """
        Generate a JWT token for communication between client and application server.
        :param subject: The subject (ID) of the client for the token.
        :param name: The name of the client for the token.
        :return: The token as a string.
        """
        # TODO: Authentication
        #   - Add token expiry & refreshing, low priority in MVP
        token = jwt.JWT(header={"alg": "HS256"}, claims={"sub": f"{subject}", "name": name, "iss": __issuer__})
        token.make_signed_token(__secret__)
        token = token.serialize()
        return token

    @staticmethod
    def validate(token) -> bool:
        try:
            jwt.JWT(key=__secret__, jwt=token)
        except Exception:
            return False
        return True

    @staticmethod
    def validate_admin(token) -> bool:
        try:
            decoded = jwt.JWT(key=__secret__, jwt=token)
            print(decoded.claims)
            # TODO: Validate is admin
        except Exception:
            return False
        return True


def requires_auth(func):
    jwkservice = JWKService()

    def wrapper(*args, **kwargs):
        authorization_header = request.headers.get("Authorization")
        if authorization_header is None:
            pass
        token = authorization_header[len('Bearer '):]
        if jwkservice.validate(token):
            return func(*args, **kwargs)
        return flask_restful.abort(401)

    wrapper.__doc__ = func.__doc__
    wrapper.__name__ = func.__name__
    return wrapper


def requires_admin(func):
    jwkservice = JWKService()

    def wrapper(*args, **kwargs):
        authorization_header = request.headers.get("Authorization")
        if authorization_header is None:
            pass
        token = authorization_header[len('Bearer '):]
        if jwkservice.validate_admin(token):
            return func(*args, **kwargs)
        return flask_restful.abort(401)

    wrapper.__doc__ = func.__doc__
    wrapper.__name__ = func.__name__
    return wrapper
