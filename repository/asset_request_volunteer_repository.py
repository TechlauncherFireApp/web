from domain import AssetRequestVolunteer, AssetRequest, AssetRequestVehicle, User, AssetType, Role
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
                         AssetType.name.label("vehicleType"),
                         AssetRequestVehicle.from_date_time.label("vehicleFrom"),
                         AssetRequestVehicle.to_date_time.label("vehicleTo"),
                         Role.name.label("volunteerRoles"),
                         AssetRequestVolunteer.status.label("volunteerStatus")) \
        .join(AssetRequestVehicle, AssetRequestVehicle.id == AssetRequestVolunteer.vehicle_id) \
        .join(AssetRequest, AssetRequest.id == AssetRequestVehicle.request_id) \
        .join(AssetType, AssetType.id == AssetRequestVehicle.asset_type_id) \
        .join(Role, Role.id == AssetRequestVolunteer.role_id) \
        .filter(AssetRequestVolunteer.user_id == volunteer_id) \
        .all()


def get_shifts_by_request(session, request_id):
    return session.query(AssetRequest.id,
                         AssetRequestVehicle.id.label('shiftID'),
                         AssetType.name.label('assetClass'),
                         AssetRequestVehicle.from_date_time.label('startTime'),
                         AssetRequestVehicle.to_date_time.label('endTime')) \
        .join(AssetRequestVehicle, AssetRequest.id == AssetRequestVehicle.request_id) \
        .join(AssetType, AssetType.id == AssetRequestVehicle.asset_type_id) \
        .filter(AssetRequestVehicle.request_id == request_id) \
        .all()


def get_volunteers(session, vehicle_id):
    return session.query(AssetRequestVolunteer.id.label("positionId"),
                         AssetRequestVolunteer.user_id.label("volunteerId"),
                         Role.name.label("role"),
                         User.first_name.label("volunteerGivenName"),
                         User.last_name.label("volunteerSurname"),
                         User.mobile_number,
                         AssetRequestVolunteer.status.label("status")) \
        .join(Role, Role.id == AssetRequestVolunteer.role_id) \
        .outerjoin(User, User.id == AssetRequestVolunteer.user_id) \
        .filter(AssetRequestVolunteer.vehicle_id == vehicle_id) \
        .all()


def remove_assignment(session, vehicle_id, position_id):
    vehicle = session.query(AssetRequestVolunteer) \
        .filter(AssetRequestVolunteer.id == position_id) \
        .filter(AssetRequestVolunteer.vehicle_id == vehicle_id) \
        .first()
    vehicle.user_id = None
    vehicle.status = None
    session.flush()


def update_shift_by_position(session, vehicle_id, position_id, user_id):
    print(vehicle_id, position_id, user_id)
    asset_request_volunteer = session.query(AssetRequestVolunteer) \
        .filter(AssetRequestVolunteer.id == position_id) \
        .filter(AssetRequestVolunteer.vehicle_id == vehicle_id) \
        .first()
    asset_request_volunteer.user_id = user_id
    asset_request_volunteer.status = 'pending'

    user = session.query(User) \
        .filter(User.id == user_id) \
        .first()

    asset_request_vehicle = session.query(AssetRequestVehicle) \
        .filter(AssetRequestVehicle.id == asset_request_volunteer.vehicle_id) \
        .first()

    print(asset_request_volunteer, asset_request_vehicle, user)

    if asset_request_vehicle is not None:
        # Send an email to the person about their assignment
        data = {
            'startTime': asset_request_vehicle.from_date_time.strftime('%H:%M:%S %d %b %Y'),
            'endTime': asset_request_vehicle.to_date_time.strftime('%H:%M:%S %d %b %Y'),
            'role': asset_request_volunteer.role.name
        }
        sender.email(user.email, 'roster', data, asset_request_vehicle.from_date_time,
                     asset_request_vehicle.to_date_time)
        return asset_request_volunteer.id


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
        sender.email(record.user.email, 'roster', data, record.asset_request_vehicle.from_date_time,
                     record.asset_request_vehicle.to_date_time)
        return record.id
