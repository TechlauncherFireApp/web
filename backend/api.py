from flask import Flask
from flask_restful import Api, Resource
from endpoints.hello_world import HelloWorld

app = Flask(__name__)
api = Api(app)

# Define the api's endpoints
api.add_resource(HelloWorld, '/hello-world')


if __name__ == '__main__':
    app.run(debug=True)