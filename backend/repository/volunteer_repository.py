from operator import or_

from domain import User, Qualification, UserRole, Role


def get_volunteer(session, volunteer_id):
    return session.query(User) \
        .filter(User.id == volunteer_id) \
        .first()


def list_volunteers(session, volunteer_id=None):
    users = session.query(User.id.label("ID"),
                         User.first_name.label('firstName'),
                         User.last_name.label('lastName'),
                         User.email.label('email'),
                         User.mobile_number.label('mobileNo'),
                         User.preferred_hours.label('prefHours'),
                         User.experience_years.label('expYears'),
                         User.qualifications.label('qualifications'),
                         User.availabilities.label('availabilities'))\
        .filter(or_(User.id == volunteer_id, volunteer_id == None))\
        .all()

    rtn = []
    # Set their roles
    for user in users:
        user = user._asdict()
        roles = session.query(Role.name) \
            .join(UserRole, Role.id == UserRole.role_id)\
            .filter(UserRole.user_id == user['ID'])\
            .all()
        user['possibleRoles'] = [x[0] for x in roles]
        rtn.append(user)

    # TODO: Do the same thing here for qualifications
    return rtn

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
