from operator import or_
from domain import User,UnavailabilityTime

def get_unavailablity(session, volunteer_id):
    return session.query(UnavailabilityTime) \
        .filter(UnavailabilityTime.userId == volunteer_id) \
        .first()

def set_unavailability(session, volunteer_id,):
    volunteer = session.query(UnavailabilityTime) \
        .filter(UnavailabilityTime.userId == volunteer_id) \
        .first()
    # TODO: add modify code here