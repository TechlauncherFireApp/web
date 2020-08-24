# Flask
from flask import Flask
from flask_cors import CORS, cross_origin
from flask_restful import Api, Resource
# Endpoints
from endpoints.hello_world import HelloWorld
from endpoints.recommendation import Recommendation
# from endpoints.assignment import Assignment

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
api = Api(app)

# Define the api's endpoints
api.add_resource(HelloWorld, '/hello-world')
api.add_resource(Recommendation, '/recommendation')
# api.add_resource(Assignment, '/assignment',
#     resource_class_kwargs={ 'volunteer_list': volunteer_list })


if __name__ == '__main__':
    app.run(debug=True)