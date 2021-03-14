from flask import Flask
from backend.controllers import existing_requests_bp, new_request_bp, volunteer_availability_bp, \
    volunteer_preferred_hours_bp, volunteer_status_bp, volunteer_shifts_bp, volunteer_all_bp, volunteer_bp, \
    recommendation_bp

# Register the application
app = Flask(__name__)

# Register all controllers individually
app.register_blueprint(existing_requests_bp)
app.register_blueprint(new_request_bp)
app.register_blueprint(recommendation_bp)
# app.register_blueprint(shift_request_bp)
# app.register_blueprint(vehicle_request_bp)
app.register_blueprint(volunteer_bp)
app.register_blueprint(volunteer_all_bp)
app.register_blueprint(volunteer_availability_bp)
app.register_blueprint(volunteer_preferred_hours_bp)
app.register_blueprint(volunteer_shifts_bp)
app.register_blueprint(volunteer_status_bp)


@app.route('/')
def main():
    return "Running..."


if __name__ == '__main__':
    import logging

    logging.basicConfig(filename='error.log', level=logging.DEBUG)
    app.run(host='0.0.0.0')
