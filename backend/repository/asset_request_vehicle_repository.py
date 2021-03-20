from sqlalchemy import func

from domain import AssetRequestVehicle


def count_vehicles(session, request_id):
    query = session.query(AssetRequestVehicle)\
        .filter(AssetRequestVehicle.request_id == request_id)
    query = query.with_entities(func.count())
    return query.scalar()


def insert_vehicle(session, request_id, type, date_from, date_to):
    record = AssetRequestVehicle(request_id=request_id, type=type, from_date_time=date_from, to_date_time=date_to)
    session.add(record)
    session.flush()
    return record.id