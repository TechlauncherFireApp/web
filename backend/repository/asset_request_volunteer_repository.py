from backend.domain import AssetRequestVolunteer, AssetRequest, AssetRequestVehicle, Volunteer


def get_asset_request_volunteer(session, volunteer_id, vehicle_id):
    return session.query(AssetRequestVolunteer) \
        .filter(AssetRequestVolunteer.volunteer_id == volunteer_id) \
        .filter(AssetRequestVolunteer.vehicle_id == vehicle_id) \
        .first()


def set_asset_request_volunteer_status(session, status, volunteer_id, vehicle_id):
    record = session.query(AssetRequestVolunteer) \
        .filter(AssetRequestVolunteer.volunteer_id == volunteer_id) \
        .filter(AssetRequestVolunteer.vehicle_id == vehicle_id) \
        .first()
    record.status = status


def get_request_by_volunteer(session, volunteer_id):
    return session.query(AssetRequest.title.label("requestTitle"),
                         AssetRequestVolunteer.id.label("vehicleID"),
                         AssetRequestVehicle.type.label("vehicleType"),
                         AssetRequestVehicle.from_date_time.label("vehicleFrom"),
                         AssetRequestVehicle.to_date_time.label("vehicleTo"),
                         AssetRequestVolunteer.roles.label("volunteerRoles"),
                         AssetRequestVolunteer.status.label("volunteerStatus")) \
        .join(AssetRequestVehicle, AssetRequestVehicle.id == AssetRequestVolunteer.vehicle_id) \
        .join(AssetRequest, AssetRequest.id == AssetRequestVehicle.request_id) \
        .filter(AssetRequestVolunteer.volunteer_id == volunteer_id)\
        .all()
