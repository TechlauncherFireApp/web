import json
from datetime import datetime

from sqlalchemy import func

from domain import Question


def get_question_by_id(session, question_id):
    """
    search question by question id
    :return: question object
    """
    question = session.query(Question).filter(Question.id == question_id).first()
    if question and question.status == 1:
        # We need to use the object after this session closed
        session.expunge(question)
        _parse_choice(question)
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
    for question in questions:
        _parse_choice(question)
    return questions


def _parse_choice(question):
    """
    Parse choice of question and remove reason field in choice (if exists).
    If decode error, fill choice in empty choice
    :param question: question object
    """
    empty_choice = [{'id': '', 'content': ''}]
    try:
        # load choice in json format
        choice = json.loads(question.choice)
        # delete reason content in choice (not displayed when getting questions)
        for row in choice:
            if row['reason']:
                row.pop('reason')
        question.choice = choice
    except json.JSONDecodeError:
        # load empty choice
        question.choice = empty_choice


def create_question(session, question_type, role, description, choice, difficulty, answer):
    """
    create a new question
    :param session:
    :param question_type: question_type.QuestionType(Enum)
    :param role: String,
    :param description: String, question content
    :param choice: String, question choices, JSON format
    :param difficulty: Integer, FROM 0 TO 4
    :param answer: String, A/B/C/D
    :return: returns id of the new question
    """
    question = Question(question_type=question_type, role=role, description=description, choice=choice,
                        difficulty=difficulty, answer=answer)
    session.add(question)
    # session.expunge(question)
    session.flush()
    return question.id


def delete_question(session, question_id):
    """
    delete a question
    :param session:
    :param question_id: id of the question want to delete
    :return: True: delete successful
             False: delete successful
    """
    existing = session.query(Question).filter(Question.id == question_id).first()
    if existing is not None:
        existing.status = False
        # session.delete(existing)
        # session.flush()
        return True
    return False


def update_question(session, question_id, role, description, choice, difficulty, answer):
    """
    update a question
    :param session:
    :param question_id: Integer, id
    :param role: String
    :param description: String, question content
    :param choice: String, question choices, JSON format
    :param difficulty: Integer, FROM 0 TO 4
    :param answer: String, A/B/C/D

    """
    question = session.query(Question).filter(Question.id == question_id).first()
    # session.expunge(question)
    if not question or question.status == 0:
        return False
    if role is not None:
        question.role = role
    if description is not None:
        question.description = description
    if choice is not None:
        question.choice = choice
    if difficulty is not None:
        question.difficulty = difficulty
    if answer is not None:
        question.answer = answer
    question.update_time = datetime.now()
    return True


def check_answer(session, question_id, answer):
    """
    check the answer
    :param session:
    :param question_id:
    :param answer: one character, e.g: A/B/C/D...
    :return:
    """
    question = session.query(Question).filter(Question.id == question_id).first()
    return question.answer == answer
