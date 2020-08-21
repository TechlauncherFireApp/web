# Flask
from flask import Flask, request
from flask_cors import CORS, cross_origin
from flask_restful import Api, Resource
from includes.main import message_return, contains
import json
# Endpoints
from endpoints.hello_world import HelloWorld
from endpoints.NewAssetRequest import NewAssetRequest
from AssetRequestVehicle.initial import Initial as AssetRequestVehicle_initial

# from endpoints.recommendation import Recommendation
# from endpoints.assignment import Assignment
# Gurobi
# from gurobi.DataGenerator import LoadVolunteers, LoadVolunteer, SetVolunteerNumber

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
# app.config['Access-Control-Allow-Credentials'] = 'true'
api = Api(app)

# Ensure volunteers have been generated
# Inputs
#   string: file path to save volunteers
#   int: number of volunteers to generate
#   boolean: whether to regenerate volunteers on every interface restart
#

# SetVolunteerNumber('volunteers', 200, False)
# volunteer_list = LoadVolunteers('volunteers')

# Define the api's endpoints
api.add_resource(HelloWorld, '/hello-world')
# api.add_resource(Recommendation, '/recommendation',
#     resource_class_kwargs={ 'volunteer_list': volunteer_list })
# api.add_resource(Assignment, '/assignment',
#     resource_class_kwargs={ 'volunteer_list': volunteer_list })
api.add_resource(NewAssetRequest, "/NewAssetRequest")

@app.route("/AssetRequestVehicle/initial", methods=["POST"])
def method():
    d = json.loads(request.data)
    if (type(d) is dict) and contains(d["id"]): return AssetRequestVehicle_initial.get(d["id"])
    return message_return()

if __name__ == '__main__':
    app.run(debug=True)