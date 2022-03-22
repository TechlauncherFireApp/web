from domain import Question, QuestionType


def get_question_by_id(session, question_id):
    question = session.query(Question).filter(Question.id == question_id).first()
    if question and question.status == 1:
        session.expunge(question)
        return question
    else:
        return None
