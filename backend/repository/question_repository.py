import json

from sqlalchemy import func

from domain import Question, QuestionType


def get_question_by_id(session, question_id):
    """
    search question by question id
    :return: question object
    """
    question = session.query(Question).filter(Question.id == question_id).first()
    if question and question.status == 1:
        # We need to use the object after this session closed
        session.expunge(question)
        # delete reason content in choice (not displayed when getting questions)
        choice = json.loads(question.choice)
        for row in choice:
            row.pop('reason')
        question.choice = choice
        return question
    else:
        return None


def get_question_list(session, num):
    """
    get random questions
    :param session:
    :param num: number of questions
    :return: question list
    """
    questions = session.query(Question).filter(Question.status == 1).order_by(func.random()).limit(num).all()
    # We need to use objects after this session closed
    session.expunge_all()
    # delete reason content in choice (not displayed when getting questions)
    for question in questions:
        choice = json.loads(question.choice)
        for choice_row in choice:
            choice_row.pop('reason')
        question.choice = choice
    return questions
