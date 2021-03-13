from backend.domain import Volunteer


def get_volunteer(session, volunteer_id):
    return session.query(Volunteer) \
        .filter(Volunteer.id == volunteer_id) \
        .first()


def list_volunteers(session):
    return session.query(Volunteer.id.label("ID"),
                         Volunteer.first_name.label('firstName'),
                         Volunteer.last_name.label('lastName'),
                         Volunteer.email.label('email'),
                         Volunteer.mobile_number.label('mobileNo'),
                         Volunteer.preferred_hours.label('prefHours'),
                         Volunteer.experience_years.label('expYears'),
                         Volunteer.possibleRoles.label('possibleRoles'),
                         Volunteer.qualifications.label('qualifications'),
                         Volunteer.availabilities.label('availabilities')).all()



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
