import json
from datetime import datetime

from domain import User, RegisterResult


def modify_profile(session, id, phone, gender, dietary, allergy) -> bool:
    user = session.query(User).filter(User.id == id).first()
    # session.expunge(question)
    if not user:
        return False
    if phone is not None:
        user.mobile_number = phone
    if gender is not None:
        user.gender = gender
    if dietary is not None:
        user.diet = dietary
    if allergy is not None:
        user.allergy = allergy
    user.update_date_time = datetime.now()
    return True


def get_profile(session, id):
    user = session.query(User).filter(User.id == id).first()
    if user:
        return user
    else:
        return None
