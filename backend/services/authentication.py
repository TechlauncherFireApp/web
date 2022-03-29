from typing import Tuple, Any

from sqlalchemy.orm import Session

from domain import User, PasswordRetrieval
from domain.type import UserType, RegisterResult, LoginResult, ForgotPassword
from services.jwk import JWKService
from services.password import PasswordService
from services.mail_sms import MailSender

import random
from datetime import datetime,timedelta

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
    @staticmethod
    def generate_code(code_len: int):
        all_chars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        last_pos = len(all_chars) - 1
        code = ''
        for _ in range(code_len):
            index = random.randint(0, last_pos)
            code += all_chars[index]
        return code

    @staticmethod
    def send_code(session: Session, email: str):
        """
        input email address, verify user account, and send code through email
        :param session:
        :param email: input email address
        :return: error code
        """
        # TODO: need to be able to resend the email and show the count down, if it is possible to implement.
        user = session.query(User).filter(User.email == email).first()
        if user is None:
            return ForgotPassword.EMAIL_NOT_FOUND
        # generate a six-figure character and number mixed string.
        _ALL_CHARACTERS = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        generate_code = ''
        for _ in range(6):
            index = random.randint(0, len(_ALL_CHARACTERS)-1)
            generate_code += _ALL_CHARACTERS[index]
        # send verification code email with subject, content, and the code
        subject = 'Your password reset code.'
        content = """
            Hi,</br>
            You recently requested to rest the password for your %s account. Use the code below to proceed.
            </br></br>
            code: <strong>%s</strong>
            </br></br>
            If you did not request a password reset, please ignore this email. 
            This password reset code is only valid for the next 30 minutes.
            </br></br>
            Thanks,
            </br>
            FireApp 3.0 Team'
        """ % (email, generate_code)
        MailSender().email(email, subject, content)
        code_expired_time = datetime.now()+timedelta(days=1)
        code_query = PasswordRetrieval(email=email, code=generate_code, created_time=datetime.now(), expired_time=code_expired_time)
        session.add(code_query)
        session.flush()
        return ForgotPassword.SUCCESS


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

