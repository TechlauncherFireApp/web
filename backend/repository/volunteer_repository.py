from operator import or_

from domain import User


def get_volunteer(session, volunteer_id):
    return session.query(User) \
        .filter(User.id == volunteer_id) \
        .first()


def list_volunteers(session, volunteer_id=None):
    return session.query(User.id.label("ID"),
                         User.first_name.label('firstName'),
                         User.last_name.label('lastName'),
                         User.email.label('email'),
                         User.mobile_number.label('mobileNo'),
                         User.preferred_hours.label('prefHours'),
                         User.experience_years.label('expYears'),
                         User.possibleRoles.label('possibleRoles'),
                         User.qualifications.label('qualifications'),
                         User.availabilities.label('availabilities'))\
        .filter(or_(User.id == volunteer_id, volunteer_id == None))\
        .all()



def set_availabilities(session, volunteer_id, availability_json):
    volunteer = session.query(User) \
        .filter(User.id == volunteer_id) \
        .first()
    volunteer.availabilities = availability_json


def set_preferred_hours(session, volunteer_id, preferred_hours):
    volunteer = session.query(User) \
        .filter(User.id == volunteer_id) \
        .first()
    volunteer.preferred_hours = preferred_hours
