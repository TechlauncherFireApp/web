from domain import UnavailabilityTime


def create_event(session, userId, title, startTime, endTime, periodicity):
    """
     Function to create an event
    :param session: session
    :param userId: Integer, user id
    :param title: String, reason why unavailable
    :param startTime: DateTime, from what time is unavailable
    :param endTime: DateTime, to what time is unavailable
    :param periodicity: Integer, Daily = 1, Weekly = 2, One-Off = 3
    """
    event = UnavailabilityTime(userId=userId, event_title=title, start_time=startTime, endTime=endTime,
                               periodicity=periodicity)
    session.add(event)
    # session.expunge(question)
    session.flush()
    return event.eventId


def remove_event(session, userId, eventId):
    """
    Function to remove an event
    :param session: session
    :param userId: Integer, user id, who want to remove an event
    :param eventId: Integer, event id want to remove
    :return: True: remove successful
             False: remove failed
    """
    existing = session.query(UnavailabilityTime).filter(UnavailabilityTime.id == userId,
                                                        UnavailabilityTime.eventId == eventId).first()
    if existing is not None:
        existing.status = False
        return True
    return False


def update_event(session, userId, eventId, startTime, endTime, title, periodicity):
    """
    Function to update an event
    :param session: session
    :param userId: Integer, user id, who want to update an event
    :param eventId: Integer, user id, which event to be updated
    :param title: String, reason why unavailable
    :param startTime: DateTime, from what time is unavailable
    :param endTime: DateTime, to what time is unavailable
    :param periodicity: Integer, Daily = 1, Weekly = 2, One-Off = 3
    :return: True: update successful
             False: update failed
    """
    event = session.query(UnavailabilityTime).filter(UnavailabilityTime.id == userId,
                                                     UnavailabilityTime.eventId == eventId).first()

    if not event.status:
        return False
    event.startTime = startTime
    event.endTime = endTime
    event.title = title
    event.periodicity = periodicity
    return True


def fetch_event(session, userId):
    """
    Find all unavailable events for specified user
    :param session: session
    :param userId: user id
    """
    events = session.query(UnavailabilityTime) \
        .filter(UnavailabilityTime.status == 1, UnavailabilityTime.userId == userId)
    # We need to use objects after this session closed
    session.expunge_all()
    return events
