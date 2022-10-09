from flask import Flask
from flask_cors import CORS
from controllers import *

# Register the application

application = app = Flask(__name__)

# TODO: Tech Debt
#   - CORS Should be specified at the host level per environment, not a global free-for-all. We do this to stop
#     cross site scripting (XSS) attacks.
CORS(app)

# Register all controllers individually
app.register_blueprint(existing_requests_bp)
app.register_blueprint(new_request_bp)
app.register_blueprint(recommendation_bp)
app.register_blueprint(shift_request_bp)
app.register_blueprint(vehicle_request_bp)
app.register_blueprint(volunteer_bp)
app.register_blueprint(volunteer_all_bp)
app.register_blueprint(volunteer_availability_bp)
app.register_blueprint(volunteer_preferred_hours_bp)
app.register_blueprint(volunteer_shifts_bp)
app.register_blueprint(volunteer_status_bp)
app.register_blueprint(authentication_bp)
app.register_blueprint(reference_bp)
app.register_blueprint(user_role_bp)
app.register_blueprint(asset_type_role_bp)
app.register_blueprint(user_type_bp)
app.register_blueprint(tenancy_config_bp)
app.register_blueprint(tutorial_quiz_bp)
app.register_blueprint(email_bp)
app.register_blueprint(profile_bp)

app.register_blueprint(volunteer_unavailability_bp)
app.register_blueprint(user_bp)
app.register_blueprint(chatbot_bp)



@app.route('/')
def main():
    return {
        'status': 'OK',
    }


if __name__ == '__main__':
    import logging

    logging.basicConfig(filename='error.log', level=logging.DEBUG)
    app.run(host='0.0.0.0')
