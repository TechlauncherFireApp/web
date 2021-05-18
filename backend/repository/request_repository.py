from domain import AssetRequest, User, UserType, AssetRequestVehicle, AssetRequestVolunteer


def get_existing_requests(session):
    """
    Get all existing asset requests.
    :param session: A database session context
    :return: A list of asset requests
    """
    return session.query(AssetRequest)


def new_request(session, title, status):
    """
    Add a new request to the database.
    :param session: A database session context
    :param title: The name of the request
    :param status: The status of the request
    :return: The id of the newly created request.
    """
    # TODO: Permissions
    #   - Source the current as an admin
    admin = session.query(User).filter(User.role == UserType.ADMIN).first()
    request = AssetRequest(title=title, user_id=admin.id, status=status)
    session.add(request)
    session.flush()
    return request.id


def delete_request(session, requestID):
    """
    :param session: A database session context
    :param requestID: The id of the request
    :return: Boolean indicating whether delete was successful
    """
    record = session.query(AssetRequest) \
        .filter(AssetRequest.id == requestID) \
        .first()
    if record is not None:
        vehicles = session.query(AssetRequestVehicle) \
            .filter(AssetRequestVehicle.request_id == record.id) \
            .all()
        for vehicle in vehicles:
            vehicle_volunteers = session.query(AssetRequestVolunteer) \
                .filter(AssetRequestVolunteer.vehicle_id == vehicle.id) \
                .all()
            for vehicle_volunteer in vehicle_volunteers:
                session.delete(vehicle_volunteer)
            session.delete(vehicle)
        session.delete(record)
        return True
    return False


def update_request_status(session, request_id, status):
    """
    :param session: A database session context
    :param request_id: The id of the request
    :param status: The new status of the request
    :return: Boolean indicating whether the update was successful
    """
    record = session.query(AssetRequest) \
        .filter(AssetRequest.id == request_id) \
        .first()
    if record is not None:
        record.status = status
        return True
    return False
