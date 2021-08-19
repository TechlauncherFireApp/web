from domain import User, UserType
from operator import or_


def promote_user(session, user_id):
    user = session.query(User). \
        filter(User.id == user_id).first()
    print('user:', user.id, 'is now promote from', user.role)
    if user:
        current_type = user.role
        if current_type == UserType.VOLUNTEER:
            user.role = UserType.ADMIN
            print(user.role)
            return True
        elif current_type == UserType.ADMIN:
            user.role = UserType.ROOT_ADMIN
            print(user.role)
            return True
    return False


def demote_user(session, user_id):
    user = session.query(User).\
        filter(User.id == user_id).first()
    print('user:', user.id, 'is now demote from', user.role)
    if user:
        current_type = user.role
        if current_type == UserType.ADMIN:
            user.role = UserType.VOLUNTEER
            print(user.role)
            return True
    return False


def self_demote(session, user_id):
    user = session.query(User).\
        filter(User.id == user_id).first()
    print('user:', user.id, 'is now demote from', user.role)
    if user:
        if user.role == '':
            user.role = UserType.ROOT_ADMIN
        current_type = user.role
        if current_type == UserType.ROOT_ADMIN:
            user.role = UserType.ADMIN
            print(user.role)
            return True
    return False

