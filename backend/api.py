# Flask
from flask import Flask
from flask_cors import CORS, cross_origin
from flask_restful import Api, Resource
# Endpoints
from endpoints.hello_world import HelloWorld
from endpoints.recommendation import Recommendation
# Gurobi
from gurobi.DataGenerator import LoadVolunteers, LoadVolunteer, SetVolunteerNumber

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
api = Api(app)

# Ensure volunteers have been generated
# Inputs
#   string: file path to save volunteers
#   int: number of volunteers to generate
#   boolean: whether to regenerate volunteers on every interface restart
#
SetVolunteerNumber('volunteers', 200, True)

# Define the api's endpoints
api.add_resource(HelloWorld, '/hello-world')
api.add_resource(Recommendation, '/recommendation',
    resource_class_kwargs={ 'volunteer_list': LoadVolunteers('volunteers') })


if __name__ == '__main__':
    app.run(debug=True)