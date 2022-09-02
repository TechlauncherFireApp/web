from domain import AssetTypeRole, Role


def get_seats(session, asset_type_id):
    __renumber_seats(session)
    return session.query(AssetTypeRole.id.label('assetTypeRoleId'), AssetTypeRole.seat_number.label('seatNumber'),
                         Role.id.label('roleId'), Role.name.label('roleName')) \
        .join(Role, Role.id == AssetTypeRole.role_id) \
        .filter(AssetTypeRole.asset_type_id == asset_type_id) \
        .all()


def delete_seat(session, assetTypeRoleId):
    record = session.query(AssetTypeRole) \
        .filter(AssetTypeRole.id == assetTypeRoleId) \
        .first()
    if record is not None:
        session.delete(record)
        __renumber_seats(session)


def add_seat(session, asset_type_id, role_id):
    # Seat number is automatically fixed later, set it to -100 so its non-null property is satisfied
    record = AssetTypeRole(asset_type_id=asset_type_id, seat_number=-100, role_id=role_id)
    session.add(record)
    __renumber_seats(session)


def __renumber_seats(session):
    """
    Fairly pointless function that reassigns seat numbers to asset types so that they're a continuous sequence. Don't
    know why I bothered with this, but I did.
    """
    ids = session.query(AssetTypeRole.asset_type_id) \
        .distinct() \
        .all()
    for _id in ids:
        asset_type_role_id, = _id
        asset_type_roles = session.query(AssetTypeRole) \
            .filter(AssetTypeRole.asset_type_id == asset_type_role_id) \
            .order_by(AssetTypeRole.insert_date_time) \
            .all()
        for key, value in enumerate(asset_type_roles):
            value.seat_number = key + 1
