from domain import Role, Qualification, AssetType


def get_roles(session):
    return session.query(Role.id, Role.name, Role.insert_date_time, Role.update_date_time, Role.deleted) \
        .all()


def add_role(session, role_name):
    role = Role(name=role_name)
    session.add(role)
    session.flush()
    return role.id


def toggle_role(session, role_name):
    existing_role = session.query(Role) \
        .filter(Role.name == role_name) \
        .first()
    if existing_role is None:
        return
    existing_role.deleted = not existing_role.deleted


def get_qualifications(session):
    return session.query(Qualification.id, Qualification.name, Qualification.insert_date_time, Qualification.update_date_time,
                         Qualification.deleted) \
        .all()


def add_qualification(session, qualification_name):
    qualification = Qualification(name=qualification_name)
    session.add(qualification)
    session.flush()
    return qualification.id


def toggle_qualification(session, qualification_name):
    existing_qualification = session.query(Qualification) \
        .filter(Qualification.name == qualification_name) \
        .first()
    if existing_qualification is None:
        return
    existing_qualification.deleted = not existing_qualification.deleted


def get_asset_type(session):
    return session.query(AssetType.id, AssetType.name, AssetType.code, AssetType.insert_date_time, AssetType.update_date_time,
                         AssetType.deleted) \
        .all()


def add_asset_type(session, asset_type_code, asset_type_name):
    asset_type = AssetType(name=asset_type_name, code=asset_type_code)
    session.add(asset_type)
    session.flush()
    return asset_type.id


def toggle_asset_type(session, asset_type_code):
    existing_asset_type = session.query(AssetType) \
        .filter(AssetType.code == asset_type_code) \
        .first()
    if existing_asset_type is None:
        return
    existing_asset_type.deleted = not existing_asset_type.deleted
