from backend.domain import Volunteer


def get_availabilities(session, volunteer_id):
    session.query(Volunteer.availabilities) \
        .filter(Volunteer.id == volunteer_id) \
        .first()


def set_availabilities(session, volunteer_id, availability_json):
    volunteer = session.query(Volunteer) \
        .filter(Volunteer.id == volunteer_id) \
        .first()
    volunteer.availabilities = availability_json
