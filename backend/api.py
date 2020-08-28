# Flask
from flask import Flask, request
from flask_cors import CORS, cross_origin
from flask_restful import Api, Resource
from includes.main import error_message, contains
import json
# Endpoints
from endpoints.hello_world import HelloWorld
from endpoints.recommendation import Recommendation
# from endpoints.assignment import Assignment
from endpoints.NewAssetRequest import NewAssetRequest
from endpoints.volunteer_all import VolunteerAll
from endpoints.shift_request import ShiftRequest
from AssetRequestVehicle.initial import Initial as AssetRequestVehicle_initial
from AssetRequestVehicle.submit import Submit as AssetRequestVehicle_submit
# Load environment variables
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
# app.config['Access-Control-Allow-Credentials'] = 'true'
api = Api(app)

# Define the api's endpoints
api.add_resource(HelloWorld, '/hello-world')
api.add_resource(Recommendation, '/recommendation')
# api.add_resource(Assignment, '/assignment',
#     resource_class_kwargs={ 'volunteer_list': volunteer_list })
api.add_resource(VolunteerAll, '/volunteer/all')
api.add_resource(ShiftRequest, '/shift/request')
api.add_resource(NewAssetRequest, "/NewAssetRequest")

@app.route("/NewAssetRequest", methods=["POST"])
def method_NewAssetRequest():
    d = json.loads(request.data)                                            # Get POST Data
    if (type(d) is dict) and contains(str(d["title"])):
        o = NewAssetRequest.get(d["title"])                                 # Get Ouput
        if type(o) in [dict, list]: return json.dumps(o)
        else: return o
    return error_message()

@app.route("/AssetRequestVehicle/initial", methods=["POST"])
def method_AssetRequestVehicle_initial():
    d = json.loads(request.data)                                            # Get POST Data
    if (type(d) is dict) and contains(d["id"]):
        o = AssetRequestVehicle_initial.get(d["id"])                        # Get Ouput
        if type(o) in [dict, list]: return json.dumps(o)
        else: return o
    return error_message()

@app.route("/AssetRequestVehicle/submit", methods=["POST"])
def method_AssetRequestVehicle_submit():
    d = json.loads(request.data)                                            # Get POST Data
    if (type(d) is dict) and contains(d["id"], d["vehicles"]):
        o = AssetRequestVehicle_submit.get(d["id"], d["vehicles"])          # Get Ouput
        if type(o) in [dict, list]: return json.dumps(o)
        else: return o
    return error_message()

if __name__ == '__main__':
    app.run(debug=True)