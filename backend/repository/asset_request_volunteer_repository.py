from backend.domain import AssetRequestVolunteer


def get_asset_request_volunteer(session, volunteer_id, vehicle_id):
    return session.query(AssetRequestVolunteer)\
        .filter(AssetRequestVolunteer.volunteer_id == volunteer_id)\
        .filter(AssetRequestVolunteer.vehicle_id == vehicle_id)\
        .first()

def set_asset_request_volunteer_status(session, status, volunteer_id, vehicle_id):
    record = session.query(AssetRequestVolunteer) \
        .filter(AssetRequestVolunteer.volunteer_id == volunteer_id) \
        .filter(AssetRequestVolunteer.vehicle_id == vehicle_id) \
        .first()
    record.status = status