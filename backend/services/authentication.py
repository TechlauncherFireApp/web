from typing import Tuple, Any

from sqlalchemy.orm import Session

from domain import User
from domain.type import UserType, RegisterResult, LoginResult
from domain.type import Gender
from domain.type import Diet
from domain import User, PasswordRetrieval
from domain.type import UserType, RegisterResult, LoginResult, ForgotPassword, VerifyCode, ResetPassword
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
                 phone: str, gender: str, diet: str, allergy: str) -> RegisterResult:
        """
        Register a new user in the application.
        :param allergy: The users' allergy
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
                        diet=diet,
                        allergy=allergy)
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
    def send_code(session: Session, email: str) -> ForgotPassword:
        """
        input email address, verify user account, and send code through email
        :param session:
        :param email: input email address
        :return: error code
        """
        user = session.query(User).filter(User.email == email).first()
        if user is None:
            return ForgotPassword.EMAIL_NOT_FOUND
        # generate a six-figure character and number mixed string.
        _ALL_CHARACTERS = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        generate_code = ''
        for _ in range(6):
            index = random.randint(0, len(_ALL_CHARACTERS)-1)
            generate_code += _ALL_CHARACTERS[index]
        subject = '[FireApp3.0] Your Password Reset Code'
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
            FireApp3.0 Team'
        """ % (email, generate_code)
        MailSender().email(email, subject, content)
        resend_user = session.query(PasswordRetrieval).filter(PasswordRetrieval.email == email).first()
        if resend_user is None:
            code_query = PasswordRetrieval(email=email, code=generate_code, created_datetime=datetime.now(), expired_datetime=datetime.now()+timedelta(days=1))
            session.add(code_query)
        else:
            resend_user.code = generate_code
            resend_user.created_datetime = datetime.now()
            resend_user.expired_datetime = resend_user.created_datetime + timedelta(days=1)
            session.commit()
        session.flush()
        return ForgotPassword.SUCCESS

    # Groundwork for verify code backend function
    @staticmethod
    def verify_code(session: Session, email: str, code: str):
        """
        Verify the input code with the code in the database, and check whether it is overdue.
        :param session:
        :param email: user's email, inherit from the last page
        :param code: input code from email
        :return: error code
        """
        query = session.query(PasswordRetrieval).filter(PasswordRetrieval.email == email).first()
        if query is None or query.code is None:
            return VerifyCode.FAIL
        now_time = datetime.now()
        if now_time > query.expired_datetime:
            return VerifyCode.CODE_OVERDUE
        if query.code == code:
            return VerifyCode.CODE_CORRECT
        else:
            return VerifyCode.CODE_INCORRECT

    #  CheckUserCode takes the user session and the code and confirms the code is correct.We should consider looking into how security codes are handled in industry.
    #  We can add captcha to make it safer

    @staticmethod
    def reset_password(session: Session, email: str, new_password: str, repeat_password: str):
        """
        Reset password, check whether two input passwords are same.
        :param session:
        :param email: user's email, inherit from the last page
        :param new_password: new password
        :param repeat_password: same as the new password
        :return:
        """
        user = session.query(User).filter(User.email == email).first()
        if user is None or new_password is None:
            return ResetPassword.FAIL
        if new_password != repeat_password:
            return ResetPassword.RECHECK_TWO_INPUTS
        if not passwordService.validate(new_password):
            return ResetPassword.BAD_PASSWORD
        # old_password = user.password
        password_hash = passwordService.hash(new_password)
        user.password = password_hash
        session.commit()
        session.flush()
        subject = '[FireApp3.0] Your Password Reset Code'
        content = """
                    Dear <strong>%s</strong>,</br>
                    Your password was recently changed successfully!
                    </br></br>
                    If you didn't make this change, please contact us.
                    </br></br>
                    Best Wishes,
                    </br>
                    FireApp3.0 Team'
                """ % (user.last_name)
        MailSender().email(email, subject, content)
        # test = session.query(User).filter(User.email == email).first()
        # print("test", passwordService.compare(old_password, test.password))
        return ResetPassword.SUCCESS


