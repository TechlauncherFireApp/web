from typing import Tuple, Any

from sqlalchemy.orm import Session

from domain import User
from domain.type import UserType, RegisterResult, LoginResult
from services.jwk import JWKService
from services.password import PasswordService

passwordService = PasswordService()
jwk_service = JWKService()


class AuthenticationService():

    @staticmethod
    def register(session: Session, email: str, password: str, given_name: str, last_name: str,
                 phone: str) -> RegisterResult:
        """
        Register a new user in the application.
        :param given_name: The users given name to register with.
        :param last_name: The users last name to register with.
        :param phone: The users mobile phone number.
        :param session: A SQLAlchemy Session for the query.
        :param email: The email to register with, this is also the username.
        :param password: The password to register with.
        :return: The result of the registration process.
        """
        # Validate the data integrity of the parameters
        if email is None:
            return RegisterResult.BAD_USERNAME
        if password is None or not passwordService.validate(password):
            return RegisterResult.BAD_PASSWORD

        # Check to see if the user already exists
        existing_user = session.query(User) \
            .filter(User.email == email) \
            .first()
        if existing_user is not None:
            return RegisterResult.USERNAME_ALREADY_REGISTERED

        # Everything seems fine, so we go ahead and create the user & the linked account.
        password_hash = passwordService.hash(password)
        new_user = User(role=UserType.VOLUNTEER, password=password_hash, first_name=given_name, last_name=last_name,
                        mobile_number=phone, email=email, preferred_hours={}, experience_years=0, possibleRoles=["Basic"],
                        qualifications=[],
                        availabilities={"Friday": [], "Monday": [], "Sunday": [], "Tuesday": [], "Saturday": [],
                                        "Thursday": [], "Wednesday": []})
        session.add(new_user)
        session.flush()
        return RegisterResult.SUCCESS

    @staticmethod
    def login(session: Session, email: str, password: str) -> Tuple[LoginResult, Any, Any]:
        user = session.query(User) \
            .filter(User.email == email) \
            .first()
        # user.role = UserType.ADMIN
        # session.commit()
        if user is None:
            return LoginResult.FAIL, None, None
        if not passwordService.compare(password, user.password):
            return LoginResult.FAIL, None, None

        return LoginResult.SUCCESS, jwk_service.generate(user.id, user.email), user

    # Groundwork for the sendcode backend function
    '''
    @staticmethod
    def send_code(session: Session, email: str):
        if not (get_user_email(Session, email)) or email is None:
            return "EMAIL_NOT_FOUND"
        else:
            sendVerificationCodeEmail()
            return "SUCCESS"
    '''

    # Groundwork for verify backend function
    '''
    @staticmethod
    def verify(session: Session, code: str):
        if code is None
            return "FAILURE"
        if checkUserCode(Session, code):
            return "SUCCESS"
        else:
            return "FAILURE"
    '''
    # CheckUserCode takes the user session and the code and confirms the code is correct. We should consider looking into how security codes are handled in industry

    # Groundwork for reset password function
    '''
    @staticmethod
    def reset(session: Session, Password: str, Password2: str):
        if Password != Password2:
            return "'NO_MATCH'"
        if #find the function for checking if a password matches the criteria:
            return "FAILURE"
        elif: 
            setNewPassword(session: Session, Password: Str) #check the existing functionality that might exist for this
            return "SUCCESS"
    '''

