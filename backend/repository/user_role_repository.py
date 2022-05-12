from domain import User, Role, UserRole
from sqlalchemy import distinct


def get_user_roles(session):
    return session.query(User.id.label('userId'), Role.id.label('roleId')). \
        join(UserRole, UserRole.user_id == User.id). \
        join(Role, Role.id == UserRole.role_id). \
        all()


def get_user_roles_by_id(session, user_id):
    user_roles = session.query(distinct(Role.name)). \
        join(UserRole, UserRole.user_id == user_id). \
        filter(UserRole.user_id == user_id). \
        all()
    user_roles_list = []
    for user_role in user_roles:
        user_roles_list.append(user_role[0])
    return user_roles_list


def add_user_role(session, user_id, role_id):
    existing = session.query(UserRole). \
        filter(UserRole.role_id == role_id).\
        filter(UserRole.user_id == user_id). \
        first()
    if existing is None:
        existing = UserRole(user_id=user_id, role_id=role_id)
        session.add(existing)
        session.flush()
    return existing.id


def delete_user_role(session, user_id, role_id):
    existing = session.query(UserRole). \
        filter(UserRole.role_id == role_id).\
        filter(UserRole.user_id == user_id). \
        first()
    if existing is not None:
        session.delete(existing)
        return True
    return False
