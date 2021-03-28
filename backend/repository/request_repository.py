from domain import AssetRequest, User, UserType


def get_existing_requests(session):
    """
    Get all existing asset requests.
    :param session: A database session context
    :return: A list of asset requests
    """
    return session.query(AssetRequest)


def new_request(session, title):
    """
    Add a new request to the database.
    :param session: A database session context
    :param title: The name of the request
    :return: The id of the newly created request.
    """
    # TODO: Permissions
    #   - Source the current as an admin
    admin = session.query(User).filter(User.role == UserType.ADMIN).first()
    request = AssetRequest(title=title, user_id=admin.id)
    session.add(request)
    session.flush()
    return request.id


# TODO: Create delete request function
def delete_request(session, id):
    session.query.filter_by(id).delete()
    session.flush()
    return True
