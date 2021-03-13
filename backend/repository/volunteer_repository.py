from backend.domain import Volunteer


def get_volunteer(session, volunteer_id):
    return session.query(Volunteer) \
        .filter(Volunteer.id == volunteer_id) \
        .first()


def set_availabilities(session, volunteer_id, availability_json):
    volunteer = session.query(Volunteer) \
        .filter(Volunteer.id == volunteer_id) \
        .first()
    volunteer.availabilities = availability_json


def set_preferred_hours(session, volunteer_id, preferred_hours):
    volunteer = session.query(Volunteer) \
        .filter(Volunteer.id == volunteer_id) \
        .first()
    volunteer.preferred_hours = preferred_hours
