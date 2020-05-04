from flask import Flask
from flask_restful import reqparse, abort, Resource

class HelloWorld(Resource):
    def get(self):
        return {"value": "Hello World!"}