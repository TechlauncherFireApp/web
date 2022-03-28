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

# Should this function maybe be refactored to 'check_user_email'

def get_user_email(session, user_email):
    """
    Password Retrieval
    vertify whether email is legal or not, whether email account have been created
    :param session:
    :param user_email: the email account that user wants to reset the password.
    :return: True: check input email address exists and legal
            False: input email does not exists in the database or illegal
    """
    # TODO:
    # delete the print statements after testing.
    while (user_email.find("@") == -1 or user_email.endswith(('com', 'au'))):
        print("the format of input email is wrong.")
        return False
    user = session.query(User).filter(User.email == user_email).first()
    if user.email:
        print("your email exists in current database, and then send code to email.")
        return True
    print("your email haven't create an account, please click the sign up button.")
    return False
# Are the print statements for testing?
# Yes