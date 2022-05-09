import sqlalchemy

from domain import ChatbotInput
from sqlalchemy.orm import Session


def get_input_by_user_email(session: Session, user_email):
    input_list = session.query(ChatbotInput)\
        .filter(ChatbotInput.user_email == user_email)\
        .order_by(sqlalchemy.desc(ChatbotInput.created_time)).all()
    session.expunge_all()
    return input_list


def add_chatbot_input(session: Session, user_email, content):
    chatbot_input = ChatbotInput(user_email=user_email, content=content)
    session.add(chatbot_input)
    session.flush()
    return True
