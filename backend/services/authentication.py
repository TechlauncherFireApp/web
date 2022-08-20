from typing import Tuple, Any

from sqlalchemy.orm import Session

from domain import User
from domain.type import UserType, RegisterResult, LoginResult
from domain.type.Gender import Gender
from domain.type.diet import Diet
from services.jwk import JWKService
from services.password import PasswordService

passwordService = PasswordService()
jwk_service = JWKService()


class AuthenticationService():

    @staticmethod
    def register(session: Session, email: str, password: str, given_name: str, last_name: str,
                 phone: str, gender: str, diet: str) -> RegisterResult:
        """
        Register a new user in the application.
        :param gender: The users gender to register with.
        :param diet: The users dietary to register with.
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

        if gender is None or gender == "":
            gender = Gender.Male

        if diet is None or diet == "":
            diet = Diet.meals

        # Everything seems fine, so we go ahead and create the user & the linked account.
        password_hash = passwordService.hash(password)
        new_user = User(role=UserType.VOLUNTEER, password=password_hash, first_name=given_name, last_name=last_name,
                        mobile_number=phone, email=email, preferred_hours={}, experience_years=0, possibleRoles=["Basic"],
                        qualifications=[],
                        availabilities={"Friday": [], "Monday": [], "Sunday": [], "Tuesday": [], "Saturday": [],
                                        "Thursday": [], "Wednesday": []},
                        gender=gender,
                        diet=diet)
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
