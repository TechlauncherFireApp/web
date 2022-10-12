from domain import User, UserType


def get_user_role(session, user_id):
    user = session.query(User). \
        filter(User.id == user_id).first()
    if user and user.role != '':
        return int(user.role.value)
    return -1


def promote_user(session, user_id):
    user = session.query(User). \
        filter(User.id == user_id).first()
    print('user:', user.id, 'is now promoted from', user.role)
    if user and user.role != '':
        current_type = user.role
        if current_type == UserType.VOLUNTEER:
            user.role = UserType.ADMIN
            print('user:', user.id, 'is now', user.role)
            return True
        elif current_type == UserType.ADMIN:
            user.role = UserType.ROOT_ADMIN
            print('user:', user.id, 'is now', user.role)
            return True
    return False


def demote_user(session, user_id):
    user = session.query(User). \
        filter(User.id == user_id).first()
    print('user:', user.id, 'is now demoted from', user.role)
    if user:
        current_type = user.role
        if current_type == UserType.ADMIN:
            user.role = UserType.VOLUNTEER
            print('user:', user.id, 'is now', user.role)
            return True
    return False


def self_demote(session, user_id):
    user = session.query(User). \
        filter(User.id == user_id).first()
    print('user:', user.id, 'is now demoted from', user.role)
    if user:
        current_type = user.role
        if current_type == UserType.ROOT_ADMIN:
            user.role = UserType.ADMIN
            print('user:', user.id, 'is now', user.role)
            return True
    return False


def get_user_by_email(session, email):
    user = session.query(User). \
        filter(User.email == email).first()
    if user:
        return user


def get_volunteer_id_name(session):
    dic_volunteer = {}
    volunteer_list = session.query(User.id, User.first_name, User.last_name).filter(User.role == "VOLUNTEER").all()
    for v in volunteer_list:
        id = v.id
        name = v.first_name + " " + v.last_name
        dic_volunteer[id] = name
    return dic_volunteer
