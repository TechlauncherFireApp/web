from sqlalchemy.orm import Session

from backend.domain import User, Admin, Volunteer
from backend.domain.type import UserType, RegisterResult
from backend.services import PasswordService

passwordService = PasswordService()


class AuthenticationService():

    @staticmethod
    def register(session: Session, email: str, password: str, role: UserType, given_name: str, last_name: str,
                 phone: str) -> RegisterResult:
        """
        Register a new user in the application.
        :param given_name: The users given name to register with.
        :param last_name: The users last name to register with.
        :param phone: The users mobile phone number.
        :param session: A SQLAlchemy Session for the query.
        :param email: The email to register with, this is also the username.
        :param password: The password to register with.
        :param role: The role the user is registering with.
        :return: The result of the registration process.
        """
        # Validate the data integrity of the parameters
        if email is None:
            return RegisterResult.BAD_USERNAME
        if password is None or not passwordService.validate(password):
            return RegisterResult.BAD_PASSWORD
        if role is None:
            return RegisterResult.BAD_ROLE

        # Check to see if the user already exists
        if role == UserType.ADMIN:
            existing_user = session.query(User)\
                .join(Admin, User.admin_id == Admin.id)\
                .filter(Admin.email == email)\
                .first()
        else:
            existing_user = session.query(User) \
                .join(Volunteer, User.admin_id == Volunteer.id) \
                .filter(Volunteer.email == email) \
                .first()
        if existing_user is not None:
            return RegisterResult.USERNAME_ALREADY_REGISTERED

        # Everything seems fine, so we go ahead and create the user & the linked account.
        password_hash = passwordService.hash(password)
        new_user = User(role=role, password=password_hash)
        if role == UserType.ADMIN:
            new_admin = Admin(first_name=given_name, last_name=last_name, mobile_number=phone, email=email)
            session.add(new_admin)
            session.flush()
            new_user.admin_id = new_admin.id
        if role == UserType.VOLUNTEER:
            new_admin = Volunteer(first_name=given_name, last_name=last_name, mobile_number=phone, email=email)
            session.add(new_admin)
            session.flush()
            new_user.admin_id = new_admin.id
        session.add(new_user)
        session.flush()
        return RegisterResult.SUCCESS
