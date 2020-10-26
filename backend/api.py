# Flask
from flask import Flask, request
from flask_cors import CORS, cross_origin
from flask_restful import Api, Resource
from includes.main import error_message, contains
import json
# Endpoints
from endpoints.hello_world import HelloWorld
from endpoints.new_request import NewRequest
from endpoints.recommendation import Recommendation
# from endpoints.assignment import Assignment
from endpoints.volunteer_all import VolunteerAll
from endpoints.volunteer import Volunteer
from endpoints.volunteer_status import VolunteerStatus
from endpoints.volunteer_shifts import VolunteerShifts
from endpoints.volunteer_availability import VolunteerAvailability
from endpoints.volunteer_prefhours import VolunteerPrefhours
from endpoints.vehicle_request import VehicleRequest
from endpoints.shift_request import ShiftRequest
from endpoints.existing_requests import ExistingRequests
# Load environment variables
from load_env import load_env

def create_app():
    load_env()

    app = Flask(__name__)
    cors = CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'
    # app.config['Access-Control-Allow-Credentials'] = 'true'
    api = Api(app)

    # Define the api's endpoints
    api.add_resource(HelloWorld, '/hello-world')
    api.add_resource(NewRequest, "/new_request")
    api.add_resource(Recommendation, '/recommendation')
    # api.add_resource(Assignment, '/assignment',
    #     resource_class_kwargs={ 'volunteer_list': volunteer_list })
    api.add_resource(VolunteerAll, '/volunteer/all')
    api.add_resource(Volunteer, '/volunteer')
    api.add_resource(VolunteerStatus, '/volunteer/status')
    api.add_resource(VolunteerShifts, '/volunteer/shifts')
    api.add_resource(VolunteerAvailability, '/volunteer/availability')
    api.add_resource(VolunteerPrefhours, '/volunteer/prefhours')
    api.add_resource(VehicleRequest, '/vehicle/request')
    api.add_resource(ShiftRequest, '/shift/request')
    api.add_resource(ExistingRequests, "/existing_requests")

    return app

if __name__ == '__main__':
    create_app().run(debug=True)