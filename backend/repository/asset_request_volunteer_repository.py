from domain import AssetRequestVolunteer, AssetRequest, AssetRequestVehicle, User
from services.mail import MailSender

sender = MailSender()


def get_asset_request_volunteer(session, volunteer_id, vehicle_id):
    return session.query(AssetRequestVolunteer) \
        .filter(AssetRequestVolunteer.volunteer_id == volunteer_id) \
        .filter(AssetRequestVolunteer.vehicle_id == vehicle_id) \
        .first()


def set_asset_request_volunteer_status(session, status, volunteer_id, shift_id):
    print(status, volunteer_id, shift_id)
    record = session.query(AssetRequestVolunteer) \
        .filter(AssetRequestVolunteer.user_id == volunteer_id) \
        .filter(AssetRequestVolunteer.id == shift_id) \
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
        .filter(AssetRequestVolunteer.user_id == volunteer_id) \
        .all()


def get_shifts_by_request(session, request_id):
    return session.query(AssetRequest.id,
                         AssetRequestVehicle.id.label('shiftID'),
                         AssetRequestVehicle.type.label('assetClass'),
                         AssetRequestVehicle.from_date_time.label('startTime'),
                         AssetRequestVehicle.to_date_time.label('endTime')) \
        .join(AssetRequestVehicle, AssetRequest.id == AssetRequestVehicle.request_id) \
        .filter(AssetRequestVehicle.request_id == request_id) \
        .all()


def get_volunteers(session, vehicle_id):
    return session.query(AssetRequestVolunteer.user_id.label("ID"),
                         AssetRequestVolunteer.position.label("positionID"),
                         AssetRequestVolunteer.roles.label("role"),
                         AssetRequestVolunteer.status.label("status")) \
        .filter(AssetRequestVolunteer.vehicle_id == vehicle_id) \
        .all()


def update_shift_by_position(session, vehicle_id, position, user_id, role):
    record = session.query(AssetRequestVolunteer) \
        .filter(AssetRequestVolunteer.vehicle_id == vehicle_id) \
        .filter(AssetRequestVolunteer.position == position) \
        .first()
    record.user_id = user_id
    record.roles = role

    if record.user is not None:
        # Send an email to the person about their assignment
        data = {
            'startTime': record.asset_request_vehicle.from_date_time.strftime('%H:%M:%S %d %b %Y'),
            'endTime': record.asset_request_vehicle.to_date_time.strftime('%H:%M:%S %d %b %Y'),
            'role': ', '.join(record.roles)
        }
        sender.email(record.user.email, 'roster', data)
        return record.id


def add_shift(session, volunteer_id, vehicle_id, position, roles):
    # Save the record to the database
    record = AssetRequestVolunteer(user_id=volunteer_id, vehicle_id=vehicle_id, position=position, roles=roles,
                                   status='pending')
    session.add(record)
    session.flush()

    if record.user is not None:
        # Send an email to the person about their assignment
        data = {
            'startTime': record.asset_request_vehicle.from_date_time.strftime('%H:%M:%S %d %b %Y'),
            'endTime': record.asset_request_vehicle.to_date_time.strftime('%H:%M:%S %d %b %Y'),
            'role': ', '.join(record.roles)
        }
        sender.email(record.user.email, 'roster', data)
        return record.id
