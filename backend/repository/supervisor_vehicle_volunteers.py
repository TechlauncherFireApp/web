from sqlalchemy import func, select

from domain import AssetRequestVolunteer


def remove_vehicle_volunteer(session, vehicle_id, position):
    existing = session.query(AssetRequestVolunteer) \
        .filter(AssetRequestVolunteer.vehicle_id == vehicle_id) \
        .all()
    role_num = len(existing)
    if role_num <= 0 or role_num <= position:
        return False
    else:
        session.delete(existing[position])
        session.flush
        return True





def insert_vehicle_volunteer(session, vehicle_id, role_id):
    new_role = AssetRequestVolunteer(vehicle_id=vehicle_id, role_id=role_id)
    session.add(new_role)
    session.flush()
    return new_role.id
