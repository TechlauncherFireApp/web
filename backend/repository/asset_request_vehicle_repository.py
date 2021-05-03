from sqlalchemy import func

from domain import AssetRequestVehicle


def count_vehicles(session, request_id):
    query = session.query(AssetRequestVehicle) \
        .filter(AssetRequestVehicle.request_id == request_id)
    query = query.with_entities(func.count())
    return query.scalar()


def get_vehicles(session, request_id):
    return session.query(AssetRequestVehicle.id.label("ID"),
                         AssetRequestVehicle.type.label("Type"),
                         AssetRequestVehicle.from_date_time.label("From_Time"),
                         AssetRequestVehicle.to_date_time.label("To_Time")) \
        .filter(AssetRequestVehicle.request_id == request_id) \
        .all()


def get_vehicle(session, vehicle_id):
    return session.query(AssetRequestVehicle.id,
                         AssetRequestVehicle.type,
                         AssetRequestVehicle.from_date_time,
                         AssetRequestVehicle.to_date_time) \
        .filter(AssetRequestVehicle.id == vehicle_id) \
        .first()


def insert_vehicle(session, request_id, type, date_from, date_to):
    print(date_from, date_to)
    record = AssetRequestVehicle(request_id=request_id, type=type, from_date_time=date_from, to_date_time=date_to)
    session.add(record)
    session.flush()
    return record.id


def delete_vehicle(session, request_id, vehicle_id):
    record = session.query(AssetRequestVehicle) \
        .filter(AssetRequestVehicle.request_id == request_id) \
        .filter(AssetRequestVehicle.id == vehicle_id) \
        .first()
    if record is not None:
        session.delete(record)
        session.flush()
        return True
    return False
