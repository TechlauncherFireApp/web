from domain import Question, QuestionType

#
def get_question_by_id(session, question_id):
    """
    search question by question id
    :return: question object
    """
    question = session.query(Question).filter(Question.id == question_id).first()
    if question and question.status == 1:
        # We should use the object after this session closed
        session.expunge(question)
        return question
    else:
        return None
