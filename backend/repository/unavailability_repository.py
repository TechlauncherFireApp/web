from operator import or_
from domain import User, UnavailabilityTime



def create_event(session, userId, title, startTime, endTime, periodicity):
    event = UnavailabilityTime(userId=userId, event_title=title, start_time=startTime, endTime=endTime,
                               periodicity=periodicity)
    session.add(event)
    # session.expunge(question)
    session.flush()
    return event.eventId


def remove_event(session, userId, eventId):
    existing = session.query(UnavailabilityTime).filter(UnavailabilityTime.id == userId,
                                                        UnavailabilityTime.eventId == eventId).first()
    if existing is not None:
        existing.status = False
        return True
    return False


def update_event(session, userId, eventId, startTime, endTime, title, periodicity):
    event = session.query(UnavailabilityTime).filter(UnavailabilityTime.id == userId,
                                                     UnavailabilityTime.eventId == eventId).first()

    if not event.status:
        return False
    event.startTime = startTime
    event.endTime = endTime
    event.title = title
    event.periodicity = periodicity
    return True
