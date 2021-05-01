from ics import Calendar, Event


class AttachmentService:

    def __init__(self):
        pass

    @staticmethod
    def generate(title, start_date, end_date):
        c = Calendar()
        e = Event()
        e.name = title
        e.begin = start_date
        e.end = end_date
        c.events.add(e)
        return c
