from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from controllers import *
from controllers import user_type

from domain import session_scope
from repository.volunteer_repository import *

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


@app.route('/')
def main():
    print('xxxx')
    return {
        'status': 'OK',
    }


# function for responses
def results():
    # build a request object
    req = request.get_json(force=True)

    # fetch action from json
    action = req.get('queryResult')
    print(action)
    with session_scope() as session:
        res = get_volunteer(session, 4)
        print(res.availabilities)
        r = availabilities_serialize(res.availabilities)
        print(r)

    # return a fulfillment response
    # return {'fulfillmentText': 'This is a response from FIREAPP.'}
    return {'fulfillmentText': r}


def availabilities_serialize(availabilities: dict, target=None):
    days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    report = 'Your calendar is:\n'
    if not target:
        for day in days:
            day_report = day + ': '
            for time_period in availabilities[day]:
                start_time = time_period[0]
                end_time = time_period[1]
                day_report = day_report + ' from ' + str(start_time) + ' to ' + str(end_time) + ','
            if day_report[-2] == ':':
                day_report = day_report + 'Nothing'
            day_report = day_report + '\n'
            report = report + day_report
    return report


@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    return make_response(jsonify(results()))


if __name__ == '__main__':
    import logging

    logging.basicConfig(filename='error.log', level=logging.DEBUG)
    app.run(host='0.0.0.0')
