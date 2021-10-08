from flask import Flask, request, abort, redirect
from flask_cors import CORS
from controllers import *
from controllers import user_type

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
app.register_blueprint(user_type.user_type_bp)

# @app.before_request
# def before_request():
#     if request.url.startswith('http://'):
#         url = request.url.replace('http://', 'https://', 1)
#         return redirect(url, code=301)

@app.route('/')
def main():
    if request.url.startswith('http://'):
        return redirect(request.url.replace('http', 'https', 1)
                        .replace('080', '443', 1))
    elif request.url.startswith('https://'):
        return 'Hello HTTPS World!'
    abort(500)
    
    # return {
    #     'status': 'OK',
    # }


if __name__ == '__main__':
    import logging

    logging.basicConfig(filename='error.log', level=logging.DEBUG)
    app.run(host='0.0.0.0', ssl_context='adhoc')
