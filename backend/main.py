from flask import Flask
from backend.controllers import *

# Register the application
app = Flask(__name__)

# Register all controllers individually
app.register_blueprint(existing_requests_bp)
app.register_blueprint(new_request_bp)
app.register_blueprint(recommendation_bp)
app.register_blueprint(shift_request_bp)
app.register_blueprint(vehicle_request_bp)
app.register_blueprint(volunteer_bp)
app.register_blueprint(volunteer_all_bp)
app.register_blueprint(volunteer_availability_bp)
app.register_blueprint(volunteer_pref_hours_bp)
app.register_blueprint(volunteer_shifts_bp)
app.register_blueprint(volunteer_status_bp)
