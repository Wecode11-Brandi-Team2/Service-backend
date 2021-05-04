class QnaService:
    def __init__(self, qna_dao):
        self.qna_dao = qna_dao

    def insert_question(self, qna_info, session):
        self.qna_dao.insert_question(qna_info, session)

    def delete_question(self, question_info, session):
        row_count = self.qna_dao.delete_question(question_info, session)

        return row_count

    def get_qnas(self, qna_info, session):
        questions = self.qna_dao.get_qnas(qna_info, session)

        return questions
